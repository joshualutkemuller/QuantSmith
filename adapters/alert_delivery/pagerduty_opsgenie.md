# PagerDuty And Opsgenie Alert Delivery Adapter

## Use For

- High-severity production incidents.
- Escalation policies with on-call ownership.
- Acknowledgement and resolution lifecycle tracking.

## Provider Requirements

- Approved service or integration key.
- Severity mapping from QuantSmith to provider priority.
- On-call schedule and escalation policy.
- Runbook and dashboard links.

## Payload Mapping

| Contract field | Incident-management field |
| --- | --- |
| `dedupe_key` | incident deduplication key |
| `severity` | urgency/priority |
| `title` | incident title |
| `summary` / `body_markdown` | incident description |
| `evidence` / `artifacts` | links |
| `runbook_uri` | runbook link |
| `status` | trigger, acknowledge, resolve |

## Delivery Rules

- Only route `high` and `critical` alerts unless a workflow explicitly opts in.
- Require a runbook for production pages.
- Use dedupe keys so repeated events update the same incident.
- Recovery messages should resolve or annotate the original incident, not create a
  new incident.

## Result Evidence

Capture incident ID, dedupe key, escalation policy, status, timestamp, and
acknowledgement/resolution URI.
