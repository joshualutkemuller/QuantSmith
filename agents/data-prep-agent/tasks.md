# Data Prep Agent Tasks

## Profile Dataset

Input: a raw dataset.

Output: a profiling summary of missingness, outliers, and type drift.

## Clean & Transform

Input: the dataset and requirements.

Output: deterministically cleaned and transformed data with lineage.

## Feature Creation

Input: the transformation spec.

Output: leakage-free features with point-in-time semantics.

## Quality & Schema Emit

Input: the prepared dataset.

Output: data-quality checks and schema metadata for downstream use.
