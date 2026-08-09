# Monitoring Agents

The Monitoring group keeps live pipelines, models, and infrastructure healthy after
launch, and hands a clean signal to the `alerts/*` agents. Detection lives here;
notification and routing live in `alerts/`.

## Group Workflow

```text
live pipeline / model / infra -> monitoring/* (detect) -> observations
  -> alerts/alert_policy (0020) -> alert_router -> delivery
```

## Agents

| Agent | Handles |
| --- | --- |
| `pipeline_monitoring/` | DAG status, dependencies, freshness, latency, backlogs, retries, partial writes, idempotency, and SLOs (via the `0019` run manifest). |
| `model_signal_monitoring/` | Prediction/feature drift, calibration, alpha decay, turnover/capacity, and regime change (runtime `signal_monitoring`, `0021`). |
| `infrastructure_cost_monitoring/` | Compute, memory, storage, API quota, market-data spend, and cost-per-run guardrails. |

## Standard

`instructions/monitoring.md` — coverage (metric/threshold/owner/alert/runbook/cadence),
point-in-time baselines, honest health, and emit-observations-don't-page.

## Rules

- Every production risk has a metric, threshold/baseline, owner, alert, runbook, cadence.
- Compare live vs an explicit, point-in-time reference; report degradation honestly.
- Emit observations to the alerting engine (`0020`); do not page directly or remediate.
- Runtime Python belongs under `src/quantsmith/`
  (`signal_monitoring.py`, `pipeline_observability.py`).

## Worked Examples

- `specs/0021-signal-monitoring/` — model/signal drift, calibration, decay, regime.
- `specs/0019-pipeline-observability/` — pipeline freshness, downtime, SLA, lineage.
