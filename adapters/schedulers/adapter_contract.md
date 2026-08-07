# Scheduler Adapter Contract

## Input

```yaml
workflow_id: string
schedule_id: string
owner: string
timezone: string
calendar: trading | business | daily | custom
trigger:
  type: cron | interval | event | manual
  expression: string
enabled: boolean
environment: dev | staging | prod
parameters:
  key: value
retry_policy:
  max_attempts: integer
  backoff_seconds: integer
  retry_on: list
backfill_policy:
  allowed: boolean
  max_lookback_days: integer
  idempotency_key_template: string
runbook_uri: string
alert_route: string
dry_run: boolean
```

## Output

```yaml
adapter_name: string
provider: string
status: scheduled | updated | disabled | skipped | failed
provider_schedule_id: string | null
next_run_utc: string | null
correlation_id: string
timestamp_utc: string
retryable: boolean
error_code: string | null
error_message_redacted: string | null
evidence_uri: string | null
```

## Required Behavior

- Convert schedule definitions using the declared timezone and calendar.
- Preserve owner, runbook, alert route, and environment metadata.
- Require idempotency metadata when backfills are allowed.
- Support dry-run validation before provider deployment.
- Return provider schedule IDs and next-run evidence.
