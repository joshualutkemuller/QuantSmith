# Data Governance Instructions

## Operating Rules

- Every dataset has an owner, a classification, and a catalog entry.
- Trace lineage source-to-consumer; keep it current as pipelines change.
- Enforce access policy and information barriers; least privilege by default.
- Keep secrets and restricted data out of the catalog metadata itself (P9).

## Checks

- Are grain, keys, contracts, and ownership explicit?
- Is point-in-time correctness preserved across joins and refreshes?
- Are secrets kept out of the repo and artifacts (P9)?
- Is the work reproducible and reviewable, not a black box?

## Consumes / Hands Off

- **Consumes:** data contracts (`templates/data/data_contract.md`), the DAG runner
  (`0011`, `src/quantsmith/pipelines/data_pipeline.py`), and governed metrics (`0008`).
- **Hands off to:** `knowledge/institutional_memory`, `secrets_management/*`, and `pipeline_observability`.
- Does **not** re-implement orchestration or redefine governed metrics.

## Output Contract

Use clear Markdown. State the design/plan, the explicit contracts, the trade-offs, and
the risks. Reference the DAG runner and data-contract template when handing off to code.

## Spec-Driven Role

The design becomes `REQ-*`; contracts, grain/keys, ownership, and point-in-time
correctness become testable `AC-*`; leakage, contract drift, and unowned data become
`RISK-*`. The standard is `instructions/pipeline_engineering.md`; the DAG runtime is
`specs/0011-data-pipeline-orchestration/`. Hands off to `knowledge/institutional_memory`, `secrets_management/*`, and `pipeline_observability`.
