# Alert Policy Instructions

## Operating Rules

- Define rules with an explicit condition (threshold `max`/`min`, missing, and — as
  they land — anomaly/composite) and a severity.
- Alert on decisions and failure modes, not every fluctuation.
- Give each rule a dedup key (rule + metric); suppress with cooldowns and
  market-calendar/maintenance windows.
- Treat absence of data as a first-class alert condition.
- Keep payloads within the shared alert contract; redact secrets/MNPI/PII.
- Evaluate policies via `evaluate_policies`; do not deliver — hand off to the router.

## Checks

- Does each rule have a clear condition and a justified severity?
- Is there a dedup key and a suppression story?
- Is absence-of-data covered where it matters?
- Is the expected alert rate sane (no fatigue)?
- Is the payload redacted?

## Consumes / Hands Off

- **Consumes:** observations from `pipeline_observability` (`0019`) and
  `signal_monitoring` (`0021`); the runtime `evaluate_policies`
  (`src/quantsmith/pipelines/alerting.py`).
- **Hands off to:** `alert_router`, `alerts/incident_notification`.
- Does **not** deliver notifications or remediate.

## Output Contract

Use clear Markdown. Present the policies (metric, kind, threshold, severity), the fired
alerts, expected rate, and suppression windows.

## Spec-Driven Role

A policy set becomes `REQ-*`; correct firing, severity, dedup, and redaction become
testable `AC-*`; alert fatigue and missed breaches become `RISK-*`. The standard is
`instructions/alerting.md`; the runtime is `src/quantsmith/pipelines/alerting.py`; the
spec is `specs/0020-alerting/`. Hands off to `alert_router` and
`alerts/incident_notification`.
