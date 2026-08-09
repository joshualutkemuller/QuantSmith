# Data Modeling Instructions

## Operating Rules

- Declare the grain first; every fact and dimension states its grain and keys.
- Choose surrogate vs natural keys deliberately; keep dimensions conformed across marts.
- Model slowly-changing dimensions (type 1/2) explicitly with effective dating.
- Keep point-in-time correctness in as-of joins; no look-ahead in dimensions.

## Checks

- Are grain, keys, contracts, and ownership explicit?
- Is point-in-time correctness preserved across joins and refreshes?
- Are secrets kept out of the repo and artifacts (P9)?
- Is the work reproducible and reviewable, not a black box?

## Consumes / Hands Off

- **Consumes:** data contracts (`templates/data/data_contract.md`), the DAG runner
  (`0011`, `src/quantsmith/pipelines/data_pipeline.py`), and governed metrics (`0008`).
- **Hands off to:** `pipeline_orchestration`, `data_quality`, and `analytics/metrics_semantic_layer`.
- Does **not** re-implement orchestration or redefine governed metrics.

## Output Contract

Use clear Markdown. State the design/plan, the explicit contracts, the trade-offs, and
the risks. Reference the DAG runner and data-contract template when handing off to code.

## Spec-Driven Role

The design becomes `REQ-*`; contracts, grain/keys, ownership, and point-in-time
correctness become testable `AC-*`; leakage, contract drift, and unowned data become
`RISK-*`. The standard is `instructions/pipeline_engineering.md`; the DAG runtime is
`specs/0011-data-pipeline-orchestration/`. Hands off to `pipeline_orchestration`, `data_quality`, and `analytics/metrics_semantic_layer`.
