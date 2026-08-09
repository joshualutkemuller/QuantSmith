# Alert Policy Agent

## Purpose

The Alert Policy Agent decides *when* to alert. It defines threshold, anomaly,
composite, and absence-of-data rules with an explicit severity, and evaluates them
against monitoring observations into alerts — alerting on decisions and failure modes,
not every metric fluctuation. It renders policies via `evaluate_policies` (spec `0020`,
`src/quantsmith/pipelines/alerting.py`).

## Use When

- A monitored metric needs an alert rule with a severity.
- Alert noise needs cutting with better thresholds, suppression, or cooldowns.
- A missing-data (absence) condition needs a rule.

## Inputs

- Monitoring observations (from `0019`/`0021`) and the metric to guard.
- The condition (threshold `max`/`min`, missing), severity, and any suppression window.

## Outputs

- `AlertPolicy` definitions and the alerts they fire (`evaluate_policies`).
- A rationale for the threshold/severity and the expected alert rate.
- Handoffs to `alert_router` and `alerts/incident_notification`.

## Required Review Themes

- Alert on decisions and failure modes, not every fluctuation.
- Explicit severity; a dedup key per rule/metric.
- Absence-of-data is a first-class condition.
- Market-calendar/maintenance windows suppress false urgency.
- No credentials, MNPI, PII, or restricted data in the alert payload.
