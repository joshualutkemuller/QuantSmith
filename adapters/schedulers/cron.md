# Cron Scheduler Adapter

## Use For

- Simple local or server-based recurring jobs.
- Prototype workflows before promotion to an orchestrator.
- Lightweight internal tools with limited dependencies.

## Delivery Rules

- Store schedule definitions in source control.
- Use explicit timezone handling; do not rely on ambiguous server-local time.
- Redirect logs to a known run directory.
- Emit a run card for every execution when the workflow affects research,
  reports, alerts, or downstream decisions.
- Pair with an alert route for failures and missed runs.

## Risks

- Weak dependency management.
- Harder audit and backfill semantics than Airflow, Dagster, or Prefect.
- Server-local configuration drift.
