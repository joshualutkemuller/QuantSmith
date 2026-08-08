# Spec: Metrics semantic layer

- **ID:** 0008-metrics-semantic-layer
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> First runtime workflow for the **Data Analyst** role: the canonical metric layer
> the analyst chain routes through before dashboards and reports.

## Problem & Context

The Data Analyst workflow (`docs/workflows.md`) routes through a
`metrics_semantic_layer` node that did not exist. Without it, "revenue",
"conversion rate", and other KPIs are redefined ad hoc in every dashboard, SQL
query, and report, so the same question returns different numbers depending on who
asked. This spec defines a governed semantic layer: each metric is defined once,
computed consistently and point-in-time, and sliced only by declared dimensions —
the single biggest data-analyst consistency win.

## Goals

- One canonical definition per metric (measure, allowed dimensions, time grain,
  owner) that dashboards and reports share.
- Consistent, point-in-time computation: a metric for a period uses only that
  period's rows, and dimension slices reconcile to the total.
- Derived (ratio) metrics computed from the same governed base measures, so a
  numerator and denominator can never disagree.
- Governance checks that reject undefined metrics, undeclared dimensions, and
  definitions missing an owner or grain before any value is served.

## Non-Goals

- A query engine, warehouse, or BI-tool integration (the dashboard agents consume
  the computed values; connection is out of scope here).
- Metric *discovery* or auto-suggestion; definitions are authored deliberately.
- Access control and row-level security (owned by `secrets_management/` and the
  warehouse, referenced but not implemented here).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The semantic layer shall define each metric exactly once (name, measure, allowed dimensions, time grain, owner) as the single source of truth; a conflicting re-definition is rejected. | must |
| REQ-002 | The layer shall compute a metric deterministically from fact rows, sliced only by declared dimensions and filtered to the requested period as-of. | must |
| REQ-003 | The layer shall support derived (ratio) metrics computed from the same governed base measures over the same filtered rows. | must |
| REQ-004 | The layer shall expose governance errors for undefined metrics, undeclared dimensions, and definitions missing an owner or time grain. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same registry and rows yield identical metric values on every computation. |
| NFR-002 | Point-in-time correctness | A metric for period P uses only rows whose period is P; rows outside P never change the value. |
| NFR-003 | Consistency | For an additive metric, the sum of its declared-dimension slices reconciles to the ungrouped total. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a registry with a metric, when a different definition is registered for the same name, then registration raises a governance error (and re-registering the identical definition does not). | REQ-001 |
| AC-002 | Given fact rows spanning periods, when a metric is computed for period P, then only rows in P contribute and rows outside P do not change the value. | REQ-002, NFR-002 |
| AC-003 | Given a declared dimension, when a metric is sliced by it, then the slices reconcile to the ungrouped total; given an undeclared dimension, computation raises a governance error. | REQ-002, NFR-003 |
| AC-004 | Given a ratio metric, when it is computed, then it equals the summed numerator measure divided by the summed denominator measure over the same filtered rows. | REQ-003 |
| AC-005 | Given a request for an undefined metric, when it is computed, then a governance error names the metric. | REQ-004 |
| AC-006 | Given the same registry and rows, when a metric is computed twice, then the values are identical. | NFR-001 |

## Data & Dependencies

- Fact rows: a period key, dimension values, and measure values (produced upstream by
  `sql-integration-agent` / `data-prep-agent`, as-of the reporting period).
- Metric definitions authored by the `metrics_semantic_layer` agent and its owners.
- Downstream consumers: `tableau`/`power_bi` dashboard agents, `reporting-agent`,
  `quality-guard-agent`.
- Standard: `instructions/metrics_semantic_layer.md`; documentation via
  `instructions/documentation.md`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | The same metric defined differently in two places. | Dashboards disagree; trust erodes. | Single-source-of-truth registry; conflicting definitions rejected (AC-001). |
| RISK-002 | A period boundary leaks rows from another period. | Wrong period totals; misleading trends. | Point-in-time period filter (AC-002 / NFR-002). |
| RISK-003 | Numerator and denominator of a ratio computed over different filters. | Inconsistent rates. | Ratio computed from the same governed base measures over the same rows (AC-004). |
| RISK-004 | Slices that do not reconcile to the total. | Analysts cannot trust drill-downs. | Additive reconciliation check for declared dimensions (AC-003 / NFR-003). |

## Assumptions & Open Questions

- Assumption: measures are additive within a period for the reconciliation guarantee;
  non-additive measures (distinct counts, medians) are a documented follow-up.
- Assumption: the period key is comparable and pre-derived to the metric's grain.
- Open question: should definitions live in code or a YAML registry the layer loads?
  Deferred to the plan's open questions (tracked, not silently deferred).

## Exceptions

None.
