# Ticketing Alert Delivery Adapter

## Use For

- Jira, ServiceNow, Linear, GitHub Issues, or similar work tracking.
- Follow-up tasks from monitoring events.
- Non-urgent remediation, review, or operational debt.
- Audit records for production issues.

## Provider Requirements

- Project/queue mapping.
- Issue type, priority, label, and assignment mapping.
- Secret-managed API credentials.
- Duplicate detection by `dedupe_key` or provider search.

## Payload Mapping

| Contract field | Ticket field |
| --- | --- |
| `route` | project, queue, or team |
| `title` | ticket summary |
| `body_markdown` | description |
| `severity` | priority |
| `owner` | assignee or owning team |
| `evidence` / `artifacts` | links |
| `runbook_uri` | runbook link |
| `correlation_id` | external ID |

## Delivery Rules

- Update an existing ticket when the same `dedupe_key` is open.
- Create a new ticket only when the event represents a new failure mode or task.
- Include reproduction steps or observed evidence when available.
- Do not attach sensitive artifacts directly unless the provider is approved for
  that data classification.

## Result Evidence

Capture ticket key/ID, URL, status, assignee, priority, and redacted payload hash.
