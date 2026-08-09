# Pipeline Monitoring Agent

## Purpose

The Pipeline Monitoring Agent watches live data pipelines: DAG status, dependencies, freshness, latency, backlogs, retries, partial writes, idempotency, and SLOs. It reads the run manifest the DAG runner emits (via pipeline_observability, spec 0019) and emits observations for alerting.

## Use When

- A live pipeline_monitoring risk needs a monitoring metric, threshold, owner, and alert.
- Degradation needs detecting before it causes a bad decision.
- Monitoring coverage needs a review against the standard.

## Inputs

- Live vs reference measurements for the plane in scope.
- Thresholds/baselines, owner, runbook, and review cadence.
- is `pipeline_observability` (`src/quantsmith/pipelines/pipeline_observability.py`, spec `0019`).

## Outputs

- A health read with breaches and the observations the alerting engine evaluates.
- A coverage statement (metric, threshold, owner, alert, runbook, cadence).
- Handoffs to `alerts/alert_policy` and `maintenance_monitoring`.

## Required Review Themes

- Track freshness, latency, backlogs, retries, partial writes, and idempotency.
- Compare against SLOs and an explicit watermark; flag stale or failed partitions.
- Report degradation honestly; emit observations, do not page directly.
