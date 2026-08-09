# Alert Policy: <name>

> The alerting contract for a monitored risk. Validated by
> `hooks/stages/alert-contract-check.sh` and the standard `instructions/alerting.md`.
> Copy this next to your monitor as `<name>_alert_policy.md`.

## Rule

- **rule_id:** <stable identifier>
- **metric:** <the monitored metric>
- **kind:** max | min | missing | anomaly | composite
- **threshold / condition:** <value or expression>
- **severity:** info | warning | critical

## Ownership & Routing

- **owner / steward:** <team or person>
- **channel by severity:** <e.g. warning→slack, critical→pagerduty>
- **deduplication key:** <rule_id:metric>
- **correlation id:** <how related alerts are grouped>
- **suppression:** <cooldown, maintenance / market-calendar windows>

## Response

- **runbook / on-call:** <link; steps for this alert>
- **escalation:** <who is paged and when if unacknowledged>
- **lifecycle:** triggered → acknowledged → resolved → closed (+ recovery notice)

## Safety

- **redaction:** no secrets, credentials, MNPI, PII, or restricted position data.
- **remediation:** notification only; any automated action needs a separate runbook.
- **test route:** validate with a synthetic event / dry-run before production.

Runtime: `src/quantsmith/pipelines/alerting.py` (`AlertPolicy`, `evaluate_policies`,
`route`); delivery: `adapters/alert_delivery/`.
