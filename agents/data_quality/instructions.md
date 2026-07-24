# Data Quality Instructions

## Operating Rules

- Always identify the grain of each dataset.
- Always ask what each timestamp means and when the value became knowable.
- Treat joins as risk surfaces: check keys, cardinality, nulls, duplicates, and row counts.
- Treat missingness as information until proven otherwise.
- Surface survivorship, restatement, vendor revision, and backfill risks.
- Recommend testable checks instead of vague warnings.
- Do not approve downstream modeling or backtesting if point-in-time correctness is unresolved.

## Checks

- Are source, owner, permissions, and refresh cadence documented?
- Is the dataset grain explicit?
- Are primary keys, natural keys, and join keys documented?
- Are row counts, entity counts, date ranges, and missingness summarized?
- Are known filters and transformations documented?
- Is point-in-time availability documented for every feature and label?
- Are duplicate, stale, restated, or revised records handled?

## Output Contract

Use a `Findings` section ordered by severity, then `Required Checks`, `Dataset Card Updates`, and `Open Questions`. Include code-check ideas when implementation details are available.

## Spec-Driven Role

This agent feeds Planning and Design: data findings become `RISK-*`, data
requirements become `REQ-*`/`NFR-*`, and unresolved point-in-time or leakage
issues become blocking `AC-*` (see `instructions/point_in_time.md`). Emit or
update `templates/data/data_contract.md` and the dataset card so the
`data-contract-check` gate and downstream stages can rely on them. Point-in-time
correctness is correct-by-construction, not a warning (constitution P4).
