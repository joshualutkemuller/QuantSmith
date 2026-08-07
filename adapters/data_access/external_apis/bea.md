# BEA API Profile

## Use For

- National income and product accounts, GDP, personal income, industry accounts,
  regional accounts, international transactions, and fixed asset datasets from
  the U.S. Bureau of Economic Analysis.
- Macro features, regime analysis, economic dashboards, and briefing context.

## Required Metadata

- `dataset_name`
- `table_name`
- `line_number` or series identifier
- `period`
- `release_date`
- `revision_date` when available
- `frequency`
- `units`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve table, line, frequency, unit, and adjustment metadata in every output.
- Keep chained-dollar, current-dollar, quantity index, and percent-change values
  distinct.
- Store release and revision metadata with the observation payload.
- Snapshot requested tables used in model or report artifacts.

## Risks

- Major BEA benchmark revisions can materially rewrite history.
- Table-line joins can drift when upstream table structures change.
- Mixing annual, quarterly, and monthly estimates without an explicit calendar
  rule can introduce timing errors.
