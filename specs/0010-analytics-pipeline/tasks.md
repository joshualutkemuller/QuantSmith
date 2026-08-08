# Tasks: End-to-end analytics pipeline

- **Spec:** 0010-analytics-pipeline (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Metrics flow only through the `0008` semantic layer; blocked reports return `None`.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `run_pipeline` composing query → prepare → profile → metric → guard → report. | REQ-001, NFR-001 | done | `orchestrator-agent` | Deterministic end-to-end path. |
| T-002 | Implement `run_query` + `prepare` (dedup, type, profile) and `profile_facts`. | REQ-002 | done | `sql-integration-agent` / `data-prep-agent` / `eda-specialist-agent` | Profiles counts and missingness. |
| T-003 | Compute metrics via the `0008` `SemanticLayer` (period filter, group_by). | REQ-003, NFR-002, NFR-003 | done | `analytics/metrics_semantic_layer` | No ad-hoc recomputation. |
| T-004 | Implement the quality guard (empty result, ungoverned metric, reconciliation). | REQ-004, NFR-003 | done | `quality-guard-agent` | Blocks with findings. |
| T-005 | Attach provenance to the `Report` artifact. | REQ-005 | done | `reporting-agent` | Source, period, counts, definition. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only reference in
`src/quantsmith/pipelines/analytics_pipeline.py` that reuses the `0008` semantic
layer. A production build swaps `run_query`/`prepare` for a warehouse connector and a
prep engine; the composition and governance contract are unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_analytics_pipeline.py::test_pipeline_end_to_end_AC_001` | done |
| AC-002 | `tests/test_analytics_pipeline.py::test_preparation_dedups_and_profiles_AC_002` | done |
| AC-003 | `tests/test_analytics_pipeline.py::test_report_matches_semantic_layer_AC_003` | done |
| AC-004 | `tests/test_analytics_pipeline.py::test_quality_guard_blocks_AC_004` | done |
| AC-005 | `tests/test_analytics_pipeline.py::test_report_provenance_AC_005` | done |
| AC-006 | `tests/test_analytics_pipeline.py::test_pipeline_reproducible_AC_006` | done |

## Follow-ups

- Optionally render the report to a Tableau/Power BI payload via the dashboard agents.
- Add near-duplicate resolution and richer data-quality checks in `prepare`.
- Wire the `0009-experimentation` readout as an alternate report type for A/B questions.