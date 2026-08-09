# Alert Router Agent

## Purpose

The Alert Router Agent decides how an alert reaches a human: ownership, deduplication,
grouping, rate limits, trading-hours rules, escalation paths, and delivery-channel
selection. It renders routing via `route` (spec `0020`,
`src/quantsmith/pipelines/alerting.py`) and delivers through the
`adapters/alert_delivery/` contract.

## Use When

- Alerts from `alert_policy` need deduplicating, owning, and routing to a channel.
- Escalation paths and rate limits need defining or reviewing.
- The same event must reach multiple channels without vendor coupling.

## Inputs

- Alerts from `alert_policy` (`evaluate_policies`, spec `0020`).
- Ownership map, severity->channel map, suppression set, and escalation threshold.

## Outputs

- `RoutedAlert` payloads (owner, channel, escalated, dedup count) via `route`.
- Delivery through the `adapters/alert_delivery/` providers.
- Handoffs to `adapters/alert_delivery/` and `alerts/incident_notification`.

## Required Review Themes

- Deduplicate by key and group related alerts; keep the highest severity with a count.
- Assign an owner and a severity-based channel; escalate high-severity alerts.
- Respect rate limits and trading-hours/maintenance windows.
- Deliver via the adapter; never hard-code a vendor.
- No credentials, MNPI, PII, or restricted data in the payload.
