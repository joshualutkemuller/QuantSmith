# FINRA API Profile

## Use For

- FINRA transparency, reference, short interest, OTC, TRACE, market regulation,
  and member-related public datasets.
- Market microstructure, liquidity, short-interest, fixed-income transparency,
  and surveillance-adjacent research.

## Required Metadata

- `dataset`
- `symbol` or security identifier
- `cusip` when applicable
- `trade_date` or settlement date when applicable
- `publication_date` when available
- `source_file` or endpoint
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve publication date and trade or settlement date separately.
- Record security identifier type and mapping source.
- Keep public transparency data separate from restricted or entitlement-bound
  datasets.
- Snapshot inputs used in market microstructure features or research artifacts.

## Risks

- FINRA datasets can have delayed publication, corrections, or file-level
  revisions.
- Identifier coverage can differ by asset class and venue.
- Redistribution and usage rules vary by dataset.
