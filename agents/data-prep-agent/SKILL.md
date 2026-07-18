---
name: data-prep-agent
description: Clean, profile, and transform analytics datasets before dashboard/report generation. Use when raw data has quality issues, requires normalization, or needs feature engineering.
---

# Data Prep Agent Skill

1. Profile incoming data for missingness, outliers, and type drift.
2. Apply deterministic cleaning steps (null handling, deduplication, casting).
3. Execute requested transformations and feature creation.
4. Emit transformation lineage and data quality checks.
5. Return a validated dataset with schema metadata.
