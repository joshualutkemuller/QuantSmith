# Plan: Metrics semantic layer

- **Spec:** 0008-metrics-semantic-layer (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Implement a small registry-plus-evaluator. Metric definitions are registered once
and stored; computation is a deterministic aggregation over fact rows that filters
to the requested period and slices only by declared dimensions. Governance holds *by
construction*: registration validates each definition and rejects conflicting
re-definitions, and computation rejects undefined metrics and undeclared dimensions
before touching data.

## Agent Routing

The workflow is the Data Analyst chain (see `docs/workflows.md` → *Data Analyst*):

```text
planning_requirements
  -> sql-integration-agent        # governed query, schema discovery
  -> data-prep-agent              # clean/profile facts (period, dims, measures)
  -> eda-specialist-agent         # hypotheses, sanity checks
  -> metrics_semantic_layer       # canonical definitions + consistent computation
  -> tooling/tableau | tooling/power_bi   # dashboards consume computed values
  -> quality-guard-agent          # contract/consistency checks before release
  -> reporting-agent              # stakeholder-ready answer with provenance
```

The `metrics_semantic_layer` agent owns the definitions; the runtime is the evaluator.

## Architecture & Components

- `Fact(period, dims, measures)` — one fact row keyed by a comparable period.
- `MetricDefinition(name, owner, grain, dimensions, source/agg | numerator/denominator)`
  — the single source of truth; `kind` is `measure` or `ratio`.
- `SemanticLayer.register/define` — validates and stores a definition; rejects a
  conflicting re-definition (idempotent for identical ones).
- `SemanticLayer.compute(name, rows, period, group_by)` — filters to the period,
  aggregates, and (optionally) slices by a declared dimension.
- `GovernanceError` — the single, explicit failure type for contract violations.

## Interfaces & Data Contracts

- Input: a `SemanticLayer` populated with definitions, and fact rows with a `period`,
  `dims`, and `measures`.
- Output: a scalar metric value, or a `{dimension_value: value}` map when `group_by`
  is set.
- All inputs are as-of the reporting period → no cross-period leakage (NFR-002).

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Governance validated at registration; period filter and declared-dimension checks at computation. |
| P5 Reversibility | yes | Definitions are data; revert by restoring the prior registry. |
| P6 Observability | yes | Governance errors are explicit and name the offending metric/dimension. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo; access control deferred to the warehouse. |
| P10 Honest reporting | yes | Single definition per metric; ratios reconcile; div-by-zero returns NaN rather than a misleading 0. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `register` single-source-of-truth + conflict rejection | T-001 |
| REQ-002 | `compute` period filter + declared-dimension slicing | T-002 |
| REQ-003 | ratio metrics via `_value` over shared filtered rows | T-003 |
| REQ-004 | `_validate` + `GovernanceError` paths | T-004 |
| NFR-001 | deterministic aggregation | T-002 |
| NFR-002 | period filter in `compute` | T-002 |
| NFR-003 | additive slice reconciliation | T-002 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Definition store | In-code registry | External SQL/semantic tool | Keeps the reference dependency-free and testable; a YAML/warehouse loader is a follow-up. |
| Ratio computation | Sum both base measures over the same rows | Average of per-row ratios | Averaging per-row ratios is the classic inconsistency bug; base-measure division is correct. |
| Div-by-zero | Return NaN | Return 0.0 | 0.0 is a misleading "answer"; NaN signals undefined honestly (P10). |
| Reconciliation scope | Additive metrics | All metrics | Distinct counts and medians are non-additive; scoped and documented. |

## Validation Strategy

- AC-001: register a conflicting definition; assert `GovernanceError`; assert an
  identical re-registration is a no-op.
- AC-002: compute for a period; assert out-of-period rows do not change the value.
- AC-003: assert slice values sum to the ungrouped total; assert an undeclared
  dimension raises.
- AC-004: assert the ratio equals summed numerator / summed denominator.
- AC-005: compute an undefined metric; assert the error names it.
- AC-006: compute twice; assert identical values.

## Rollout, Observability & Rollback

The layer is a library consumed by the dashboard and reporting agents. Rollout
publishes new/updated definitions; rollback restores the prior registry. Governance
errors surface at definition and query time, so inconsistencies fail loudly rather
than shipping a wrong number.

## Open Questions

- Should definitions move to a YAML registry the layer loads at startup, versioned in
  the repo? Deferred until a second consumer needs it.
- Add non-additive measures (distinct count, percentile) with their own
  reconciliation semantics.
