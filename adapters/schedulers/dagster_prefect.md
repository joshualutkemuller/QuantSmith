# Dagster And Prefect Scheduler Adapter

## Use For

- Asset-aware data workflows.
- Python-native orchestration.
- Stronger local development ergonomics than classic scheduler-only systems.
- Workflows that benefit from typed config and observable run state.

## Delivery Rules

- Map workflow outputs to assets, flows, or tasks with explicit metadata.
- Keep schedule configuration separate from business logic.
- Preserve owner, runbook, data contract, alert route, and environment metadata.
- Emit run cards and artifact URIs after successful materializations.
- Make retries and backfills idempotent.

## Risks

- Teams may mix orchestration semantics with modeling logic.
- Asset partitions and backfills can be misunderstood without clear as-of rules.
- Provider-specific deployment metadata should stay in adapter configuration.
