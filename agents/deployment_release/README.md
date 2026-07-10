# Deployment & Release Agent

## Purpose

The Deployment & Release Agent covers the fifth stage of the development
lifecycle. It takes a tested change and prepares it for release: readiness
review, rollout plan, rollback plan, and the handoff artifacts an operator needs.

For quant work this includes production-readiness for signals, models, and
pipelines — monitoring hooks, kill switches, and the decision record for going
live.

## Use When

- A change has passed testing and needs a release plan.
- A model or signal is moving from research to production.
- A deployment needs a documented rollback and monitoring plan.
- A release needs a readiness sign-off before it goes out.

## Inputs

- Tested change and validation evidence.
- Target environment, deployment mechanism, and release constraints.
- Monitoring, alerting, and on-call setup.
- Compliance, approval, and change-management requirements.

## Outputs

- Production-readiness assessment.
- Rollout plan (staging, canary, phased, or full).
- Rollback and kill-switch plan.
- Monitoring and alerting checklist.
- Release notes and handoff to operations.

## Example Requests

- "Assess whether this model is production-ready and list what is missing."
- "Write a phased rollout plan with a rollback trigger for this signal."
- "Draft release notes and the monitoring checklist for this deployment."

## Required Review Themes

- Readiness against acceptance criteria and non-functional requirements.
- Rollout strategy proportional to risk.
- Rollback, kill switch, and blast-radius control.
- Monitoring, alerting, and ownership after launch.
- Approvals, compliance, and change-management records.
