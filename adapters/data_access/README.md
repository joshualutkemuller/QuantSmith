# Data Access Adapters

Data access adapters normalize how workflows reach external datasets while
keeping source-specific authentication, credentials, pagination, rate limits, and
snapshot behavior outside agent logic.

## Files

| File | Purpose |
| --- | --- |
| `adapter_contract.md` | Source-neutral data access request and response schema. |
| `sql.md` | SQL database and warehouse access profile. |
| `object_storage.md` | S3, Azure Blob, GCS, local object stores, and lakehouse files. |
| `market_data.md` | Market/vendor data access with calendars, as-of capture, and entitlements. |

## Design Rule

Data ingestion agents decide what data is required and what contract it must
meet. Data access adapters retrieve the source bytes or rows and return evidence
for lineage, permissions, and reproducibility.
