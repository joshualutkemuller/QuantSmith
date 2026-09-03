"""RAG Resources Server — spec 0054.

TF-IDF search (stdlib only) over the knowledge store with per-access-tier
filtering and cited passages. Extends the 0052 adapter contract with a new
``resources/search`` method.

Usage::

    from quantsmith.adapters.mcp_servers.rag_resources import (
        RagRecord, SearchHit, build_index, dispatch_rag,
    )

    index = build_index([
        RagRecord(uri="knowledge://memory/scope/id", text="...", access_level="internal"),
        RagRecord(uri="knowledge://market_research/eq/note/n001", text="...", access_level="public"),
    ])
    resp = dispatch_rag(
        {"jsonrpc": "2.0", "method": "resources/search", "id": 1,
         "params": {"caller_clearance": "internal", "query": "momentum signal"}},
        index=index,
    )

No ``mcp`` package dependency (NFR-001). No I/O — ``RagIndex`` is built from
caller-injected ``RagRecord`` objects (NFR-002). Clearance enforced via
``ACCESS_RANK`` from ``contract.py`` (NFR-003). Sort key ``(-score, uri)``
ensures deterministic results (NFR-004).

**Governance invariants (from 0052):**

- ``caller_clearance`` is required; absent → -32600 (RISK-001).
- Records beyond the caller's clearance are excluded from search, list, and read
  (double enforcement: index may be pre-filtered by caller AND dispatch re-checks).
- Existence masking: both "not in index" and "clearance denied" return -32600
  on ``resources/read`` so callers cannot probe for restricted record existence
  (RISK-003).
- Passages are sentence-level excerpts (≤ 500 chars), never raw store objects
  (RISK-002).
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .contract import (
    ERR_ACCESS_DENIED,
    ERR_METHOD_NOT_FOUND,
    METHOD_LIST,
    METHOD_READ,
    SUPPORTED_CLEARANCES,
    McpResponse,
    ResourceContent,
    ResourceMeta,
    clearance_allows,
    error_response,
    parse_request,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

METHOD_SEARCH = "resources/search"

VALID_DOMAINS: Tuple[str, ...] = ("memory", "market_research", "sources", "all")

_TOP_K_DEFAULT = 5
_TOP_K_MAX = 20
_PASSAGE_MAX = 500

ERR_INVALID_PARAMS = -32602

_STOP_WORDS: frozenset = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "it", "its", "not",
    "no", "nor", "so", "yet", "as", "if", "then", "than", "when", "where",
    "which", "who", "how", "this", "that", "these", "those", "via", "per",
})

# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RagRecord:
    """A document ready for indexing.

    The caller translates from their store format (workflow_memory.Record,
    MarketResearchItem, or any text blob) before calling ``build_index``.
    """

    uri: str            # knowledge://<authority>/...
    text: str           # full text to index (citation summary is recommended)
    access_level: str   # public | internal | restricted


@dataclass(frozen=True)
class SearchHit:
    """One ranked result from ``resources/search``."""

    uri: str
    passage: str        # ≤ 500-char sentence excerpt
    score: float        # TF-IDF dot product, rounded to 6 dp
    access_level: str


# ---------------------------------------------------------------------------
# Internal index structures
# ---------------------------------------------------------------------------


@dataclass
class _IndexedDoc:
    uri: str
    access_level: str
    text: str
    tf: Dict[str, float]
    sentences: List[str]


class RagIndex:
    """Pre-built TF-IDF index.  Build via ``build_index(records)``."""

    def __init__(self, docs: List[_IndexedDoc], idf: Dict[str, float]) -> None:
        self._docs = docs
        self._idf = idf


# ---------------------------------------------------------------------------
# Tokenizer + TF-IDF helpers
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> List[str]:
    return [
        t for t in re.findall(r"[a-z]+", text.lower())
        if t not in _STOP_WORDS and len(t) > 2
    ]


def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    if not tokens:
        return {}
    counts: Counter = Counter(tokens)
    n = len(tokens)
    return {t: c / n for t, c in counts.items()}


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n", text)
    return [p.strip() for p in parts if p.strip()]


def _best_passage(sentences: List[str], q_tokens: List[str]) -> str:
    if not sentences:
        return ""
    q_set = set(q_tokens)
    best = max(
        sentences,
        key=lambda s: (len(q_set & set(_tokenize(s))), -sentences.index(s)),
    )
    return best[:_PASSAGE_MAX]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_index(records: Sequence[RagRecord]) -> RagIndex:
    """Build a TF-IDF index from caller-supplied records.

    The caller is responsible for:
    - Translating their records into ``RagRecord`` objects.
    - Pre-filtering by access tier if desired (the dispatch layer re-checks).
    - Running ``contains_secret()`` on record text before including it.
    """
    docs: List[_IndexedDoc] = []
    for rec in records:
        tokens = _tokenize(rec.text)
        tf = _compute_tf(tokens)
        sentences = _split_sentences(rec.text)
        docs.append(_IndexedDoc(
            uri=rec.uri,
            access_level=rec.access_level,
            text=rec.text,
            tf=tf,
            sentences=sentences,
        ))

    n = len(docs)
    df: Counter = Counter()
    for doc in docs:
        df.update(set(doc.tf.keys()))

    idf: Dict[str, float] = {
        t: math.log((n + 1) / (df[t] + 1)) + 1.0
        for t in df
    }

    return RagIndex(docs=docs, idf=idf)


def search_index(
    index: RagIndex,
    query: str,
    caller_clearance: str,
    top_k: int = _TOP_K_DEFAULT,
    domain: str = "all",
) -> List[SearchHit]:
    """Rank records in ``index`` by TF-IDF similarity to ``query``.

    Records beyond ``caller_clearance`` are silently excluded (REQ-008).
    Results are sorted by score descending, URI ascending for ties (REQ-007,
    NFR-004).
    """
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    scored: List[Tuple[float, str, str, str]] = []  # score, uri, access_level, passage
    for doc in index._docs:
        if not clearance_allows(doc.access_level, caller_clearance):
            continue
        if domain != "all":
            # URI authority is the segment between "knowledge://" and the next "/"
            after_scheme = doc.uri[len("knowledge://"):]
            authority = after_scheme.split("/")[0] if "/" in after_scheme else after_scheme
            if authority != domain:
                continue

        score = sum(
            doc.tf.get(t, 0.0) * index._idf.get(t, 0.0)
            for t in q_tokens
        )
        if score > 0.0:
            passage = _best_passage(doc.sentences, q_tokens)
            scored.append((score, doc.uri, doc.access_level, passage))

    scored.sort(key=lambda x: (-x[0], x[1]))
    return [
        SearchHit(
            uri=s[1],
            passage=s[3],
            score=round(s[0], 6),
            access_level=s[2],
        )
        for s in scored[:top_k]
    ]


def list_index_resources(
    index: RagIndex,
    caller_clearance: str,
) -> List[ResourceMeta]:
    """Return metadata for all records in the index within caller's clearance."""
    metas: List[ResourceMeta] = []
    for doc in index._docs:
        if not clearance_allows(doc.access_level, caller_clearance):
            continue
        metas.append(ResourceMeta(
            uri=doc.uri,
            name=doc.uri.split("/")[-1],
            description=f"RAG-indexed record ({doc.access_level})",
            mime_type="text/plain",
            access_level=doc.access_level,
        ))
    metas.sort(key=lambda m: m.uri)
    return metas


