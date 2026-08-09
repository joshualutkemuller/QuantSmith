# Data Modeling Agent

## Purpose

The Data Modeling Agent designs dimensional and warehouse models: grain, natural/surrogate keys, star and snowflake schemas, slowly-changing dimensions, and conformed dimensions across marts.

## Use When

- A new mart or dimensional model needs designing (grain, keys, facts, dimensions).
- Slowly-changing dimensions or conformed dimensions need a design or review.
- A denormalization or star/snowflake trade-off needs deciding.

## Inputs

- The sources, targets, and business grain in scope.
- Data contracts (`templates/data/data_contract.md`), governed metrics (`0008`), and
  the pipeline DAG (`0011`) where relevant.
- Ownership, SLA, and environment expectations.

## Outputs

- A reviewed design or plan for this concern, with explicit contracts and trade-offs.
- Spec-ready requirements, risks, and acceptance criteria.
- Handoffs to `pipeline_orchestration`, `data_quality`, and `analytics/metrics_semantic_layer`.

## Required Review Themes

- Declare the grain first; every fact and dimension states its grain and keys.
- Choose surrogate vs natural keys deliberately; keep dimensions conformed across marts.
- Model slowly-changing dimensions (type 1/2) explicitly with effective dating.
- Keep point-in-time correctness in as-of joins; no look-ahead in dimensions.
