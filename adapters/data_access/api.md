# API Data Access Adapter

## Use For

- REST, GraphQL, RPC, webhook pull, and streaming APIs.
- Vendor, internal platform, SaaS, analytics, and operational systems that expose
  data through authenticated endpoints.
- Incremental ingestion, point-in-time pulls, status checks, and workflow
  enrichment where the source is not naturally SQL or object storage.
- Provider-specific profiles under `external_apis/` for sources whose release
  calendars, identifiers, vintages, revisions, or redistribution terms require
  more detailed handling.

## Delivery Rules

- Capture base URL, endpoint, method, request parameters, response schema, and
  API version.
- Use managed secrets and record only the credential alias, auth scheme, scopes,
  and entitlement context.
- Support dry-run validation for endpoint reachability, permissions, request
  shape, and expected response envelope.
- Make pagination, cursors, continuation tokens, rate limits, retries, and
  backoff behavior explicit.
- Preserve as-of time, source response timestamp, ingestion timestamp, and any
  provider sequence or event ID.
- Materialize replayable snapshots or checksums when downstream research,
  reporting, or model validation depends on reproducibility.
- Redact tokens, cookies, API keys, bearer headers, signed URLs, and sensitive
  request or response fields from logs and artifacts.

## Risks

- APIs can change response fields, pagination behavior, defaults, or rate limits
  without obvious downstream failures.
- Retry logic can duplicate records unless idempotency keys, event IDs, or cursor
  checkpoints are handled deliberately.
- Pulling latest-state endpoints without source timestamps can create
  point-in-time leakage.
- Vendor terms, entitlements, and redistribution rules may restrict where
  retrieved data or derived artifacts can be delivered.

## Provider Profiles

Use provider profiles when a source requires rules beyond the generic API
contract.

| Profile | Use For |
| --- | --- |
| `external_apis/fred.md` | FRED and ALFRED macroeconomic time series and vintages. |
| `external_apis/bls.md` | BLS labor, CPI, PPI, wage, productivity, and survey series. |
| `external_apis/bea.md` | BEA national, regional, industry, and international accounts. |
| `external_apis/census.md` | Census economic, demographic, housing, and trade datasets. |
| `external_apis/treasury.md` | U.S. Treasury yield curve, auction, fiscal, and debt datasets. |
| `external_apis/federal_reserve.md` | Federal Reserve board statistical releases and supervisory datasets. |
| `external_apis/ny_fed.md` | NY Fed rates, markets, surveys, and reference datasets. |
| `external_apis/sec_edgar.md` | SEC EDGAR filings, company facts, submissions, and XBRL data. |
| `external_apis/finra.md` | FINRA transparency, reference, short interest, and market regulation data. |
| `external_apis/sp_global.md` | S&P Global Market Intelligence, ratings, indices, and vendor datasets. |
