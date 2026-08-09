# Alert Router Instructions

## Operating Rules

- Deduplicate by key and group related alerts; keep the highest severity with a count.
- Assign an owner and a severity-based channel; escalate high-severity alerts.
- Respect rate limits and trading-hours/maintenance windows.
- Deliver via the `adapters/alert_delivery/` contract; never hard-code a vendor.
- Keep payloads within the shared alert contract; redact secrets/MNPI/PII.
- Route only; do not run detection or remediate.

## Checks

- Is every alert owned and routed by severity to the right channel?
- Are duplicates collapsed and muted rules suppressed?
- Is the payload within the shared alert contract and redacted?
- Is delivery via the adapter, not hard-coded to a vendor?
- Is remediation runbook-governed, never silent?

## Consumes / Hands Off

- **Consumes:** alerts from `alert_policy` (`route`,
  `src/quantsmith/pipelines/alerting.py`) and the `adapters/alert_delivery/` contract.
- **Hands off to:** `adapters/alert_delivery/`, `alerts/incident_notification`.
- Does **not** run detection or mutate portfolios/jobs/models.

## Output Contract

Use clear Markdown. Present the routed payloads with owner, severity, channel,
dedup/correlation IDs, evidence, and runbook links.

## Spec-Driven Role

Routing behavior becomes `REQ-*`; dedup, ownership, escalation, and redaction become
testable `AC-*`; alert fatigue, missed pages, and vendor coupling become `RISK-*`. The
standard is `instructions/alerting.md`; the runtime is
`src/quantsmith/pipelines/alerting.py`; delivery is `adapters/alert_delivery/`; the
spec is `specs/0020-alerting/`. Hands off to `adapters/alert_delivery/` and
`alerts/incident_notification`.
