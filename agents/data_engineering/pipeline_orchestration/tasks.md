# Pipeline Orchestration Tasks

## Design A Pipeline DAG

Input: sources, transforms, sinks, and their dependencies; the partition scheme.

Output: a DAG of steps with declared dependencies and per-step data contracts, plus
an execution plan (partitioning, idempotency, retries, backfill).

## Add A Data Contract To A Step

Input: a step and its intended output schema.

Output: a data contract (columns, types, required fields) wired so a violation fails
the step before its output is used.

## Make A Pipeline Idempotent

Input: a pipeline that duplicates or diverges on re-run.

Output: an idempotent design — completed partitions skipped, recompute deterministic —
and the state/keying strategy that guarantees it.

## Plan A Backfill

Input: a backfill window and the current pipeline state.

Output: a backfill plan that runs only the missing partitions, with the run-manifest
fields that confirm coverage and freshness.
