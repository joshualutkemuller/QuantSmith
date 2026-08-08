# Tasks: Data-pipeline orchestration

- **Spec:** 0011-data-pipeline-orchestration (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Ordering, contract validation, idempotency, and bounded retries hold.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `Pipeline` (toposort, cycle/missing-dep rejection) and ordered `run`. | REQ-001, NFR-001, NFR-002 | done | `data_engineering/pipeline_orchestration` | Kahn's algorithm, deterministic. |
| T-002 | Implement `DataContract.validate` and enforce it per step output. | REQ-002, NFR-002 | done | `data_quality` | Violations recorded; not retried. |
| T-003 | Implement idempotent partitioned execution with a state store and `force`. | REQ-003, NFR-001 | done | `data_engineering/pipeline_orchestration` | Completed partition skipped; forced recompute identical. |
| T-004 | Implement bounded retries for transient step failures. | REQ-004 | done | `data_engineering/pipeline_orchestration` | Persistent failure recorded. |
| T-005 | Implement `backfill` and the `RunManifest` observability record. | REQ-005, NFR-003 | done | `data_engineering/pipeline_orchestration` | Only missing partitions run. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only reference in
`src/quantsmith/pipelines/data_pipeline.py`. A production build wraps a real scheduler
(Airflow/Dagster/Prefect) and a durable state backend behind the same contract; the
ordering, validation, idempotency, retry, and backfill guarantees are unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_data_pipeline.py::test_topological_order_AC_001` | done |
| AC-002 | `tests/test_data_pipeline.py::test_contract_validation_AC_002` | done |
| AC-003 | `tests/test_data_pipeline.py::test_idempotency_AC_003` | done |
| AC-004 | `tests/test_data_pipeline.py::test_retries_AC_004` | done |
| AC-005 | `tests/test_data_pipeline.py::test_backfill_AC_005` | done |
| AC-006 | `tests/test_data_pipeline.py::test_deterministic_AC_006` | done |

## Follow-ups

- Promote the in-memory state store to a durable backend.
- Add `pipeline-contract-check.sh` (DAG ownership, inputs/outputs, schedule, retry/
  backfill, idempotency, runbook metadata) and a `pipeline-observability` node.
- Add `data_engineering/data_modeling`, `pipeline_builder`, `pipeline_deployment`, and
  `data_governance` agents as further Data Engineer nodes.