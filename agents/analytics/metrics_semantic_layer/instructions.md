# Metrics Semantic Layer Instructions

## Operating Rules

- Define each metric exactly once; a conflicting re-definition for the same name is
  rejected, not merged silently.
- Give every metric an owner and a time grain before it is served.
- Declare the dimensions a metric may be sliced by; reject slicing by any other.
- Compute a metric for a period from that period's rows only — never leak rows across
  a period boundary.
- Define ratio metrics as summed numerator / summed denominator over the same
  filtered rows; never average per-row ratios.
- Keep additive metrics additive so declared-dimension slices reconcile to the total;
  flag non-additive measures (distinct counts, medians) explicitly.
- Return an explicit error (not a misleading `0`) when a request is ungoverned.

## Checks

- Is there exactly one definition per metric name?
- Does every metric have an owner and a time grain?
- Are all requested slices declared dimensions of the metric?
- Does the period filter exclude other periods (point-in-time)?
- Is each ratio computed from governed base measures over the same rows?
- Do additive slices reconcile to the ungrouped total?

## Output Contract

Use clear Markdown. State the canonical definition in a fenced block or table
(name, kind, measure/aggregation or numerator/denominator, dimensions, grain,
owner). Include a `Governance Review` section listing conflicts, point-in-time
risks, and reconciliation notes. Name the runtime symbol
(`SemanticLayer`/`MetricDefinition`) when handing off to code.

## Spec-Driven Role

A metric definition becomes a `REQ-*`; single-source-of-truth, point-in-time period
filtering, dimension reconciliation, and ratio consistency become testable `AC-*`;
duplicate/conflicting definitions and period-boundary leakage become `RISK-*`. The
standard is `instructions/metrics_semantic_layer.md`; the runtime is
`src/quantsmith/pipelines/metrics_semantic_layer.py`; the worked spec is
`specs/0008-metrics-semantic-layer/`. Hands off to `tooling/tableau`,
`tooling/power_bi`, `quality-guard-agent`, and `reporting-agent`.
