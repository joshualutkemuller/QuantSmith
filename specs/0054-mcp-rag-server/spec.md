# Spec: MCP RAG Server

- **ID:** 0054-mcp-rag-server
- **Status:** Draft
- **Author:** QuantSmith
- **Last updated:** 2026-09-03
- **Depends on:** 0052 (MCP adapter contract)

> WHAT and WHY only. No implementation detail — that belongs in `plan.md`.

## Problem & Context

Specs 0052 (resources server), 0053 (memory-graph server), and 0056 T-003
(market-research server) made the three knowledge domains reachable over MCP.
All three support `resources/list` and `resources/read`. Neither supports
*search* — a caller who doesn't know a record's URI must list everything and
filter client-side, which grows linearly with the store.

This spec adds a `resources/search` method: given a free-text query, the server
ranks all records the caller may access by relevance and returns the top-K
results as cited passages. One index per access tier enforces the clearance
boundary: an index built for the `internal` tier never contains `restricted`
records, so a bug in scoring can never surface restricted content to an
`internal` caller.

The RAG server is the fourth and final knowledge-domain server in the 0052
contract. It extends the contract without modifying it: the same
`caller_clearance` enforcement, the same `knowledge://` URI scheme, the same
`dispatch_*` / pure-function pattern.

## Goals

1. Add `resources/search` to the 0052 MCP contract, returning ranked hits with
   cited passages for the caller's clearance tier.
2. Build TF-IDF indexes using stdlib only; no vector-library dependency.
3. Enforce per-access-tier isolation: an `internal` caller can never see
   `restricted` records regardless of query content or scoring.
4. Return cited passages (sentence-level excerpts), never raw store objects.

## Non-Goals

- Embedding-based semantic search: deferred; requires a vector library.
- Network-fetched content or live index updates: indexes are caller-injected.
- Persistent index storage: the index is rebuilt from injected records per
  session.
- Writing or mutating records (read-only, same as 0052–0053).
- Cross-store federation beyond the three authorities (sources, memory,
  market_research).
- Pagination for `resources/search` results: `top_k` bounds the response size.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | `dispatch_rag(message, *, index)` MUST be a pure function: no I/O, returns a JSON-RPC 2.0 dict. The `RagIndex` is caller-built from a caller-supplied `Sequence[RagRecord]`. | must |
| REQ-002 | `caller_clearance` MUST be required on every request; absent or unrecognized → -32600. | must |
| REQ-003 | The server MUST implement `resources/search` with required `query` param and optional `domain` and `top_k` params. | must |
| REQ-004 | An empty or whitespace-only `query` MUST return error -32602. | must |
| REQ-005 | `top_k` MUST default to 5; values outside `[1, 20]` MUST return error -32602. | must |
| REQ-006 | `domain` MUST be one of `memory`, `market_research`, `sources`, `all` (default `all`); an unknown value MUST return -32602. | must |
| REQ-007 | Results MUST be sorted by score descending, then by URI ascending for ties (deterministic). | must |
| REQ-008 | Records beyond the caller's clearance MUST NOT appear in search results, list, or read responses. | must |
| REQ-009 | `resources/read` for a record at or below the caller's clearance MUST return the record's full text. Existence masking applies: a denied or absent URI MUST return -32600, not -32604. | must |
| REQ-010 | `resources/list` MUST return metadata for all indexed records within the caller's clearance, sorted by URI. | must |
| REQ-011 | Each `SearchHit` in a `resources/search` response MUST include `uri`, `passage`, `score`, and `access_level`. | must |
| REQ-012 | Scoring MUST use TF-IDF (stdlib `collections.Counter` + `math.log`); no new entry in `pyproject.toml`. | must |
| REQ-013 | The passage in each hit MUST be a sentence-level excerpt (≤ 500 characters) from the record's text, selected by maximum query-term overlap. | must |
| REQ-014 | Unsupported methods MUST return error -32601. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Standard library only. | No new entry in `pyproject.toml`. |
| NFR-002 | No I/O in the adapter; the `RagIndex` is built from caller-injected records. | Testable without filesystem or network. |
| NFR-003 | Clearance enforcement uses `ACCESS_RANK` from `contract.py`. | Same enforcement constant as 0052–0053. |
| NFR-004 | Deterministic: same query, same index, same caller_clearance → identical ranked results. | Enables reproducible test assertions. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a request missing `caller_clearance`, when dispatched, then the response error code is -32600. | REQ-002 |
| AC-002 | Given `resources/search` with `query: ""`, when dispatched, then the response error code is -32602. | REQ-004 |
| AC-003 | Given `resources/search` with `top_k: 25`, when dispatched, then the response error code is -32602. | REQ-005 |
| AC-004 | Given `resources/search` with `domain: "unknown"`, when dispatched, then the response error code is -32602. | REQ-006 |
| AC-005 | Given two records where record A scores 0.8 and record B scores 0.5, when searched, then A precedes B in results. | REQ-007 |
| AC-006 | Given a `restricted` and an `internal` record, when searched with `caller_clearance: internal`, then only the `internal` record appears in results. | REQ-008 |
| AC-007 | Given `internal` and `restricted` records, when searched with `caller_clearance: public`, then no record appears. | REQ-008 |
| AC-008 | Given five matching records, when searched with `top_k: 2`, then at most two hits are returned. | REQ-005 |
| AC-009 | Given a matching record in search results, then each hit contains `uri`, `passage`, `score`, and `access_level`. | REQ-011 |
| AC-010 | Given an unsupported method `memory/query`, when dispatched, then the response error code is -32601. | REQ-014 |
| AC-011 | Given an index with public and restricted records, when `resources/list` is dispatched with `caller_clearance: internal`, then only public and internal records appear, sorted by URI. | REQ-010 |
| AC-012 | Given an `internal` record in the index, when `resources/read` is dispatched with `caller_clearance: internal`, then the response contains the record's text. | REQ-009 |
| AC-013 | Given a `restricted` record, when `resources/read` is dispatched with `caller_clearance: internal`, then the response error code is -32600 (existence masking). | REQ-009 |
| AC-014 | Given records from `memory` and `market_research` domains, when searched with `domain: memory`, then only memory records appear in results. | REQ-006 |
| AC-015 | Given a `restricted` record in the index, when searched with `caller_clearance: restricted`, then the restricted record may appear in results. | REQ-008, REQ-003 |

