# Spec: Data-pipeline orchestration

- **ID:** 0011-data-pipeline-orchestration
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> First runtime workflow for the **Data Engineer** role: a DAG runner with data
> contracts, idempotency, retries, backfill, and a run manifest.

## Problem & Context

The Data Engineer workflow (`docs/workflows.md`) routes through `data_modeling`,
`pipeline_orchestration`, and `pipeline_observability` nodes that did not exist. The
role had a partial agent set (`data_ingestion/*`, `data-prep-agent`, `data_quality`)
but no spec-backed, tested runtime, so the core data-engineering guarantees —
dependency-ordered execution, contract-validated outputs, idempotent partitioned
runs, retries, backfill, and observability — were unproven. This spec defines those
guarantees as one runnable DAG runner: the first-class artifact the Data Engineer
role was missing.

## Goals

- Build a pipeline as a DAG of steps with declared dependencies, executed in
  dependency order, rejecting cycles and missing dependencies.
- Validate each step's output against a data contract (columns, types, required).
- Run idempotently across partitions: a completed partition is skipped; a forced
  re-run reproduces the same output.
- Retry a transient step failure up to a max attempt count; record persistent
  failures instead of swallowing them.
- Backfill only the missing partitions and emit a run manifest for observability.

## Non-Goals

- A distributed scheduler, a real warehouse connector, or a cron/trigger system
  (owned by the scheduler adapters and ingestion agents; this is the deterministic
  core).
- Streaming / event-time semantics; batch partitions only in this slice.
- Data lineage graphs and a catalog (owned by a future `data_governance` node).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall build a pipeline as a DAG of steps with declared dependencies, execute in dependency order, and reject cycles and missing dependencies. | must |
| REQ-002 | The system shall validate each step's output against its data contract (columns, types, required/non-null); a violation fails the step. | must |
| REQ-003 | The system shall execute idempotently across partitions — a completed partition is skipped unless forced, and a forced re-run reproduces the same output. | must |
| REQ-004 | The system shall retry a transient step failure up to a max attempt count and record a persistent failure. | must |
| REQ-005 | The system shall backfill only the missing partitions and emit a run manifest recording per-(step, partition) status. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same pipeline and inputs yield an identical manifest and outputs on every run. |
| NFR-002 | Ordering correctness | No step runs before its dependencies; contract violations are not retried. |
| NFR-003 | Observability | Every run emits a manifest with a status for each executed (step, partition). |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a DAG, when it runs, then steps execute in dependency order and a downstream step sees upstream output; a cycle or missing dependency is rejected at construction. | REQ-001, NFR-002 |
| AC-002 | Given a step whose output violates its contract, when it runs, then the step fails with a recorded violation; valid output passes. | REQ-002 |
| AC-003 | Given a completed partition, when the pipeline reruns, then the step is skipped; when forced, it recomputes identical output. | REQ-003 |
| AC-004 | Given a step that fails transiently then succeeds, when it runs with retries, then it completes; a step that always fails is marked failed after the max attempts. | REQ-004 |
| AC-005 | Given some partitions already complete, when a backfill runs, then only missing partitions execute and the manifest lists per-partition status. | REQ-005, NFR-003 |
| AC-006 | Given the same pipeline and partitions, when it runs twice, then the manifests and outputs are identical. | NFR-001 |

## Data & Dependencies

- Step functions that read upstream outputs and a partition key and return rows.
- Data contracts declaring each output's schema.
- A pipeline state store (in-memory for the reference) tracking completed partitions.
- Agents: `data_ingestion/*`, `data-prep-agent`, `data_quality`, and the new
  `data_engineering/pipeline_orchestration`.
- Standard: `instructions/pipeline_engineering.md`; contract template
  `templates/data/data_contract.md`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | A step runs before its inputs are ready. | Corrupt or empty outputs. | Topological execution; a step with an unmet dependency does not run (AC-001). |
| RISK-002 | Bad data flows downstream unchecked. | Silent corruption of derived tables. | Contract validation fails the step before its output is used (AC-002). |
| RISK-003 | Re-runs duplicate or diverge. | Non-idempotent pipelines, double counting. | Idempotent skip + deterministic recompute (AC-003 / NFR-001). |
| RISK-004 | Transient errors marked as permanent, or permanent errors retried forever. | Flaky or stuck pipelines. | Bounded retries; contract violations are not retried (AC-004 / NFR-002). |

## Assumptions & Open Questions

- Assumption: batch partitions (e.g., dates) with independent per-partition execution.
- Assumption: step functions are deterministic given their inputs and partition.
- Open question: promote the in-memory state store to a durable backend, and add a
  freshness/SLA gate (`pipeline-contract-check.sh`) as a follow-up.

## Exceptions

None.
