# Alert Router Tasks

## Route Alerts

Input: alerts from `alert_policy`.

Output: `RoutedAlert` payloads with owner, severity, channel, and dedup count (`route`).

## Review A Routing Flow

Input: an existing alert routing setup.

Output: a review of ownership, dedup, escalation, rate limits, and redaction, with fixes.

## Define Escalation

Input: a high-severity alert.

Output: the escalation path and channel, and the acknowledgement handoff.

## Test With Synthetic Events

Input: synthetic alerts.

Output: confirmation that routing and channel selection work before production.
