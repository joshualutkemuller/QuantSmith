# Metrics Semantic Layer Agent

## Purpose

The Metrics Semantic Layer Agent owns the canonical definitions of an
organization's metrics — the single source of truth for what "revenue",
"conversion rate", "active users", or any KPI means. It defines each metric once
(measure, allowed dimensions, time grain, owner), reviews new and changed
definitions for consistency and point-in-time correctness, and hands governed
definitions to dashboards and reports so the same question returns the same number
everywhere.

## Use When

- A KPI needs a canonical, agreed definition before it appears on a dashboard.
- Two dashboards or reports disagree on the same metric and the definition must be
  reconciled.
- A derived (ratio) metric needs defining so its numerator and denominator stay
  consistent.
- A metric change needs a governance review (owner, grain, allowed dimensions).

## Inputs

- The business question and the metric(s) it needs.
- The available fact grain, dimensions, and base measures (from
  `sql-integration-agent` / `data-prep-agent`).
- Any existing or conflicting definitions to reconcile.
- The metric owner and the required time grain.

## Outputs

- A canonical metric definition (name, measure/aggregation or ratio, allowed
  dimensions, time grain, owner).
- A governance review: single-source-of-truth conflicts, undeclared dimensions,
  point-in-time/period-boundary risks, and additive-reconciliation notes.
- The definition wired for the runtime evaluator
  (`src/quantsmith/pipelines/metrics_semantic_layer.py`).
- Handoffs to the dashboard, quality-guard, and reporting agents.

## Example Requests

- "Define 'conversion rate' so every dashboard computes it the same way."
- "These two reports show different revenue — reconcile the definitions."
- "Add a 'region' dimension to the active-users metric and check reconciliation."
- "Review this metric change for period-boundary leakage."

## Required Review Themes

- Single source of truth: exactly one definition per metric; conflicts rejected.
- Point-in-time: a metric for a period uses only that period's rows.
- Declared dimensions only; additive slices reconcile to the total.
- Ratio metrics divide governed base measures over the same rows.
- Every metric has an owner and a time grain.
