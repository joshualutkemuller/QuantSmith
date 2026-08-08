# Metrics Semantic Layer Tasks

## Define A Metric

Input: a business question, the fact grain, base measures, and dimensions.

Output: a canonical metric definition (name, measure/aggregation or ratio, allowed
dimensions, time grain, owner) ready for the runtime evaluator.

## Reconcile Conflicting Definitions

Input: two definitions of the same metric that disagree.

Output: one reconciled definition and a note on what changed and why the conflict is
rejected going forward.

## Add A Dimension

Input: a metric and a new dimension to slice by.

Output: the updated definition and a reconciliation check that slices sum to the
total for additive metrics.

## Governance Review

Input: a new or changed metric definition.

Output: a review covering single-source-of-truth conflicts, owner/grain presence,
declared dimensions, point-in-time period filtering, and ratio consistency.
