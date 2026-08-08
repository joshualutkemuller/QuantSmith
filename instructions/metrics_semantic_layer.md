# Metrics Semantic Layer Standard

How to define and govern metrics so a KPI means the same thing everywhere. This is
the standard behind the `analytics/metrics_semantic_layer` agent and the
`specs/0008-metrics-semantic-layer/` runtime.

## Why A Semantic Layer

When "revenue" or "conversion rate" is redefined in every dashboard, SQL query, and
report, the same question returns different numbers and trust erodes. A semantic
layer defines each metric **once** and computes it **consistently**, so dashboards
and reports read a definition rather than reinventing it.

## A Metric Definition

Every metric declares:

- **name** — the canonical identifier (one per metric).
- **kind** — `measure` (aggregate one base measure) or `ratio` (divide two base
  measures).
- **measure + aggregation** (`sum`/`count`/`mean`) for a measure metric, or
  **numerator + denominator** base measures for a ratio.
- **dimensions** — the attributes the metric may be sliced by (and only these).
- **grain** — the time grain the metric is reported at (e.g. day, month).
- **owner** — the team or person accountable for the definition.

## Governance Rules

1. **Single source of truth.** Exactly one definition per metric name. A conflicting
   re-definition is rejected; an identical one is idempotent.
2. **Owner and grain required.** No metric is served without both.
3. **Declared dimensions only.** Slicing by an undeclared dimension is an error.
4. **Point-in-time.** A metric for a period uses only that period's rows; a period
   boundary must never leak rows from another period.
5. **Additive reconciliation.** For additive metrics, the sum of declared-dimension
   slices equals the ungrouped total. Non-additive measures (distinct counts,
   medians, ratios) are flagged and handled explicitly.
6. **Ratios over shared rows.** A ratio divides summed base measures over the same
   filtered rows — never an average of per-row ratios.
7. **Fail loudly.** An ungoverned request (undefined metric, undeclared dimension)
   returns an explicit error, and an undefined division returns `NaN`, not a
   misleading `0`.

## Checklist

- [ ] Exactly one definition per metric name.
- [ ] Owner and grain present.
- [ ] Dimensions declared; no undeclared slicing.
- [ ] Period filter is point-in-time.
- [ ] Additive slices reconcile to the total.
- [ ] Ratios computed from governed base measures over the same rows.
- [ ] Ungoverned requests error instead of returning a wrong number.

## Runtime & Spec

- Runtime: `src/quantsmith/pipelines/metrics_semantic_layer.py`
  (`SemanticLayer`, `MetricDefinition`, `Fact`, `GovernanceError`).
- Spec: `specs/0008-metrics-semantic-layer/`.
- Consumers: `tooling/tableau`, `tooling/power_bi`, `quality-guard-agent`,
  `reporting-agent`.
