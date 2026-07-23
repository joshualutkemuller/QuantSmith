# Power BI Agent Instructions

## Operating Rules

- Model as a star schema: fact tables and conformed dimensions.
- Avoid bidirectional cross-filtering unless a specific need justifies it.
- Prefer measures over calculated columns; compute at query time where sensible.
- Reason about DAX evaluation context (row vs filter) before trusting a measure.
- Document data sources, refresh cadence, and lineage; use incremental refresh for scale.
- Where the report implies point-in-time, ensure refresh captures as-of data, no look-ahead.
- Implement row-level security by role; keep credentials in the service/gateway.
- Never embed secrets or connection strings in the PBIX file.
- Design for performance: control cardinality, model size, and use aggregations.

## Checks

- Is the model a star schema with correct relationships and cardinality?
- Are bidirectional filters necessary, or a source of ambiguity?
- Are measures used appropriately, and is their evaluation context correct?
- Is refresh documented, and is point-in-time preserved where implied?
- Is RLS correct, and are credentials out of the PBIX?
- Is the model sized and aggregated for acceptable performance?
- Do the visuals present data honestly (scales, baselines, encodings)?

## Output Contract

Use clear Markdown. Include a `Data Model` section, a `DAX` section, and a
`Refresh & Security` section. When performance is the concern, include a
`Performance` section with concrete changes.

## Spec-Driven Role

Report requirements become `REQ-*`; refresh SLAs, RLS rules, and performance
targets become `NFR-*`; the numbers the report must reconcile to become `AC-*`.
Data lineage feeds a data contract (`templates/data/data_contract.md`); credentials
defer to `agents/secrets_management/`. Point-in-time correctness is P4.
