# Data Engineering Agents (`data_engineering/`)

The Data Engineering group holds the specialist roles that turn raw sources into
modeled, orchestrated, contract-backed, observable data — the **Data Engineer** role.
It starts with pipeline orchestration, the node the whole chain hangs on.

## Group Workflow

These agents sit downstream of ingestion in the Data Engineer chain (see
`docs/workflows.md` → *Data Engineer*):

```text
data_ingestion/* (or sql-integration-agent) -> data_modeling (planned)
  -> data_engineering/pipeline_orchestration
  -> data-prep-agent + data_quality
  -> pipeline_observability (planned; consumes the run manifest)
```

## Agents

| Agent | Handles |
| --- | --- |
| `pipeline_orchestration/` | DAG design and execution — dependency ordering, data contracts per step, idempotent partitioned runs, retries, backfill, and a run manifest. |
| `data_modeling/` (planned) | Dimensional/warehouse modeling: grain, keys, star/snowflake schemas, slowly-changing dimensions. |
| `pipeline_observability/` (planned) | Freshness, SLAs, lineage, data-downtime detection from the run manifest. |
| `pipeline_builder/`, `pipeline_deployment/`, `data_governance/` (planned) | Compile intent into a DAG; environment promotion/rollback; catalog, lineage, and access policy. |

## Standard

`instructions/pipeline_engineering.md` — DAG, idempotency, retry/backfill, data
contracts, and observability discipline.

## Rules

- Keep each specialist narrow and inspectable.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.
- Every step declares a data contract; bad data fails the step, it does not flow
  downstream.
- Runtime Python belongs under `src/quantsmith/` (the DAG runner lives at
  `src/quantsmith/pipelines/data_pipeline.py`); agent directories describe roles,
  prompts, instructions, and tasks.

## Worked Example

`specs/0011-data-pipeline-orchestration/` — the DAG runner as a spec-driven,
test-backed runtime workflow.
