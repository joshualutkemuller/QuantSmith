# Census API Profile

## Use For

- Economic, demographic, housing, business, trade, and geographic datasets from
  the U.S. Census Bureau.
- Regional macro context, housing analysis, local-market screens, and feature
  enrichment.

## Required Metadata

- `dataset`
- `variables`
- `geography`
- `period`
- `vintage`
- `release_date` when available
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Preserve geography identifiers, hierarchy, and vintage year.
- Store variable labels and concepts with the returned data.
- Keep estimates, margins of error, and annotation fields separate.
- Record the exact variables and geography predicates used in each request.

## Risks

- Geographic definitions and vintages can change over time.
- Survey estimates may require margin-of-error handling before use in models.
- Suppressed or annotated values can be misread as ordinary numeric values.
