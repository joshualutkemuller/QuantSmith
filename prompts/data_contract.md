# Prompt: Data Contract (author a checkable data contract)

Use with the Data Quality Agent to define what consumers can rely on for a dataset.

## Inputs

- Dataset name, source, and grain.
- Column schema and types.
- Point-in-time availability, publication/revision lags, and vintage rules.
- Missingness, uniqueness, and value-range expectations.
- Lineage, access constraints, and refresh schedule.

## Instructions

Fill `templates/data/data_contract.md`. Declare the grain and keys, the schema,
the point-in-time rules, and the missingness/quality rules with thresholds and a
breach action for each. Contracts are checkable — the `data-contract-check` hook
looks for schema, keys, point-in-time, and missingness sections.

## Output

A completed data contract, plus any open questions about availability timing or
quality thresholds.
