# Infrastructure & Cost Monitoring Instructions

## Operating Rules

- Track compute/memory/storage, API quota, market-data spend, and cost-per-run.
- Set budget guardrails with thresholds and owners; flag creep early.
- Report overage honestly; emit observations, do not page directly.

## Checks

- Does every monitored risk have a metric, threshold/baseline, owner, alert, runbook,
  and cadence?
- Is the comparison point-in-time (no look-ahead in the reference)?
- Is degradation reported honestly (no false healthy)?
- Are observations emitted to the alerting engine rather than paging directly?

## Consumes / Hands Off

- **Consumes:** live vs reference measurements; the runtime declares cost/usage metrics and thresholds (a dedicated runtime is a follow-up).
- **Hands off to:** `alerts/alert_policy` (`0020`), `maintenance_monitoring`.
- Does **not** page directly, route, or remediate.

## Output Contract

Use clear Markdown. Present the health read (measured values, breaches), the emitted
observations, and the coverage statement.

## Spec-Driven Role

Monitoring coverage becomes `REQ-*`; correct detection, honest health, and
observation emission become testable `AC-*`; missed degradation and false healthy
become `RISK-*`. The standard is `instructions/monitoring.md`; the alerting standard
is `instructions/alerting.md`. Hands off to `alerts/alert_policy` and
`maintenance_monitoring`.
