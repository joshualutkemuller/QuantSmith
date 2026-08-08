# Tasks: Metrics semantic layer

- **Spec:** 0008-metrics-semantic-layer (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Governance holds: single definition per metric, declared dimensions only,
  point-in-time period filtering.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `SemanticLayer.register`/`define` with single-source-of-truth conflict rejection. | REQ-001 | done | `metrics_semantic_layer` | Idempotent for identical definitions. |
| T-002 | Implement `compute` (period filter, declared-dimension slicing, deterministic aggregation). | REQ-002, NFR-001, NFR-002, NFR-003 | done | `metrics_semantic_layer` | Additive slices reconcile to the total. |
| T-003 | Implement ratio metrics over the same filtered rows. | REQ-003 | done | `metrics_semantic_layer` | Div-by-zero returns NaN. |
| T-004 | Implement `_validate` and `GovernanceError` paths (undefined metric, undeclared dimension, missing owner/grain). | REQ-004 | done | `quality-guard-agent` | Errors name the offending metric/dimension. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only reference in
`src/quantsmith/pipelines/metrics_semantic_layer.py`. A production build may load
definitions from a versioned YAML registry and connect to a warehouse; the
governance contract stays the same.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_metrics_semantic_layer.py::test_conflicting_definition_rejected_AC_001` | done |
| AC-002 | `tests/test_metrics_semantic_layer.py::test_period_filter_is_point_in_time_AC_002` | done |
| AC-003 | `tests/test_metrics_semantic_layer.py::test_dimension_slices_reconcile_AC_003` | done |
| AC-004 | `tests/test_metrics_semantic_layer.py::test_ratio_metric_consistent_AC_004` | done |
| AC-005 | `tests/test_metrics_semantic_layer.py::test_undefined_metric_rejected_AC_005` | done |
| AC-006 | `tests/test_metrics_semantic_layer.py::test_computation_reproducible_AC_006` | done |

## Follow-ups

- Decide whether definitions move to a versioned YAML registry loaded at startup.
- Add non-additive measures (distinct count, percentile) with reconciliation
  semantics.
- Add the `experimentation` analytics agent (A/B testing, power analysis) as the
  next Data Analyst node.