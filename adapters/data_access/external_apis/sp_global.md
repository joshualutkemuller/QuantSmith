# S&P Global API Profile

## Use For

- S&P Global Market Intelligence, ratings, fundamentals, estimates, indices,
  loans, credit, commodities, economics, and private-company datasets.
- Vendor-enriched workflows for issuer research, credit/rating context, market
  data, entity mapping, and enterprise dashboards.

## Required Metadata

- `dataset`
- `endpoint`
- `entity_id` or provider security identifier
- `ticker`
- `isin`, `cusip`, or `sedol` when available
- `as_of_date`
- `effective_date` when available
- `publication_date` or vendor timestamp when available
- `entitlement_context`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Treat S&P Global as an entitlement-bound vendor source, even when the data
  resembles public fundamentals or market data.
- Preserve provider identifiers and entity mappings before converting to internal
  security master identifiers.
- Record API product, dataset, endpoint, field list, and entitlement context for
  every pull.
- Keep raw vendor payloads, normalized tables, and derived research features in
  separate layers.
- Snapshot or checksum any pull used in a model, dashboard, backtest, or report.
- Route artifact delivery through approved channels that respect redistribution
  and license restrictions.

## Risks

- Vendor identifiers can differ from internal security masters and from public
  identifiers such as ticker, CIK, ISIN, CUSIP, or SEDOL.
- Corporate actions, estimates, ratings, and fundamentals may carry effective
  dates, publication dates, and revision dates that should not be collapsed.
- Entitlements can vary by user, product, desk, region, and downstream use case.
- Some derived artifacts may still be restricted if they expose licensed source
  data too directly.
