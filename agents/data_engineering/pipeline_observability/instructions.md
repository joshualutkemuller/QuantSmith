# Pipeline Observability Instructions

## Operating Rules

- Read the `RunManifest` from the DAG runner (`0011`); do not re-orchestrate.
- Evaluate freshness against an explicit watermark; a step behind it is stale.
- Treat a failed partition as data downtime until a later run recovers it.
- Report a degraded SLA whenever any step is stale, in downtime, or over its attempt
  budget; never report healthy to be reassuring.
- Trace lineage from the pipeline's real dependencies.
- Emit specific, actionable breaches — which step, which partition, which threshold.

## Checks

- Is every step's latest successful partition at or beyond the watermark?
- Does any step have a failed (unrecovered) partition?
- Did any step exceed its max-attempts SLA?
- Does the lineage match the DAG dependencies?
- Is the overall status honest (degraded when any breach exists)?

## Consumes / Hands Off

- **Consumes:** the `RunManifest` and `Pipeline` from `pipeline_orchestration`
  (`0011`, `src/quantsmith/pipelines/data_pipeline.py`), via `observe`
  (`src/quantsmith/pipelines/pipeline_observability.py`).
- **Hands off to:** `maintenance_monitoring`, the `alerts/*` agents, and
  `pipeline_orchestration` (for re-run/backfill).
- Does **not** re-run pipelines or redefine data contracts.

## Output Contract

Use clear Markdown. Present the per-step health table (status counts, latest ok
partition, attempts, fresh/downtime), then `Freshness`, `Data Downtime`, `SLA`, and
`Lineage` sections. Name `observe` / `ObservabilityReport` when handing off to code.

## Spec-Driven Role

The observability requirement becomes `REQ-*`; freshness, downtime detection, the SLA
verdict, and lineage become testable `AC-*`; stale data, unrecovered downtime, and
false-healthy reporting become `RISK-*`. The runtime is
`src/quantsmith/pipelines/pipeline_observability.py`; the spec is
`specs/0019-pipeline-observability/`; the standard is
`instructions/pipeline_engineering.md`. Hands off to `maintenance_monitoring` and the
alerts agents.
