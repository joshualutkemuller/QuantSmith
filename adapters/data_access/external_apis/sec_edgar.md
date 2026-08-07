# SEC EDGAR API Profile

## Use For

- SEC company submissions, company facts, filings, XBRL data, accession records,
  and disclosure metadata.
- Fundamental research, issuer monitoring, event detection, and compliance-aware
  evidence collection.

## Required Metadata

- `cik`
- `ticker` when mapped
- `accession_number`
- `form_type`
- `filing_date`
- `accepted_at_utc`
- `period_of_report`
- `concept` or taxonomy tag when applicable
- `source_url`
- `retrieved_at_utc`

## Delivery Rules

- Send a compliant user-agent string for SEC requests.
- Preserve CIK, accession number, form type, filing date, accepted timestamp, and
  period of report.
- Keep raw filing metadata, parsed facts, and derived features as separate
  layers.
- Record ticker-to-CIK mapping source and timestamp.
- Snapshot filings or facts used in model training, reports, or alerts.

## Risks

- Filing date, accepted timestamp, and period of report have different economic
  meanings.
- Company facts can restate prior periods and require point-in-time handling.
- Ticker mappings change across corporate actions and should not be treated as
  stable identifiers.
