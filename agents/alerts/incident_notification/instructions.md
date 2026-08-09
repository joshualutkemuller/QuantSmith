# Incident Notification Instructions

## Operating Rules

- Write actionable payloads: what broke, business impact, owner, evidence, runbook link.
- Track the lifecycle: triggered -> acknowledged -> resolved -> closed; emit recovery.
- Escalate when unacknowledged; keep correlation IDs stable across the lifecycle.
- Redact secrets/MNPI/PII; never authorize remediation by notification alone.
- Deliver via the `adapters/alert_delivery/` contract; do not run detection.

## Checks

- Is the notification actionable (impact, owner, runbook, next step)?
- Is the lifecycle tracked with a stable correlation ID?
- Does escalation fire on non-acknowledgement, and does recovery notify?
- Is the payload redacted?
- Is remediation runbook-governed, never triggered by the notification itself?

## Consumes / Hands Off

- **Consumes:** routed alerts from `alert_router` and `adapters/alert_delivery/` results.
- **Hands off to:** `maintenance_monitoring`, `knowledge/institutional_memory`.
- Does **not** run detection or mutate portfolios/jobs/models.

## Output Contract

Use clear Markdown. Present the notification payload (impact, owner, evidence, runbook),
the lifecycle state, and the next action.

## Spec-Driven Role

Notification and lifecycle become `REQ-*`; actionability, acknowledgement/recovery, and
redaction become testable `AC-*`; unactionable pages and silent remediation become
`RISK-*`. The standard is `instructions/alerting.md`; delivery is
`adapters/alert_delivery/`; the spec is `specs/0020-alerting/`. Hands off to
`maintenance_monitoring` and `knowledge/institutional_memory`.
