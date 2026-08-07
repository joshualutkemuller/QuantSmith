# Alerting Agents

This group will define how QuantSmith turns validated monitoring events into
actionable notifications without coupling detection logic to a delivery vendor.
Alerting is a pipeline: evaluate a policy, enrich and deduplicate the event, route
it by severity and ownership, deliver it through one or more adapters, and track
acknowledgement or escalation.

## Planned Agents

| Agent | Handles |
| --- | --- |
| `alert_policy/` | Threshold, anomaly, composite, and absence-of-data rules; severity, suppression, cooldowns, and market-calendar awareness. |
| `alert_router/` | Ownership, deduplication, grouping, rate limits, trading-hours rules, escalation paths, and delivery-channel selection. |
| `incident_notification/` | Actionable notification payloads, acknowledgement state, escalation, recovery notices, and links to runbooks/evidence. |

Delivery channels are adapters, not agents. Initial adapters should cover email,
Slack, Microsoft Teams, PagerDuty/Opsgenie-style incident systems, SMS/push where
policy permits, generic webhooks, and ticket creation in systems such as Jira,
ServiceNow, or Linear. This keeps alert semantics consistent while allowing a team
to swap providers.

## Group Workflow

```text
monitor emits event → alert_policy → alert_router → channel adapter
  → acknowledgement / escalation → incident or recovery record
```

The monitoring agent owns detection and evidence. Alert agents own notification
policy and delivery. They must not silently mutate portfolios, rerun jobs, or
retrain models; any automated remediation requires an explicit, separately
approved runbook.

## Shared Alert Contract

Every alert should carry:

- stable event and rule identifiers, source, environment, owner, and emitted time;
- observed value, expected range/baseline, severity, confidence, and evidence;
- first-seen/last-seen times, deduplication key, cooldown, and correlation ID;
- business impact, affected dataset/model/pipeline/portfolio, and as-of timestamp;
- runbook and dashboard links plus acknowledgement and escalation state;
- redacted payloads with no credentials, MNPI, PII, or restricted position data.

## Design Principles

- Alert on decisions and failure modes, not every metric fluctuation.
- Separate detection from delivery so the same event can route to multiple channels.
- Prefer stateful lifecycle notifications: triggered, acknowledged, resolved, closed.
- Use market calendars and maintenance windows to prevent false urgency.
- Test routing and templates with synthetic events before production activation.
- Measure alert quality through precision, time-to-acknowledge, time-to-resolve,
  escalation rate, duplicate rate, and ignored-alert rate.
