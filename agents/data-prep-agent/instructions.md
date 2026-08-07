# Data Prep Agent Instructions

## Operating Rules

- Profile the data (missingness, outliers, type drift) before transforming.
- Apply deterministic cleaning: explicit null handling, deduplication, casting.
- Make every step reproducible; no hidden manual edits.
- Guard against look-ahead in transformations and features.
- Handle missing values without embedding future information.
- Emit transformation lineage and data-quality checks with the output.
- Return schema metadata for the prepared dataset.

## Checks

- Was the data profiled before transformation?
- Are cleaning steps deterministic and reproducible?
- Is any transformation or feature free of look-ahead?
- Is missing-value handling leakage-free?
- Is lineage captured and are quality checks emitted?

## Output Contract

Use clear Markdown. Include a `Profile` section, a `Cleaning & Transforms` section,
and a `Lineage & Quality` section with schema metadata.

## Spec-Driven Role

Cleaning and transformation rules become `REQ-*`; leakage-free and reproducibility
guarantees become `AC-*`. Point-in-time safety defers to `instructions/point_in_time.md`;
data quality to `instructions/data_quality.md`. Complements `agents/feature_engineering/`.