## Data & Dependencies

- **`src/quantsmith/adapters/mcp_servers/contract.py`** — `ACCESS_RANK`,
  `clearance_allows`, `KnowledgeUri`, `McpResponse`, `error_response`,
  `parse_request`, `SUPPORTED_CLEARANCES` (spec 0052).
- **`src/quantsmith/adapters/mcp_servers/memory_resources.py`** — pattern source
  for `dispatch_*`, `list_*`, `read_*` helpers (spec 0053).
- No dependency on `workflow_memory.py` or `market_research.py`; the caller
  translates their records into `RagRecord` objects before calling `build_index`.

No private data in the adapter itself. Record text comes from the caller;
passages are sentence-level substrings, never raw store objects.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Scoring bug surfaces `restricted` content to a lower-clearance caller. | Compliance incident. | Per-access-tier index isolation: the `RagIndex` is built from caller-filtered records; the dispatch layer also checks clearance before returning any hit. Double enforcement (REQ-008). |
| RISK-002 | A passage excerpt contains a credential-shaped string. | Credential exposure via search results. | Passages are sentence-level substrings, not full record text. The caller is responsible for credential-scanning records before indexing, consistent with `contains_secret()` in 0052 (REQ-007 of 0052). |
| RISK-003 | `resources/read` for a denied record reveals existence via a distinct -32604 error. | Metadata leakage. | Both "access denied" and "not in index" return -32600 (REQ-009, existence masking). |
| RISK-004 | Non-deterministic result ordering breaks test assertions. | Flaky tests; unreliable production behaviour. | Sort key is `(-score, uri)` — URI is a stable tiebreaker (REQ-007, NFR-004). |

## Assumptions & Open Questions

- Assumption: TF-IDF over sentence text is sufficient for the current store size
  (< 10 000 records). Embedding-based search is deferred to a future spec.
- Assumption: Passage length cap of 500 characters prevents response bloat
  without requiring pagination within a single hit.
- Open question: Should `resources/search` support `as_of` for point-in-time
  filtering over memory records? Deferred — the `RagRecord.text` field already
  reflects whatever the caller chose to include; point-in-time filtering is the
  caller's responsibility at index-build time.
- Open question: Should hit score be normalized to [0, 1]? Deferred; absolute
  TF-IDF scores are sufficient for ranking and are reproducible across runs on
  the same index.

## Exceptions

None.
