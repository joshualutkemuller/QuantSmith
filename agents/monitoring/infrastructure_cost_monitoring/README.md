# Infrastructure & Cost Monitoring Agent

## Purpose

The Infrastructure & Cost Monitoring Agent watches compute, memory, storage, API quota, market-data spend, and cost-per-run, with guardrails so a workflow does not silently blow its budget. It declares metrics and thresholds and emits observations for alerting.

## Use When

- A live infrastructure_cost_monitoring risk needs a monitoring metric, threshold, owner, and alert.
- Degradation needs detecting before it causes a bad decision.
- Monitoring coverage needs a review against the standard.

## Inputs

- Live vs reference measurements for the plane in scope.
- Thresholds/baselines, owner, runbook, and review cadence.
- declares cost/usage metrics and thresholds (a dedicated runtime is a follow-up).

## Outputs

- A health read with breaches and the observations the alerting engine evaluates.
- A coverage statement (metric, threshold, owner, alert, runbook, cadence).
- Handoffs to `alerts/alert_policy` and `maintenance_monitoring`.

## Required Review Themes

- Track compute/memory/storage, API quota, market-data spend, and cost-per-run.
- Set budget guardrails with thresholds and owners; flag creep early.
- Report overage honestly; emit observations, do not page directly.
