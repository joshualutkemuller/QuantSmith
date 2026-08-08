# Pipeline Orchestration Instructions

## Operating Rules

- Model the pipeline as a DAG: declare each step's dependencies; reject cycles and
  references to unknown steps.
- Execute in dependency order; a step whose inputs are not ready does not run.
- Give every step an output data contract (columns, types, required fields); a
  violation fails the step and is recorded, never passed downstream.
- Do not retry contract violations — bad data is not transient. Retry only transient
  failures, and bound the attempts.
- Make execution idempotent per partition: a completed partition is skipped, and a
  forced recompute is deterministic (no duplication, no drift).
- Backfill only the partitions that are missing; isolate partitions so a failure in
  one does not block the others.
- Emit a run manifest recording the status of each (step, partition) for observability
  and freshness.

## Checks

- Is the dependency graph acyclic and complete (no unknown deps)?
- Does every step have an output contract, and is it enforced before downstream use?
- Are contract violations recorded and not retried?
- Is re-running a completed partition a no-op, and is recompute deterministic?
- Are retries bounded, and are persistent failures recorded?
- Does backfill run only missing partitions, and does the manifest cover every run?

## Output Contract

Use clear Markdown. Present the DAG (steps and dependencies), the per-step contracts,
and the execution plan (partitioning, idempotency, retries, backfill). Describe the
run-manifest fields. Name the runtime symbols (`Pipeline`, `Step`, `DataContract`,
`run`, `backfill`) when handing off to code.

## Spec-Driven Role

The pipeline design becomes `REQ-*`; dependency ordering, contract validation,
idempotency, bounded retries, and backfill become testable `AC-*`; cycles, bad-data
propagation, non-idempotent re-runs, and unbounded retries become `RISK-*`. The
standard is `instructions/pipeline_engineering.md`; the runtime is
`src/quantsmith/pipelines/data_pipeline.py`; the worked spec is
`specs/0011-data-pipeline-orchestration/`. Hands off to `data-prep-agent`,
`data_quality`, and the `data_ingestion/*` agents.