def read_index_resource(
    index: RagIndex,
    uri: str,
    caller_clearance: str,
) -> ResourceContent:
    """Return a record's full text.

    Existence masking: both "not in index" and "clearance denied" raise
    ``PermissionError`` so callers cannot probe for restricted record existence
    (RISK-003 / REQ-009).
    """
    doc = next((d for d in index._docs if d.uri == uri), None)
    # Not found → PermissionError (not FileNotFoundError) — existence masking
    if doc is None:
        raise PermissionError(f"access denied: {uri!r}")
    if not clearance_allows(doc.access_level, caller_clearance):
        raise PermissionError(f"access denied ({doc.access_level}): {uri!r}")
    return ResourceContent(uri=uri, text=doc.text, mime_type="text/plain")


def dispatch_rag(
    message: Dict[str, Any],
    *,
    index: RagIndex,
) -> Dict[str, Any]:
    """Dispatch a JSON-RPC 2.0 message to the RAG resources server.

    Handles ``resources/search``, ``resources/list``, and ``resources/read``.
    Returns a JSON-serializable dict. No I/O.
    """
    try:
        req = parse_request(message)
    except ValueError as exc:
        return error_response(message.get("id"), ERR_ACCESS_DENIED, str(exc)).to_dict()

    # caller_clearance required on every request (RISK-001, REQ-002)
    clearance = req.caller_clearance
    if not clearance:
        return error_response(req.id, ERR_ACCESS_DENIED, "caller_clearance is required").to_dict()
    if clearance not in SUPPORTED_CLEARANCES:
        return error_response(
            req.id, ERR_ACCESS_DENIED,
            f"unrecognized caller_clearance {clearance!r}",
        ).to_dict()

    if req.method not in (METHOD_SEARCH, METHOD_LIST, METHOD_READ):
        return error_response(
            req.id, ERR_METHOD_NOT_FOUND,
            f"method {req.method!r} not supported",
        ).to_dict()

    # ------------------------------------------------------------------
    # resources/search
    # ------------------------------------------------------------------
    if req.method == METHOD_SEARCH:
        query: str = req.params.get("query", "")
        if not query or not query.strip():
            return error_response(req.id, ERR_INVALID_PARAMS, "query must be a non-empty string").to_dict()

        domain: str = req.params.get("domain", "all")
        if domain not in VALID_DOMAINS:
            return error_response(
                req.id, ERR_INVALID_PARAMS,
                f"domain {domain!r} must be one of {VALID_DOMAINS}",
            ).to_dict()

        raw_top_k: Any = req.params.get("top_k", _TOP_K_DEFAULT)
        try:
            top_k = int(raw_top_k)
        except (TypeError, ValueError):
            return error_response(req.id, ERR_INVALID_PARAMS, "top_k must be an integer").to_dict()
        if not (1 <= top_k <= _TOP_K_MAX):
            return error_response(
                req.id, ERR_INVALID_PARAMS,
                f"top_k must be in [1, {_TOP_K_MAX}], got {top_k}",
            ).to_dict()

        hits = search_index(index, query.strip(), clearance, top_k, domain)
        return McpResponse(
            id=req.id,
            result={
                "hits": [
                    {
                        "uri": h.uri,
                        "passage": h.passage,
                        "score": h.score,
                        "access_level": h.access_level,
                    }
                    for h in hits
                ]
            },
        ).to_dict()

    # ------------------------------------------------------------------
    # resources/list
    # ------------------------------------------------------------------
    if req.method == METHOD_LIST:
        metas = list_index_resources(index, clearance)
        return McpResponse(
            id=req.id,
            result={
                "resources": [
                    {
                        "uri": m.uri,
                        "name": m.name,
                        "description": m.description,
                        "mimeType": m.mime_type,
                        "access_level": m.access_level,
                    }
                    for m in metas
                ]
            },
        ).to_dict()

    # ------------------------------------------------------------------
    # resources/read
    # ------------------------------------------------------------------
    uri: str = req.params.get("uri", "")
    if not uri:
        return error_response(req.id, ERR_ACCESS_DENIED, "missing 'uri' parameter").to_dict()

    try:
        content = read_index_resource(index, uri, clearance)
    except PermissionError as exc:
        return error_response(req.id, ERR_ACCESS_DENIED, str(exc)).to_dict()

    return McpResponse(
        id=req.id,
        result={
            "contents": [
                {"uri": content.uri, "text": content.text, "mimeType": content.mime_type}
            ]
        },
    ).to_dict()
