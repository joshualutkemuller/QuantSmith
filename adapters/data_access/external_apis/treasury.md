# U.S. Treasury API Profile

## Use For

- Treasury yield curve, auction, debt, fiscal, savings bond, and public finance
  datasets.
- Rates features, funding-cost context, collateral analysis, macro dashboards,
  and market briefings.

## Required Metadata

- `dataset`
- `record_date`
- `maturity` or security term when applicable
- `cusip` when applicable
- `auction_date` when applicable
- `issue_date` when applicable
- `units`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve maturity labels and convert them to numeric tenors only in a derived
  field.
- Keep auction, issuance, outstanding debt, and yield-curve datasets separate.
- Capture filter, sort, pagination, and field-selection parameters.
- Snapshot yield curve and auction pulls used in backtests or reporting.

## Risks

- Record dates, auction dates, issue dates, and settlement dates are different
  concepts and should not be collapsed.
- Maturity labels can produce incorrect tenor ordering if sorted lexically.
- Endpoint defaults can omit fields or pagination pages unless explicitly set.
