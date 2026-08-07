# Alert Delivery Adapter Contract

## Purpose

Define the channel-neutral payload that every alert delivery adapter must accept.
This contract prevents Slack, Teams, email, PagerDuty, ticketing, and webhook
logic from leaking back into agents.

## Input

```yaml
event_id: string
workflow_id: string
run_id: string
source: string
environment: dev | staging | prod
severity: info | warning | high | critical
status: triggered | updated | acknowledged | resolved | closed
owner: string
route: string
title: string
summary: string
body_markdown: string
observed_at_utc: string
as_of_utc: string
correlation_id: string
dedupe_key: string
cooldown_seconds: integer
evidence:
  - label: string
    uri: string
artifacts:
  - label: string
    uri: string
runbook_uri: string | null
dashboard_uri: string | null
acknowledgement:
  required: boolean
  acknowledgement_uri: string | null
privacy:
  contains_pii: boolean
  contains_mnpi: boolean
  contains_restricted_positions: boolean
  redaction_level: none | standard | strict
dry_run: boolean
```

## Output

```yaml
adapter_name: string
provider: string
status: delivered | skipped | failed
provider_message_id: string | null
provider_thread_id: string | null
correlation_id: string
dedupe_key: string
timestamp_utc: string
retryable: boolean
error_code: string | null
error_message_redacted: string | null
acknowledgement_uri: string | null
evidence_uri: string | null
```

## Required Behavior

- Validate required fields before calling the provider.
- Respect `dry_run` and return the exact payload that would have been sent,
  excluding secrets.
- Apply deduplication and cooldowns before delivery when requested by
  `alert_router`.
- Preserve `correlation_id` across retries, updates, acknowledgements, and
  recovery messages.
- Redact sensitive fields according to `privacy.redaction_level`.
- Return provider IDs so the workflow can update or thread future messages.
- Never include credentials, raw tokens, or secret values in output.

## Failure Handling

Adapters classify failures as retryable or terminal.

Retryable examples:

- provider rate limit;
- temporary network failure;
- transient authentication service error;
- provider service outage.

Terminal examples:

- invalid recipient or route;
- missing required payload field;
- privacy policy violation;
- unsupported provider capability.
