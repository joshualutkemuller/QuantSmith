# Tasks: Workflow Memory Runtime & Author Attribution

- **Spec:** 0048-workflow-memory-runtime (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-21

## Definition of Done (applies to every task)

- Standard library only; no new dependency in `pyproject.toml`.
- The committed `memory/` store parses and validates with **zero edits to its
  record files** — that is the backward-compatibility evidence (NFR-003).
- No raw email or OS username is ever written into a record.
- `memory-check.sh` still runs, and still performs its secret/PII scan, when
  the `quantsmith` package is not installed.
- Every `AC-*` has a named test; the pseudonymous-not-anonymous limit is stated
  in the code, not only in the spec.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Subset YAML parser + `Record`/`Store`/`Finding` dataclasses; `load_store`. | REQ-001, NFR-001, NFR-005 | todo | Raise `MemoryParseError(file, line, reason)` outside the subset — never guess (RISK-001). Committed store is the fixture. |
| T-002 | `query` with scope/type/confidence/status filters and deterministic ordering. | REQ-002, NFR-002 | todo | Total order: confidence, corroboration, `last_confirmed`, then `id`. |
| T-003 | Point-in-time filtering by `pit_scope`. | REQ-003 | todo | Unrecognised `pit_scope` ⇒ **excluded** and reported (RISK-004). Exclusion is the safe failure; inclusion leaks. |
| T-004 | `render_context` with a character budget, rank-ordered fill, and an explicit omitted count. | REQ-004 | todo | Budget is characters, not tokens — no tokenizer in this module. Show `last_confirmed` on every line. |
| T-005 | `validate`: required fields, enum values, duplicate ids, date order, author pattern. | REQ-005, REQ-009, REQ-010 | todo | This is what replaces grepping for the string `first_seen`. Missing author is a finding, not an error. |
| T-006 | `check_decay` against each store's `freshness_days`. | REQ-006 | todo | Reads the value `manifest.yaml` has always declared and nothing has ever read. |
| T-007 | `resolve_author` chain + pseudonymous handle derivation; `identity.yml` gitignored. | REQ-007, REQ-008, NFR-004 | todo | Env override short-circuits before any subprocess. Hex output cannot contain `@` — that is the guard, not convention. |
| T-008 | `store_version` content hash. | REQ-011 | todo | For `templates/docs/run_card.md`'s "memory version used". |
| T-009 | CLI entry (`python -m quantsmith.pipelines.workflow_memory --validate --decay`). | REQ-005, REQ-006 | todo | The seam `memory-check.sh` calls. |
| T-010 | Wire `memory-check.sh` to prefer the runtime, keeping the grep path as fallback. | REQ-005, REQ-006 | todo | Gate must degrade gracefully in a copied scaffold with no package. |
| T-011 | `tests/test_workflow_memory.py` — one test per AC. | NFR-002, NFR-003, NFR-005 | todo | Malformed fixtures in `tmp_path`; never commit broken YAML. |
| T-012 | Wire catalogs and docs: `specs/README.md`, root `README.md` runtime table, `src/quantsmith/pipelines/README.md`, `instructions/workflow_memory.md` (author field + pseudonymity), `agents/knowledge/*` (point at the runtime). | REQ-001 | todo | `doc-counts`, `spec-index`, and `readme-sync` all enforce parts of this. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Verification | Status |
| --- | --- | --- |
| AC-001 | `test_committed_store_loads_unchanged_AC_001` | todo |
| AC-002 | `test_query_by_scope_AC_002` | todo |
| AC-003 | `test_query_deterministic_AC_003` | todo |
| AC-004 | `test_pit_scope_excludes_original_vintage_AC_004` | todo |
| AC-005 | `test_render_budget_drops_lowest_ranked_AC_005` | todo |
| AC-006 | `test_missing_last_confirmed_flagged_AC_006` | todo |
| AC-007 | `test_duplicate_id_flagged_AC_007` | todo |
| AC-008 | `test_date_order_flagged_AC_008` | todo |
| AC-009 | `test_decay_window_AC_009` | todo |
| AC-010 | `test_env_override_short_circuits_AC_010` | todo |
| AC-011 | `test_git_email_handle_stable_and_opaque_AC_011` | todo |
| AC-012 | `test_distinct_identities_distinct_handles_AC_012` | todo |
| AC-013 | `test_email_author_flagged_and_agrees_with_pii_scan_AC_013` | todo |
| AC-014 | `test_store_version_changes_with_content_AC_014` | todo |
| AC-015 | `test_unsupported_yaml_raises_with_location_AC_015` | todo |

## Sequencing

T-001 gates everything — nothing can be queried, validated, or rendered until
records parse. T-002→T-004 complete the read path and are the first point at
which the store delivers value. T-005/T-006 convert the gate from
string-matching to record validation. T-007 is independent of T-001–T-006 and
can proceed in parallel. T-009/T-010 are the wiring; T-012 is the catalog sweep
the docs gates enforce.

## Follow-ups (explicitly not this spec)

- **Ingestion (the write path)** — extracting candidate records from completed
  agent workflows. Deliberately last: capturing knowledge nobody retrieves is
  the failure mode `spec.md`'s Non-Goals name. Build it once retrieval has
  demonstrably improved a workflow, so the evidence says what is worth
  capturing.
- **Approval workflow** — `status` transitions with a `reviewed_by` handle,
  routed through a second agent. This spec supplies the identity that workflow
  routes to; it does not build the workflow.
- **Organisation scale** — multi-team namespacing, contradiction detection
  between stores, and impact scoring ("what did this record earn us?").
- **`access_level` enforcement inside `query`** rather than reporting, once a
  caller exists that carries a level to enforce against (`spec.md`, Open
  Questions).
- **Structured `pit_scope`** — replacing free text with a typed field would
  retire RISK-004 rather than mitigating it, but it edits `0002`'s schema and
  every committed record, so it needs its own spec.
