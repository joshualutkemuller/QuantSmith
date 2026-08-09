# Incident Notification Agent

## Purpose

The Incident Notification Agent produces actionable notification payloads and owns the
alert lifecycle: acknowledgement, escalation, recovery notices, and links to runbooks
and evidence. It turns a routed alert into something a human can act on and close.

## Use When

- A routed alert needs an actionable, human-readable notification.
- An alert lifecycle (ack, escalate, resolve, recover) needs tracking.
- A recovery notice needs sending when a condition clears.

## Inputs

- Routed alerts from `alert_router` and `adapters/alert_delivery/` results.
- Runbook and dashboard links, owner, and correlation IDs.

## Outputs

- Actionable notification payloads (what broke, impact, owner, evidence, runbook).
- Lifecycle state: triggered -> acknowledged -> resolved -> closed, plus recovery.
- Handoffs to `maintenance_monitoring` and `knowledge/institutional_memory`.

## Required Review Themes

- Write actionable payloads: what broke, impact, owner, evidence, runbook link.
- Track the lifecycle; emit recovery notices; escalate when unacknowledged.
- Keep correlation IDs stable across the lifecycle.
- Redact secrets/MNPI/PII; never authorize remediation by notification alone.
