# Microsoft Teams Alert Delivery Adapter

## Use For

- Enterprise team workflows where Teams is the approved collaboration surface.
- Operational alerts that need cards, links, and acknowledgement actions.
- Scheduled draft packs or status summaries for bank/desk channels.

## Provider Requirements

- Approved app registration, workflow, or incoming webhook.
- Team/channel routing map.
- Secret-managed tenant/client credentials when Graph APIs are used.
- Enterprise retention and data-classification policy.

## Payload Mapping

| Contract field | Teams field |
| --- | --- |
| `route` | team/channel, chat, or webhook URL |
| `title` | adaptive card title |
| `summary` | card summary |
| `body_markdown` | card body |
| `evidence` / `artifacts` | card actions or links |
| `acknowledgement_uri` | action button |
| `correlation_id` | card metadata/footer |

## Delivery Rules

- Use adaptive cards for structured alerts and plain messages for simple status.
- Keep card content concise; link to evidence bundles rather than embedding them.
- Respect enterprise route allowlists and information-barrier constraints.
- Include runbook, owner, severity, and as-of time in every operational alert.

## Result Evidence

Capture provider activity ID, route, timestamp, update capability, and redacted
payload hash.
