# Plan: Alerting (policy evaluation + routing)

- **Spec:** 0020-alerting (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Two pure functions — `evaluate_policies` (observations → alerts) and `route` (alerts →
routed alerts) — with the alerting discipline built in. No-false-silence holds by
construction (a breach always produces an alert), and vendor-neutrality holds because
`route` produces owner/channel-tagged payloads that the `adapters/alert_delivery/`
providers deliver — the engine never delivers or remediates. Pure Python, deterministic.

## Agent Routing

```text
monitoring (0019/0021) -> observations
  -> alerts/alert_policy [evaluate_policies] -> alerts/alert_router [route]
  -> adapters/alert_delivery -> alerts/incident_notification (lifecycle)
```

## Architecture & Components

- `Observation` — a monitored value (None when missing).
- `AlertPolicy` — `rule_id`, `metric`, `kind` (`max`/`min`/`missing`), `threshold`,
  `severity`; validates on construction.
- `Alert` — `rule_id`, `metric`, `severity`, `dedup_key`, `message`, `value`.
- `evaluate_policies(policies, observations)` — fires an alert per breach.
- `Routing` — owners (per rule), channels (per severity), suppressed rules,
  escalate-at severity, defaults.
- `route(alerts, routing)` — dedup (highest severity + count), suppress, assign
  owner/channel, escalate.

## Interfaces & Data Contracts

- Input: policies and observations; a `Routing`.
- Output: `List[Alert]` from evaluation; `List[RoutedAlert]` (owner, channel,
  escalated, count) from routing.
- Routed payloads feed the `adapters/alert_delivery/` contract; nothing is delivered
  or mutated here.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Pure functions; a breach always fires; deterministic. |
| P5 Reversibility | yes | Pure computation; nothing to roll back. |
| P6 Observability | yes | Alerts carry evidence (value, threshold, dedup, count). |
| P9 Security & data | yes | No secrets; payloads redacted. |
| P10 Honest reporting | yes | No false silence; severity/escalation reflect the breach. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `evaluate_policies` | T-001 |
| REQ-002 | `route` (dedup/suppress/assign/escalate) | T-002 |
| REQ-003 | routed payloads; no delivery/remediation | T-002 |
| REQ-004 | shared contract fields; redaction | T-001, T-002 |
| NFR-001 | deterministic functions | T-001, T-002 |
| NFR-002 | breach always fires | T-001 |
| NFR-003 | no credential-shaped content | T-001 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Split | Evaluate + route as two functions | One monolithic "alert" call | Detection and routing are distinct concerns; easier to test and reuse. |
| Delivery | Adapter contract | Deliver in the engine | Vendor-neutrality; swap channels without touching logic. |
| Dedup | Highest severity + count | Keep all | Collapsing noise is the whole point (alert fatigue). |
| Policy kinds | threshold + missing | Also anomaly/composite now | Start with the essentials; anomaly/composite are a follow-up. |

## Validation Strategy

- AC-001: assert threshold and missing breaches fire; calm inputs don't.
- AC-002: assert duplicates collapse with a count; suppressed rules drop.
- AC-003: assert owner/channel assignment and critical escalation.
- AC-004: assert no secret-shaped content in payloads.
- AC-005: evaluate + route twice; assert identical.

## Rollout, Observability & Rollback

A library consumed by the alert agents; routed payloads hand off to the delivery
adapters. Nothing to roll back; a changed policy set simply changes what fires.

## Open Questions

- Add anomaly (z-score) and composite (AND/OR) policy kinds, cooldown/market-calendar
  windows, and a stateful acknowledgement lifecycle.
