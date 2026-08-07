# Airflow Scheduler Adapter

## Use For

- Production DAGs with explicit dependencies.
- Backfills and catchup logic.
- Shared operational visibility.
- Data pipelines with SLAs, sensors, and retry policy.

## Delivery Rules

- Map `workflow_id` to DAG ID and `schedule_id` to DAG schedule metadata.
- Preserve task ownership, runbook, data contract, and alert route.
- Use idempotent task design for retries and backfills.
- Emit dataset, artifact, and run-card locations as XCom or metadata records.
- Avoid task-level secrets in DAG files; use approved connections or secret
  backends.

## Risks

- Catchup/backfill can create duplicate outputs without idempotency keys.
- DAG parse errors can silently block deployment.
- Airflow connection sprawl can bypass secrets-management standards.
