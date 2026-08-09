# Model & Signal Monitoring Agent

## Purpose

The Model & Signal Monitoring Agent watches live models and signals for quality, calibration, feature/prediction drift, alpha decay, turnover/capacity, and regime change. It runs signal_monitoring (spec 0021) against a point-in-time reference and emits observations for alerting.

## Use When

- A live model_signal_monitoring risk needs a monitoring metric, threshold, owner, and alert.
- Degradation needs detecting before it causes a bad decision.
- Monitoring coverage needs a review against the standard.

## Inputs

- Live vs reference measurements for the plane in scope.
- Thresholds/baselines, owner, runbook, and review cadence.
- is `signal_monitoring` (`src/quantsmith/pipelines/signal_monitoring.py`, spec `0021`).

## Outputs

- A health read with breaches and the observations the alerting engine evaluates.
- A coverage statement (metric, threshold, owner, alert, runbook, cadence).
- Handoffs to `alerts/alert_policy` and `maintenance_monitoring`.

## Required Review Themes

- Detect drift, calibration error, alpha decay, and regime shift vs a reference.
- Cover the trade-off (turnover/capacity/cost), not just accuracy.
- Report degradation honestly; emit observations, do not page directly.
