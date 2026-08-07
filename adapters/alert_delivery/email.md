# Email Alert Delivery Adapter

## Use For

- Nightly draft packs and scheduled reports.
- Low-to-medium urgency operational alerts.
- Evidence bundles that need attachments or durable forwarding.
- Stakeholder summaries where a threaded chat message would be too ephemeral.

## Provider Requirements

- Approved sender identity.
- Recipient allowlist or group routing.
- Secret-managed SMTP, Microsoft Graph, Gmail, or enterprise mail credentials.
- Attachment size policy.
- Optional archive mailbox for audit.

## Payload Mapping

| Contract field | Email field |
| --- | --- |
| `route` | `to`, `cc`, or distribution group |
| `title` | subject |
| `summary` | preview line |
| `body_markdown` | HTML/plaintext body |
| `evidence` | body links |
| `artifacts` | body links or attachments |
| `correlation_id` | message header and footer |

## Delivery Rules

- Default to links over attachments for large or sensitive artifacts.
- Include severity, owner, as-of time, and runbook link near the top.
- For scheduled content packs, use a stable subject prefix such as
  `[QuantSmith Draft Pack]`.
- For alerts, include the lifecycle state: triggered, updated, resolved, or closed.
- Do not send emails containing restricted position data unless the workflow
  explicitly permits it and the recipient route is approved.

## Result Evidence

Capture provider message ID, recipient group, timestamp, attachment/link list, and
redacted send status.
