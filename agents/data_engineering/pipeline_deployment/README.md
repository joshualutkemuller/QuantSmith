# Pipeline Deployment Agent

## Purpose

The Pipeline Deployment Agent handles environment promotion for data pipelines: dry runs, canaries, rollback, state migration, and scheduler-specific deployment adapters.

## Use When

- A pipeline needs promoting from dev to staging to prod safely.
- A deployment needs a dry run, canary, and rollback plan.
- A schema/state migration needs sequencing with the deployment.

## Inputs

- The sources, targets, and business grain in scope.
- Data contracts (`templates/data/data_contract.md`), governed metrics (`0008`), and
  the pipeline DAG (`0011`) where relevant.
- Ownership, SLA, and environment expectations.

## Outputs

- A reviewed design or plan for this concern, with explicit contracts and trade-offs.
- Spec-ready requirements, risks, and acceptance criteria.
- Handoffs to `pipeline_orchestration`, `deployment_release`, and `secrets_management/*`.

## Required Review Themes

- Promote through environments with a dry run and a canary before full rollout.
- Define rollback and state-migration steps; never a one-way door.
- Bind to a scheduler via the schedulers adapter, not vendor-specific agent logic.
- Keep secrets in the platform's store; deployments never embed credentials (P9).
