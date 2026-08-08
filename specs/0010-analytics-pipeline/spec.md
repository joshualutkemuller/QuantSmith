# Spec: End-to-end analytics pipeline

- **ID:** 0010-analytics-pipeline
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Capstone for the **Data Analyst** role: runs the whole analyst chain end to end and
> composes the governed metrics layer (`0008`).

## Problem & Context

The Data Analyst chain has agents for every step and two spec-backed nodes
(`0008-metrics-semantic-layer`, `0009-experimentation`), but the chain itself — query
→ prepare → explore → metrics → quality guard → report — had no end-to-end spec or
acceptance tests. Without a capstone, the pieces are individually sound but the
"business question → trustworthy answer" path is unproven and can drift. This spec
defines the pipeline as one runnable, reproducible workflow that turns a source and a
metric request into a governed report artifact, refusing to publish when a quality
check fails.

## Goals

- One runnable path from a data source and a metric request to a report answer.
- Data preparation that dedups, types, and profiles rows and surfaces missingness.
- Metric values computed through the governed semantic layer (`0008`), never ad hoc.
- A quality guard that blocks the report on empty results, ungoverned metrics, or a
  failed reconciliation.
- A report artifact that carries provenance a reviewer can trust.

## Non-Goals

- A real warehouse connector, BI rendering, or scheduling (the ingestion, dashboard,
  and orchestration agents own those; this is the deterministic reference path).
- New metric semantics (owned by `0008`) or experiment analysis (owned by `0009`).
- Natural-language request parsing (owned by the `orchestrator-agent`).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The pipeline shall run the Data Analyst chain end to end from a source and a metric request to a report artifact. | must |
| REQ-002 | Data preparation shall produce typed, deduplicated facts and a data-quality profile (input/unique/fact counts, duplicates removed, missingness). | must |
| REQ-003 | Metric values shall be computed through the governed semantic layer (`0008`), not recomputed ad hoc. | must |
| REQ-004 | A quality guard shall block the report when a check fails (empty result, ungoverned metric, failed reconciliation) and record findings. | must |
| REQ-005 | The report artifact shall carry provenance: source, period, row counts, and the metric definition used. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same source and registry yield an identical report on every run. |
| NFR-002 | Point-in-time | A report for a period reflects only that period's rows (delegated to the `0008` period filter). |
| NFR-003 | Governed consistency | Every reported metric has a definition in the semantic layer; there are no ungoverned numbers. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a source and a metric request, when the pipeline runs, then it returns a report with a numeric answer and status "ok". | REQ-001 |
| AC-002 | Given rows with duplicates and missing values, when they are prepared, then duplicates are removed, missingness is counted, and the fact count reflects typed, period-bearing rows. | REQ-002 |
| AC-003 | Given a metric request, when the pipeline computes it, then the report value equals the semantic layer's direct computation for the same inputs. | REQ-003, NFR-003 |
| AC-004 | Given an ungoverned metric or an empty result, when the pipeline runs, then the report is "blocked" with a finding; a valid request is "ok". | REQ-004 |
| AC-005 | Given a completed run, when the report is produced, then it carries provenance (source, period, input/fact counts, metric definition). | REQ-005 |
| AC-006 | Given the same inputs, when the pipeline runs twice, then the reports are identical. | NFR-001 |

## Data & Dependencies

- A source table of rows (the reference stand-in for a `sql-integration-agent` query).
- A populated `SemanticLayer` from `0008-metrics-semantic-layer`.
- A `FactSchema` mapping source fields to period, dimensions, and measures.
- Agents: `sql-integration-agent`, `data-prep-agent`, `eda-specialist-agent`,
  `analytics/metrics_semantic_layer`, `quality-guard-agent`, `reporting-agent`.
- Standards: `instructions/data_quality.md`, `instructions/metrics_semantic_layer.md`,
  `instructions/documentation.md`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | A wrong number ships because a metric was recomputed ad hoc. | Untrustworthy report. | Metrics computed only through the `0008` semantic layer (AC-003 / NFR-003). |
| RISK-002 | An empty or broken query publishes a misleading zero. | False conclusions. | Quality guard blocks empty results and ungoverned metrics (AC-004). |
| RISK-003 | Duplicated rows inflate totals. | Overstated metrics. | Preparation dedups and profiles rows (AC-002). |
| RISK-004 | A report without provenance cannot be audited. | Un-reviewable output. | Provenance attached to every report (AC-005). |

## Assumptions & Open Questions

- Assumption: the source query is deterministic and pre-derived to the metric's grain.
- Assumption: exact-duplicate rows are safe to drop; near-duplicate resolution is a
  follow-up owned by `data-prep-agent`.
- Open question: should the report render to a dashboard payload (Tableau/Power BI)
  here, or stay a structured artifact the dashboard agents consume? Deferred.

## Exceptions

None.
