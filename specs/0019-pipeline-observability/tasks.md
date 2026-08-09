# Tasks: Data-pipeline observability

- **Spec:** 0019-pipeline-observability (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; tests exist and pass deterministically.
- Reads the `0011` `RunManifest`; does not re-orchestrate.
- Reports degraded on any staleness/downtime/attempt breach (no false healthy).
- No secrets or private data; runtime code lives under `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement per-step health from the manifest (`StepHealth`, grouping). | REQ-001, NFR-001, NFR-003 | done | `pipeline_observability` | Counts, latest ok partition, attempts. |
| T-002 | Implement freshness (vs watermark) and downtime detection. | REQ-002, REQ-003, NFR-002 | done | `pipeline_observability` | Stale and downtime flags + breaches. |
| T-003 | Implement the SLA verdict and lineage from the pipeline. | REQ-004, NFR-002 | done | `pipeline_observability` | `healthy`/`degraded` + lineage map. |
| T-004 | Accept per-step watermarks and attempt SLAs (`_per_step`). | REQ-005 | done | `pipeline_observability` | Scalar or `{step: value}` dict. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtime: `src/quantsmith/pipelines/pipeline_observability.py` (`observe`,
`ObservabilityReport`, `StepHealth`). Consumes the `0011` DAG runner's `RunManifest`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_pipeline_observability.py::test_step_health_AC_001` | done |
| AC-002 | `tests/test_pipeline_observability.py::test_freshness_AC_002` | done |
| AC-003 | `tests/test_pipeline_observability.py::test_downtime_AC_003` | done |
| AC-004 | `tests/test_pipeline_observability.py::test_sla_and_lineage_AC_004` | done |
| AC-005 | `tests/test_pipeline_observability.py::test_deterministic_AC_005` | done |
| AC-006 | `tests/test_pipeline_observability.py::test_per_step_thresholds_AC_006` | done |

## Follow-ups

- Per-step SLA thresholds — **done** (`observe` accepts scalar or per-step dicts).
- `pipeline-contract-check.sh` gate — **done** (validates a pipeline manifest against
  `templates/data/pipeline_manifest.md`; enforced in CI, skips when absent).
- The other Data Engineer nodes (`data_modeling`, `pipeline_builder`,
  `pipeline_deployment`, `data_governance`) are design/review agents; add executable
  runtimes only when a concrete workflow needs one.
