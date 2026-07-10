# Deployment & Release Instructions

## Operating Rules

- Confirm the change passed its tests and met acceptance criteria before release.
- Scale the rollout strategy to the blast radius and reversibility.
- Require a rollback path and a kill switch for anything that trades or serves.
- Define monitoring and alert thresholds before, not after, launch.
- Name the owner and the on-call path for the change post-launch.
- Capture required approvals and compliance records.
- Do not sign off with unresolved blocking gaps; list them instead.

## Checks

- Is validation evidence present and mapped to acceptance criteria?
- Is there a concrete rollback and kill-switch plan with triggers?
- Are monitoring, alerting, and ownership defined?
- Is the rollout strategy proportional to the risk?
- Are approvals and change-management requirements satisfied?
- Are release notes and an operations handoff ready?

## Output Contract

Use clear Markdown sections. Always include a `Readiness Gaps` section and a
`Rollback Plan` section. When the release trades, serves models, or touches
regulated data, include an `Approvals & Compliance` section.
