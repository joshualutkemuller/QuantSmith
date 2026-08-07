# Federal Reserve API Profile

## Use For

- Federal Reserve Board statistical releases, bank data, financial accounts,
  supervisory datasets, and policy-related series.
- Macro context, bank-sector analysis, liquidity monitoring, and research
  features.

## Required Metadata

- `release`
- `series_id` or dataset key
- `observation_date`
- `release_date`
- `revision_date` when available
- `frequency`
- `units`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve release names and series identifiers exactly as published.
- Record publication timestamps and revision markers when available.
- Keep policy, balance-sheet, banking, and flow-of-funds datasets separated by
  source release.
- Snapshot inputs used for models, dashboards, or published reports.

## Risks

- Many Federal Reserve series also appear through FRED; duplicate sources can
  disagree because of timing, transformations, or metadata.
- Release calendars and observation periods are easy to confuse.
- Some datasets have usage constraints or sensitive supervisory context.
