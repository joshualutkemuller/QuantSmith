# Power BI Agent Tasks

## Data Model Review

Input: a Power BI dataset (tables, relationships, measures).

Output: a star-schema and relationship review with cardinality and filter-direction
fixes.

## DAX Review

Input: measures and calculated columns.

Output: correctness (evaluation context) and performance findings, with rewrites.

## Refresh & Security Design

Input: data sources and access requirements.

Output: a refresh/lineage plan (incremental where needed, point-in-time where
implied) and a row-level security design with credentials in the service.

## Performance Tuning

Input: a slow or oversized model.

Output: model-size, cardinality, and aggregation recommendations with expected
impact.
