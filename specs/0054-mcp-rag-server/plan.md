# Plan: MCP RAG Server (spec 0054)

## Approach

Follow the `dispatch_*` / pure-function pattern established by 0052 (resources
server), 0053 (memory-graph server), and 0056 T-003 (market-research server).
One new file: `src/quantsmith/adapters/mcp_servers/rag_resources.py`.

### Public surface

```python
@dataclass(frozen=True)
class RagRecord:
    uri: str           # knowledge://<authority>/...
    text: str          # full text to index (citation summary from the source server)
    access_level: str  # public | internal | restricted

@dataclass(frozen=True)
class SearchHit:
    uri: str
    passage: str       # ≤ 500-char sentence excerpt, best query overlap
    score: float       # TF-IDF dot product (rounded to 6 dp)
    access_level: str

def build_index(records: Sequence[RagRecord]) -> RagIndex: ...
def dispatch_rag(message: Dict[str, Any], *, index: RagIndex) -> Dict[str, Any]: ...
```

`RagIndex` is an opaque object with no public fields. Callers build it once
from their translated records, then hand it to `dispatch_rag` on each request.
The index contains only the caller-filtered records; there is no second filtering
step at build time. `dispatch_rag` also checks clearance at dispatch time
(double enforcement — RISK-001).

### `RagIndex` internals

```python
@dataclass
class _IndexedDoc:
    uri: str
    access_level: str
    text: str                   # original text (for resources/read)
    tf: Dict[str, float]        # term → tf (count / doc_len)
    sentences: List[str]        # split on '.', '!', '?', '\n'

class RagIndex:
    _docs: List[_IndexedDoc]
    _idf: Dict[str, float]      # term → log((N+1)/(df+1)) + 1.0
```

### TF-IDF implementation (stdlib)

```
tokenize(text) → lowercase, re.findall('[a-z]+'), drop stop words, drop len≤2

tf(tokens) = {term: count(term) / len(tokens)}

idf(term) = log((N + 1) / (df[term] + 1)) + 1.0   [smoothed, +1 additive]
            where N = number of indexed documents
                  df[term] = number of docs containing term

score(query, doc) = sum(tf[doc][t] * idf[t] for t in tokenize(query) if t in tf[doc])
```

The +1 additive smoothing prevents division-by-zero on unseen terms and gives
all known terms a positive IDF floor, which keeps short documents fairly ranked.

### Passage extraction

```
sentences(text) → re.split(r'(?<=[.!?])\s+|\n', text)
best_sentence → argmax(|q_tokens ∩ tokenize(sent)|, tiebreak by position)
passage = best_sentence[:500]
```

If the text has no sentence boundaries (a single long string), the passage is
the first 500 characters.

### `resources/search` dispatch

```
params:
  query            (required str)  → -32602 if empty/whitespace
  caller_clearance (required str)  → -32600 if missing/unrecognized
  domain           (optional str, default "all") → -32602 if not in VALID_DOMAINS
  top_k            (optional int, default 5)     → -32602 if not in [1, 20]

result:
  {"hits": [{"uri":…, "passage":…, "score":…, "access_level":…}, …]}
```

### `resources/list` dispatch

Same response shape as 0052/0053. Returns all docs in the index within the
caller's clearance, sorted by URI. Uses `clearance_allows` from `contract.py`.

### `resources/read` dispatch

URI must be present in the index. Existence masking: both "not in index" and
"clearance denied" return -32600 (not -32604).

### Authority routing in `resources/read`

`dispatch_rag` does NOT check the URI authority against `KNOWN_AUTHORITIES` from
`contract.py` — the RAG server indexes records from multiple authorities, so any
`knowledge://` URI present in the index is valid. A URI not in the index returns
-32600.

## Traceability

| REQ | Implemented by |
| --- | --- |
| REQ-001 | `dispatch_rag` signature; no file I/O in module |
| REQ-002 | `clearance` check at top of `dispatch_rag` |
| REQ-003 | `resources/search` branch in `dispatch_rag` |
| REQ-004 | `if not query.strip()` → ERR_INVALID_PARAMS |
| REQ-005 | `top_k` bounds check → ERR_INVALID_PARAMS |
| REQ-006 | `domain` membership check → ERR_INVALID_PARAMS |
| REQ-007 | `scored.sort(key=lambda x: (-x.score, x.uri))` |
| REQ-008 | `clearance_allows(doc.access_level, caller_clearance)` gate in search + list + read |
| REQ-009 | `read` returns -32600 for both missing and denied URIs |
| REQ-010 | `list` iterates `_docs`, filters, sorts by URI |
| REQ-011 | `SearchHit` dataclass fields |
| REQ-012 | `math.log`, `collections.Counter` in `build_index` |
| REQ-013 | `_best_passage(sentences, q_tokens)[:500]` |
| REQ-014 | method not in `SUPPORTED_METHODS | {"resources/search"}` → ERR_METHOD_NOT_FOUND |

## Files

| File | Action |
| --- | --- |
| `src/quantsmith/adapters/mcp_servers/rag_resources.py` | Create |
| `tests/test_rag_resources.py` | Create |
| `specs/0054-mcp-rag-server/spec.md` | Create |
| `specs/0054-mcp-rag-server/plan.md` | Create |
| `specs/0054-mcp-rag-server/tasks.md` | Create |
| `specs/README.md` | Add 0054 row |
| `README.md` | Increment runtime count; add 0054 row |
| `docs/handoff.md` | Mark 0054 done; update next free spec |
| `src/quantsmith/adapters/mcp_servers/__init__.py` | Add docstring note |
