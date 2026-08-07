# FRED / ALFRED API Profile

## Use For

- Macroeconomic time series from the Federal Reserve Bank of St. Louis.
- Rates, credit, inflation, labor, GDP, monetary aggregates, and regional
  economic indicators.
- ALFRED vintages when point-in-time research or backtesting requires values as
  known on a historical date.

## Required Metadata

- `series_id`
- `observation_date`
- `release_date` or provider realtime date when available
- `vintage_date` for ALFRED pulls
- `frequency`
- `units`
- `seasonal_adjustment`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Prefer ALFRED or realtime-period pulls for backtests, model validation, and
  trading research.
- Store both raw provider values and normalized numeric values.
- Capture FRED transformations explicitly; do not silently mix levels, changes,
  percent changes, and annualized rates.
- Preserve missing-value markers before converting them to nulls.
- Record the exact series ID list and request parameters used for batch pulls.

## Risks

- Latest FRED values can include revisions unavailable at the historical
  decision time.
- Frequency conversions can move information backward in time if release dates
  are not preserved.
- Series IDs can be deprecated, renamed, or replaced.
