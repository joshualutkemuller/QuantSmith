# Spec: Data-pipeline observability

- **ID:** 0019-pipeline-observability
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> The second Data Engineer runtime node: read a pipeline's run manifest for freshness,
> downtime, SLA, and lineage. Reuses the `0011` DAG runner.

## Problem & Context

The `0011` DAG runner produces a `RunManifest` (per-(step, partition) status and
attempts) but nothing consumes it, so a data consumer cannot answer "is this table
fresh, complete, and on-SLA?" and an on-call engineer cannot see which step broke or
whether it recovered. This spec adds the observability node: it turns the run manifest
into a health read — per-step status, freshness against a watermark, data-downtime
detection, an SLA verdict, and a lineage view — without re-orchestrating anything.

## Goals

- Compute per-step health from a `RunManifest` (status counts, latest successful
  partition, attempts).
- Evaluate freshness against a watermark and flag stale steps.
- Detect data downtime (a failed partition) and report it honestly.
- Produce an SLA verdict and a lineage view from the pipeline dependencies.

## Non-Goals

- Re-running or backfilling pipelines (owned by `0011`).
- Alert delivery/notification (owned by the `alerts/*` agents and adapters).
- Metric/data-quality definition (owned by `0008` and `data_quality`).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Consume a `RunManifest` and compute per-step health: ok/failed/skipped counts, latest successful partition, and max attempts. | must |
| REQ-002 | Evaluate freshness against a watermark and flag steps whose latest successful partition is behind it. | must |
| REQ-003 | Detect data downtime — a step with a failed partition — and list the downtime steps. | must |
| REQ-004 | Produce an SLA verdict (stale, downtime, or attempts over budget = degraded) and a lineage map from the pipeline dependencies. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same manifest and watermark yield an identical report. |
| NFR-002 | Honest reporting | The status is `degraded` whenever any step is stale, in downtime, or over its attempt budget; never a false `healthy`. |
| NFR-003 | Reuse | Consumes the `0011` `RunManifest`/`Pipeline`; it does not re-orchestrate or redefine contracts. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a run manifest, when observed, then each step's ok/failed/skipped counts, latest ok partition, and max attempts are computed. | REQ-001 |
| AC-002 | Given a watermark, when a step's latest ok partition is behind it, then the step is flagged stale (and fresh otherwise). | REQ-002 |
| AC-003 | Given a manifest with a failed partition, when observed, then the step is flagged as data downtime; a clean run has none. | REQ-003 |
| AC-004 | Given a pipeline and a max-attempts SLA, when observed, then the SLA verdict reflects staleness/downtime/attempts and the lineage matches the DAG dependencies. | REQ-004, NFR-002 |
| AC-005 | Given the same manifest and watermark, when observed twice, then the reports are identical. | NFR-001 |

## Data & Dependencies

- Input: a `RunManifest` and (for lineage) a `Pipeline` from
  `pipeline_orchestration` (`0011`, `src/quantsmith/pipelines/data_pipeline.py`).
- A freshness watermark and an optional max-attempts SLA.
- Standard: `instructions/pipeline_engineering.md`.
- Agents: `data_engineering/pipeline_observability`; hands off to
  `maintenance_monitoring` and the `alerts/*` agents.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Stale data served as current. | Wrong decisions on old data. | Freshness check against an explicit watermark (AC-002). |
| RISK-002 | A silent failure hides a data gap. | Missing data unnoticed. | Downtime detection from failed partitions (AC-003). |
| RISK-003 | A false `healthy` reassures wrongly. | Undetected degradation. | SLA verdict is degraded on any breach (NFR-002 / AC-004). |
| RISK-004 | Observability drifts from orchestration. | Inconsistent state. | Reads the `0011` manifest directly; no separate re-run (NFR-003). |

## Assumptions & Open Questions

- Assumption: partitions are comparable integers (e.g. dates) and the watermark is the
  expected latest partition.
- Open question: add per-step SLA thresholds and a `pipeline-contract-check.sh` gate
  that asserts DAG ownership/schedule/retry/runbook metadata (tracked, not deferred
  silently).

## Exceptions

None.
