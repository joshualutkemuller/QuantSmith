# Slack Alert Delivery Adapter

## Use For

- Team-visible workflow status.
- Analyst or desk review channels.
- Incident updates that benefit from threaded discussion.
- Lightweight acknowledgements and follow-up links.

## Provider Requirements

- Workspace-approved app or bot token.
- Channel allowlist.
- User/group mapping from alert route to Slack channel, user group, or DM.
- Rate-limit and retry policy.

## Payload Mapping

| Contract field | Slack field |
| --- | --- |
| `route` | channel ID, user ID, or user group |
| `title` | message header |
| `summary` | first block |
| `body_markdown` | section blocks |
| `evidence` / `artifacts` | link blocks |
| `acknowledgement_uri` | button or link |
| `correlation_id` | metadata and footer |

## Delivery Rules

- Prefer channel messages for shared operational context and DMs only for
  explicitly routed ownership.
- Thread updates under the original message when `provider_thread_id` exists.
- Keep high-severity messages short and link to evidence/runbooks.
- Avoid posting raw tables, secrets, PII, MNPI, or restricted positions.
- Use dry-run rendering before enabling a new route.

## Result Evidence

Capture Slack channel ID, message timestamp, thread timestamp, permalink if
available, and redacted payload hash.
