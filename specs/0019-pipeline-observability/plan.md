# Plan: Data-pipeline observability

- **Spec:** 0019-pipeline-observability (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

A single pure function, `observe`, that folds a `RunManifest` into per-step health and
derives freshness, downtime, an SLA verdict, and lineage. Honesty holds by construction
— the status is `degraded` whenever any breach exists — and reuse holds because it reads
the `0011` manifest directly rather than re-running anything. Pure Python, deterministic.

## Agent Routing

```text
pipeline_orchestration (0011) -> RunManifest
  -> data_engineering/pipeline_observability [observe]
  -> maintenance_monitoring / alerts/* (on degraded)
```

## Architecture & Components

- `StepHealth` — per-step: latest ok partition, ok/failed/skipped counts, max attempts,
  fresh and downtime flags.
- `ObservabilityReport` — steps, freshness breaches, downtime steps, SLA verdict +
  breaches, and a lineage map; `status()` derives healthy/degraded.
- `observe(manifest, watermark, pipeline=None, max_attempts_sla=None)` — groups results
  by step (first-seen order), computes health, and assembles the report.

## Interfaces & Data Contracts

- Input: a `RunManifest` (`0011`), a `watermark` partition, an optional `Pipeline` for
  lineage, and an optional `max_attempts_sla`.
- Output: an `ObservabilityReport`; `status()` is `healthy` or `degraded`.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Pure fold over the manifest; deterministic. |
| P5 Reversibility | yes | Read-only analysis; nothing to roll back. |
| P6 Observability | yes | This *is* the observability surface — per-step health and lineage. |
| P9 Security & data | yes | No private data, secrets, or credentials. |
| P10 Honest reporting | yes | Degraded on any staleness/downtime/attempt breach; no false healthy. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | per-step grouping + `StepHealth` | T-001 |
| REQ-002 | freshness vs watermark | T-002 |
| REQ-003 | downtime from failed partitions | T-002 |
| REQ-004 | SLA verdict + lineage | T-003 |
| REQ-005 | `_per_step` scalar-or-dict threshold resolution | T-004 |
| NFR-001 | deterministic fold | T-001 |
| NFR-002 | degraded on any breach | T-002, T-003 |
| NFR-003 | reads the `0011` manifest | T-001 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Input | The `0011` `RunManifest` | A separate metrics store | Reuse; observability tracks exactly what ran. |
| Downtime | Any failed partition | Only the latest | A gap in any partition is missing data until recovered. |
| SLA | Boolean verdict + breach list | A numeric score | A verdict plus specific breaches is actionable. |
| Freshness | Explicit watermark | Wall-clock guessing | The consumer states the expected partition; no hidden clock. |

## Validation Strategy

- AC-001: assert per-step counts, latest ok partition, and attempts.
- AC-002: assert stale vs fresh across watermarks.
- AC-003: assert downtime on a failed partition; none on a clean run.
- AC-004: assert the SLA verdict and lineage against the DAG.
- AC-005: observe twice; assert identical reports.

## Rollout, Observability & Rollback

A read-only library consumed by the observability agent and monitoring. Nothing to roll
back; it reflects whatever the latest manifest says. On `degraded`, it hands off to
`maintenance_monitoring` and the alerts agents.

## Open Questions

- Per-step SLA thresholds and a `pipeline-contract-check.sh` gate for DAG ownership,
  schedule, retry/backfill, idempotency, and runbook metadata.
