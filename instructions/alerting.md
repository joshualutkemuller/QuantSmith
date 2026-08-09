# Alerting Standard

How QuantSmith turns validated monitoring events into actionable, routed
notifications without coupling detection to a delivery vendor. This is the standard
behind the `alerts/*` agents (`specs/0020-alerting/`), the alerting runtime
(`src/quantsmith/pipelines/alerting.py`), and the `adapters/alert_delivery/` contract.

## Why This Standard

Alerting fails in two directions: too many alerts (every fluctuation pages someone,
so real ones are ignored) or too few (a real breach is silently missed). This standard
separates detection from delivery, deduplicates and suppresses noise, and keeps a
stateful lifecycle, so alerts stay actionable and trusted.

## The Alerting Pipeline

```text
monitor emits observations -> alert_policy (evaluate) -> alert_router (route)
  -> alert_delivery adapter -> acknowledgement / escalation -> incident or recovery
```

Detection (monitoring) and delivery (adapters) are separate; the alert agents own
notification policy and routing only.

## Rules

1. **Alert on decisions and failure modes, not every fluctuation.** A policy fires on
   a threshold, an anomaly, a composite condition, or absence of data — with an
   explicit severity.
2. **Separate detection from delivery.** The same event routes to multiple channels;
   channels are adapters, never agents.
3. **Deduplicate and suppress.** Alerts sharing a dedup key collapse to one; muted
   rules, cooldowns, and maintenance/market-calendar windows drop or defer alerts.
4. **Own every alert.** Each alert has an owner and a channel chosen by severity;
   high-severity alerts escalate (page).
5. **Stateful lifecycle.** Prefer triggered → acknowledged → resolved → closed over
   fire-and-forget; emit recovery notices.
6. **Carry the shared alert contract.** Stable rule/event IDs, source, environment,
   owner, observed value vs expected, severity, evidence, dedup key, correlation ID,
   business impact, runbook/dashboard links, and acknowledgement state.
7. **Redact.** No credentials, MNPI, PII, or restricted position data in a payload.
8. **Never auto-remediate silently.** Notification alone never mutates a portfolio,
   reruns a job, or retrains a model; remediation needs a separately approved runbook.
9. **Test before production.** Route synthetic events through templates and channels
   first; measure precision, time-to-ack/resolve, escalation, and duplicate rates.

## Checklist

- [ ] Each policy has a severity and a clear condition (threshold/anomaly/composite/missing).
- [ ] Alerts deduplicate by key; muted rules and windows suppress noise.
- [ ] Every routed alert has an owner and a severity-based channel.
- [ ] High-severity alerts escalate.
- [ ] Payloads carry the shared contract and are redacted.
- [ ] No silent remediation; runbooks govern any automated action.

## Runtime & Spec

- Runtime: `src/quantsmith/pipelines/alerting.py`
  (`AlertPolicy`, `evaluate_policies`, `Routing`, `route`).
- Spec: `specs/0020-alerting/`.
- Delivery: `adapters/alert_delivery/` (email, Slack, Teams, PagerDuty/Opsgenie,
  SMS/push, webhook, ticketing).
- Detection: `agents/monitoring/*` and `instructions/monitoring.md`.
