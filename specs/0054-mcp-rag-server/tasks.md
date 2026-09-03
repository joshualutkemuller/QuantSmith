# Tasks: MCP RAG Server

- **Spec:** 0054-mcp-rag-server (`spec.md`, `plan.md`)
- **Last updated:** 2026-09-03

## Definition of Done (applies to every task)

- Standard library only; no new dependency in `pyproject.toml` (NFR-001).
- `caller_clearance` required on every request; absent or unrecognized → -32600 (REQ-002).
- Existence masking: both "not in index" and "clearance denied" return -32600 on `resources/read` (REQ-009).
- Every `AC-*` has a named test.
- `clearance_allows` / `ACCESS_RANK` from `contract.py` is the enforcement constant — never a string comparison (NFR-003).
- Deterministic: same query, same index, same clearance → identical ranked results (NFR-004).

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Write `specs/0054-mcp-rag-server/spec.md` — requirements, ACs, risks | REQ-001–REQ-014, NFR-001–NFR-004 | done | |
| T-002 | Write `specs/0054-mcp-rag-server/plan.md` — TF-IDF design, passage extraction, traceability table | REQ-001–REQ-014, NFR-001–NFR-004 | done | |
| T-003 | Create `src/quantsmith/adapters/mcp_servers/rag_resources.py` — `RagRecord`, `SearchHit`, `build_index`, `search_index`, `list_index_resources`, `read_index_resource`, `dispatch_rag` | REQ-001–REQ-014, NFR-001–NFR-004 | done | |
| T-004 | Write `tests/test_rag_resources.py` — one test per AC-001–AC-015 | REQ-001–REQ-014, NFR-002–NFR-004 | done | |
| T-005 | Update `src/quantsmith/adapters/mcp_servers/__init__.py` — add 0054 docstring note | REQ-001, NFR-001 | done | |
| T-006 | Update `specs/README.md` — add 0054 row | REQ-001 | done | |
| T-007 | Update `README.md` — increment Specs count, add 0054 row | REQ-001 | done | |
| T-008 | Update `docs/handoff.md` — mark 0054 done, update planned specs entry | REQ-001 | done | |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test | Status |
| --- | --- | --- |
| AC-001 | `test_missing_clearance_returns_access_denied_AC_001`, `test_unrecognized_clearance_returns_access_denied_AC_001` | done |
| AC-002 | `test_empty_query_returns_invalid_params_AC_002`, `test_whitespace_query_returns_invalid_params_AC_002` | done |
| AC-003 | `test_top_k_too_large_returns_invalid_params_AC_003`, `test_top_k_zero_returns_invalid_params_AC_003` | done |
| AC-004 | `test_unknown_domain_returns_invalid_params_AC_004` | done |
| AC-005 | `test_higher_score_ranks_first_AC_005` | done |
| AC-006 | `test_internal_caller_excludes_restricted_records_AC_006` | done |
| AC-007 | `test_public_caller_sees_no_restricted_or_internal_AC_007` | done |
| AC-008 | `test_top_k_limits_result_count_AC_008` | done |
| AC-009 | `test_search_hit_fields_AC_009` | done |
| AC-010 | `test_unsupported_method_returns_method_not_found_AC_010` | done |
| AC-011 | `test_list_returns_accessible_records_sorted_AC_011` | done |
| AC-012 | `test_read_accessible_record_returns_text_AC_012` | done |
| AC-013 | `test_read_denied_record_returns_access_denied_AC_013`, `test_read_nonexistent_uri_also_returns_access_denied_AC_013` | done |
| AC-014 | `test_domain_filter_restricts_to_memory_AC_014` | done |
| AC-015 | `test_restricted_caller_sees_restricted_records_AC_015` | done |
