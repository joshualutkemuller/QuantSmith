# Maintenance & Monitoring Agent

## Purpose

The Maintenance & Monitoring Agent covers the sixth and final stage of the
development lifecycle. It keeps a live signal, model, or pipeline healthy after
launch: monitoring, drift detection, incident response, retraining decisions, and
documentation upkeep.

For quant work this is where performance decay, data drift, and regime change are
caught, and where the decision to retrain, degrade, or retire is made and recorded.

## Use When

- Something is live and needs a monitoring or health-check plan.
- Performance, data, or behavior has drifted and needs triage.
- An incident or postmortem needs structure and follow-through.
- Docs, runbooks, or model cards have gone stale relative to the running system.

## Inputs

- Live system, its metrics, and expected baselines.
- Monitoring, alerting, and logging in place.
- Recent incidents, drift signals, or performance changes.
- Retraining, decommission, and ownership policies.

## Outputs

- Monitoring and health-check plan with thresholds.
- Drift and decay triage and root-cause analysis.
- Incident writeups and postmortems with action items.
- Retrain / degrade / retire recommendation with rationale.
- Documentation and runbook updates.

## Monitoring Coverage

The agent should design coverage across four planes rather than treating a single
dashboard as monitoring:

| Plane | Representative signals |
| --- | --- |
| Data | Freshness, completeness, schema drift, distribution drift, revisions, point-in-time violations, lineage gaps. |
| Model / signal | Prediction quality, calibration, residuals, feature drift, turnover, capacity, decay, regime sensitivity. |
| Pipeline / service | DAG status, latency, retries, backlogs, partial writes, idempotency failures, dependency and SLA/SLO breaches. |
| Business / risk | P&L attribution, exposure/limit breaches, borrow or funding changes, collateral shortfalls, cost and resource budgets. |

Each metric must map to an owner, baseline, decision, runbook, and review cadence.
Detection events flow into `agents/alerts/`; the monitoring agent must not embed
email, chat, or incident-vendor logic directly.

## Planned Extensions

- `pipeline_monitoring/`: DAG, dependency, freshness, latency, retry, backfill, and
  partial-write health.
- `model_signal_monitoring/`: performance decay, calibration, feature drift,
  turnover/capacity, and regime change.
- `infrastructure_cost_monitoring/`: compute, memory, storage, API quota, market-data
  spend, and cost-per-run guardrails.
- Synthetic checks, shadow runs, canaries, and champion/challenger comparisons.
- Automatic evidence bundles for incidents and postmortems, with human-approved
  remediation and retrain/degrade/retire decisions.

## Example Requests

- "Define the monitoring thresholds and alerts for this live signal."
- "This model's performance dropped — triage drift vs regime vs data issue."
- "Write the postmortem for this data outage with follow-up actions."

## Required Review Themes

- Whether monitoring can actually detect the failure modes that matter.
- Drift, decay, and regime change vs one-off noise.
- Root cause over symptom patching.
- Retrain / degrade / retire decisions made explicitly and recorded.
- Keeping runbooks, model cards, and docs current with reality.
