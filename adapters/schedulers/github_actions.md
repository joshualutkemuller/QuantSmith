# GitHub Actions Scheduler Adapter

## Use For

- Repository-native scheduled workflows.
- CI-adjacent validation jobs.
- Manual dispatches with versioned parameters.
- Public or internal SDK examples.

## Delivery Rules

- Prefer `workflow_dispatch` plus `schedule` so humans can rerun the workflow.
- Pin dependency versions and record commit SHA in the run card.
- Store non-secret parameters in workflow YAML and secrets in GitHub secrets or an
  approved secret manager.
- Upload artifacts when the workflow produces reports, draft packs, or evidence.
- Route failed runs through `alert_delivery/`.

## Risks

- Scheduled workflows can drift with repository permissions.
- Long-running market-data or modeling jobs may exceed provider limits.
- Secrets and artifacts require explicit retention policy.
