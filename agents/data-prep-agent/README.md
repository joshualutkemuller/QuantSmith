# Data Prep Agent

## Purpose

The Data Prep Agent cleans, profiles, and transforms analytics datasets before
dashboard or report generation. It profiles for quality issues, applies deterministic
cleaning, executes requested transformations, and emits lineage and quality checks.

## Use When

- Raw data has quality issues (missingness, outliers, type drift).
- Data needs normalization, deduplication, casting, or feature creation.
- A transformed dataset needs lineage and quality metadata before downstream use.

## Inputs

- The raw dataset and its schema.
- The cleaning and transformation requirements.
- Downstream use (dashboard, report, model) and its constraints.

## Outputs

- A profiling summary (missingness, outliers, type drift).
- Deterministic cleaning steps applied (null handling, dedup, casting).
- The requested transformations and features.
- Transformation lineage and data-quality checks.
- A validated dataset with schema metadata.

## Example Requests

- "Profile this dataset and apply deterministic cleaning with lineage."
- "Transform and feature-engineer this data for dashboard use."
- "Emit data-quality checks and schema metadata for the prepared dataset."

## Required Review Themes

- Deterministic, reproducible cleaning steps (no hidden manual edits).
- Point-in-time safety in any transformation or feature (no look-ahead).
- Missing-value handling that does not embed future information.
- Transformation lineage captured end to end.
- Data-quality checks emitted with the output.
