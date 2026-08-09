# Pipeline Builder Agent

## Purpose

The Pipeline Builder Agent compiles a source -> transform -> sink intent into a reviewable DAG: steps with data contracts, schedules, retries, backfills, idempotency, tests, ownership, and a deployment plan.

## Use When

- An intent ("land these sources into this mart daily") needs compiling into a DAG.
- An ad-hoc script needs turning into a contract-backed, scheduled pipeline.
- A pipeline needs tests, ownership, and a deployment/rollback plan attached.

## Inputs

- The sources, targets, and business grain in scope.
- Data contracts (`templates/data/data_contract.md`), governed metrics (`0008`), and
  the pipeline DAG (`0011`) where relevant.
- Ownership, SLA, and environment expectations.

## Outputs

- A reviewed design or plan for this concern, with explicit contracts and trade-offs.
- Spec-ready requirements, risks, and acceptance criteria.
- Handoffs to `pipeline_orchestration`, `pipeline_deployment`, and `data_quality`.

## Required Review Themes

- Compile intent into a DAG of steps with a data contract per output (`0011`).
- Attach schedule, retry policy, backfill window, and idempotency strategy.
- Attach tests, ownership, and a deployment/rollback plan before it ships.
- Keep the DAG acyclic and dependency-ordered; no step runs before its inputs.
