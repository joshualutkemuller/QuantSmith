# Monitoring Standard

How QuantSmith keeps live pipelines, models, and infrastructure healthy after launch —
detecting drift, decay, downtime, and cost problems, and emitting the observations that
alerting acts on. This is the standard behind the `monitoring/*` agents
(`specs/0021-signal-monitoring/`), the monitoring runtime
(`src/quantsmith/pipelines/signal_monitoring.py`), the pipeline-observability runtime
(`0019`), and `agents/maintenance_monitoring/`.

## Why This Standard

A model or pipeline that was correct at launch degrades: data drifts, alpha decays,
regimes change, pipelines go stale, costs creep. Monitoring makes degradation visible
*before* it causes a bad decision, and hands a clean signal to alerting rather than
paging on raw noise.

## Coverage — every production risk is monitored

For each live risk, declare: a **metric**, a **threshold/baseline**, an **owner**, an
**alert**, a **runbook**, and a **review cadence**. The planes to cover:

| Plane | What to monitor | Runtime |
| --- | --- | --- |
| Pipeline / data | Freshness, SLAs, lineage, downtime, retries, backlogs, partial writes | `pipeline_observability` (`0019`) |
| Model / signal | Prediction/feature drift, calibration, alpha decay, turnover/capacity, regime change | `signal_monitoring` (`0021`) |
| Infrastructure / cost | Compute, memory, storage, API quota, market-data spend, cost-per-run | (declare metric + threshold) |

## Rules

1. **Baseline first.** Every check compares live behavior to an explicit reference
   (a training window, a prior period, a budget); no reference, no drift.
2. **Point-in-time.** Compare like-for-like windows; no look-ahead in the reference.
3. **Honest health.** A check over its threshold makes the subject *degraded*; never
   report healthy to be reassuring.
4. **Emit observations, don't page directly.** Monitoring produces measured values;
   alerting (`0020`) decides severity, dedup, and routing.
5. **Cover the trade-off, not just accuracy.** Turnover, capacity, and cost sit
   alongside quality — a "healthy" model that is uneconomic is not healthy.
6. **Every risk has an owner, a runbook, and a cadence.** Monitoring without an owner
   and a documented response is theatre.

## Checklist

- [ ] Each production risk has a metric, threshold/baseline, owner, alert, runbook, cadence.
- [ ] Checks compare live vs an explicit, point-in-time reference.
- [ ] Degradation is reported honestly (no false healthy).
- [ ] Monitoring emits observations to the alerting engine; it does not page directly.
- [ ] The cost/turnover/capacity plane is covered, not just accuracy.

## Runtime & Spec

- Runtimes: `src/quantsmith/pipelines/signal_monitoring.py` (`monitor_signal`,
  `SignalHealth`) and `src/quantsmith/pipelines/pipeline_observability.py` (`observe`).
- Specs: `specs/0021-signal-monitoring/`, `specs/0019-pipeline-observability/`.
- Hands off to: `instructions/alerting.md` and the `alerts/*` agents.
