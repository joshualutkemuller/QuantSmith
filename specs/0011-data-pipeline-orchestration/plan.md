# Plan: Data-pipeline orchestration

- **Spec:** 0011-data-pipeline-orchestration (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Implement a small, deterministic DAG runner. Ordering correctness holds *by
construction* (topological sort at pipeline construction, cycles and missing
dependencies rejected there), data safety holds by construction (each output is
validated against its contract before any downstream step consumes it), and
idempotency holds by construction (a completed `(step, partition)` in the state store
is skipped, and recomputation is deterministic). Pure Python so the reference runs
anywhere.

## Agent Routing

The workflow is the Data Engineer chain (see `docs/workflows.md` → *Data Engineer*):

```text
data_ingestion/* (or sql-integration-agent)   # source rows per partition
  -> data_engineering/pipeline_orchestration    # DAG: order, contracts, retries, backfill
  -> data-prep-agent + data_quality             # step logic and contract review
  -> (manifest) pipeline observability           # per-(step, partition) status & freshness
```

## Architecture & Components

- `DataContract(name, columns, required)` + `validate(rows)` → list of violations.
- `Step(name, fn, deps, contract, max_attempts)` — a unit of work; `fn(inputs,
  partition)` returns rows.
- `Pipeline(steps)` — validates dependencies and topologically orders them
  (Kahn's algorithm, deterministic); rejects cycles.
- `run(pipeline, partitions, state, force)` — executes per partition in order, with
  contract validation, retries, and idempotent skips; updates `state`.
- `backfill(pipeline, partitions, state)` — runs only incomplete partitions.
- `RunManifest` / `StepResult` — the observability record.

## Interfaces & Data Contracts

- Input: a `Pipeline`, a list of partitions, and an optional `state` store.
- A step function receives `{dep_name: rows}` and the partition, and returns rows.
- Output: a `RunManifest` of `StepResult`s (`ok` / `failed` / `skipped`), with
  violations recorded on failure; `state` carries completed partitions forward.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Topological order, contract validation before use, deterministic recompute. |
| P5 Reversibility | yes | Re-run or backfill regenerates outputs; state is the record. |
| P6 Observability | yes | Run manifest records per-(step, partition) status and attempts. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | Persistent failures and contract violations are recorded, not swallowed. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `Pipeline._toposort` + `run` ordering | T-001 |
| REQ-002 | `DataContract.validate` in `_run_step` | T-002 |
| REQ-003 | idempotent skip + deterministic recompute in `run` | T-003 |
| REQ-004 | retry loop in `_run_step` | T-004 |
| REQ-005 | `backfill` + `RunManifest` | T-005 |
| NFR-001 | pure, deterministic functions | T-001 |
| NFR-002 | toposort + no-retry on contract violation | T-001, T-002 |
| NFR-003 | `RunManifest` per-(step, partition) status | T-005 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Scheduling | In-process topological run | External scheduler (Airflow/Dagster) | Keeps the reference dependency-free and testable; adapters wrap real schedulers later. |
| Retry scope | Transient errors only | Retry contract violations too | Bad data is not transient; retrying it hides a defect (NFR-002). |
| Failure handling | Stop the partition's downstream, continue other partitions | Fail the whole run | Partition isolation lets good partitions complete; the manifest shows the failure. |
| State | In-memory store | Durable backend | Simplest correct reference; a durable backend is a follow-up. |

## Validation Strategy

- AC-001: assert downstream sees upstream output; assert cycles/missing deps raise.
- AC-002: assert null-required and wrong-type outputs fail with recorded violations.
- AC-003: assert a completed partition is skipped; a forced re-run is identical.
- AC-004: assert a flaky step completes with retries; an always-failing one is failed.
- AC-005: assert backfill runs only missing partitions; manifest lists statuses.
- AC-006: assert two runs give identical manifests and outputs.

## Rollout, Observability & Rollback

A library the ingestion and prep agents call. Rollout adds or changes a step;
rollback re-points to the prior pipeline definition and re-runs. The run manifest is
the observability surface — per-(step, partition) status feeds a future freshness/SLA
gate.

## Open Questions

- Promote the in-memory state store to a durable backend.
- Add a `pipeline-contract-check.sh` gate for DAG ownership, freshness, and idempotency
  metadata, and a `pipeline-observability` node consuming the manifest.
