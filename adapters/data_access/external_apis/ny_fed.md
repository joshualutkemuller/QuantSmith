# NY Fed API Profile

## Use For

- SOFR, repo, primary dealer, Treasury market, household credit, inflation
  expectations, and survey datasets from the Federal Reserve Bank of New York.
- Funding, financing, collateral, liquidity, and macro-monitoring workflows.

## Required Metadata

- `dataset`
- `observation_date`
- `publication_date` or release timestamp
- `rate_type` or survey measure when applicable
- `tenor` when applicable
- `units`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve publication date separately from observation date.
- Keep rates, survey, dealer, and market datasets separated by dataset family.
- Record calendar conventions, holidays, and missing-publication behavior.
- Snapshot SOFR and repo-related pulls used in financing models or dashboards.

## Risks

- Funding-rate publication dates can differ from market observation dates.
- Survey datasets often carry sampling and methodology caveats.
- Time-series definitions can change after methodology updates.
