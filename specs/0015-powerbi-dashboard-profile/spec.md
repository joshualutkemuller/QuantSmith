# Spec: Power BI dashboard profile

- **ID:** 0015-powerbi-dashboard-profile
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> First BI-tool profile from the `0014` expansion track: renders the tool-agnostic
> dashboard spec into a Power BI payload, reusing the existing Power BI contract and
> validator.

## Problem & Context

Spec `0014` added `analytics/dashboard_design`, which produces a *tool-agnostic*
dashboard spec, and named a BI-tool expansion track to render it. But the spec was
prose only — there was no code contract for it, and no renderer, so a design could not
actually become a Power BI report. Separately, the existing Power BI runtime
(`agentic_code_tools/powerbi.py`) was dead code: it imported a `PowerBIPayload`
contract that had never been defined, so it could not even be imported. This spec fixes
that contract and ships the first renderer: a `DashboardSpec` → Power BI payload
profile, validated by the existing `PowerBIPayloadValidator`.

## Goals

- A concrete, tool-agnostic `DashboardSpec` code contract (panels with governed
  metric references and chart types, filters) — the input every BI-tool profile
  renders.
- A Power BI renderer that maps a `DashboardSpec` to a Power BI report payload,
  reusing the existing `PowerBIPayload` and `PowerBIPayloadValidator`.
- Repair the broken Power BI contract so the existing runtime imports and validates.
- A pattern the remaining profiles (Looker, Qlik, Superset, Streamlit) follow.

## Non-Goals

- A live Power BI API/publish integration (the profile produces a validated payload;
  publishing is a deployment concern).
- Metric definition, dashboard *design*, or storytelling (owned by `0008` and `0014`).
- Rendering to other BI tools (this profile is Power BI; others follow the pattern).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Provide a tool-agnostic `DashboardSpec` contract (ordered panels, each with a governed metric and a chart type from a fixed vocabulary, plus dataset, page, and filters). | must |
| REQ-002 | Render a `DashboardSpec` into a Power BI payload, mapping chart types to Power BI visuals and governed metrics to measures, de-duplicated and order-preserving, carrying dataset/page/filters. | must |
| REQ-003 | Validate the rendered payload with the existing `PowerBIPayloadValidator`, and reject a spec with an empty panel set or a panel lacking a governed metric. | must |
| REQ-004 | Repair the `PowerBIPayload` contract so the existing Power BI runtime imports and validates. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reuse | The renderer reuses `PowerBIPayload` and `PowerBIPayloadValidator`; it does not define a new payload or validator. |
| NFR-002 | Reproducibility | The same `DashboardSpec` renders to an identical payload every time. |
| NFR-003 | Governance | Every rendered measure is a governed metric from the spec; unknown chart types and metric-less panels are rejected. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a `DashboardSpec`, when rendered, then the payload's visuals and measures reflect the panels (de-duplicated, ordered) and the title/dataset/page are carried through. | REQ-002 |
| AC-002 | Given panels with chart types from the vocabulary, when rendered, then each maps to its Power BI visual; an unknown chart type is rejected at spec construction. | REQ-001, REQ-002 |
| AC-003 | Given a panel with no governed metric or an empty panel set, when constructed, then a `DashboardSpecError` is raised; a valid render passes the `PowerBIPayloadValidator`. | REQ-003, NFR-003 |
| AC-004 | Given the same spec, when rendered twice, then the payloads are identical and filters/dataset are carried through. | NFR-002 |
| AC-005 | Given an empty panel set, when a spec is constructed, then it is rejected before rendering. | REQ-003 |

## Data & Dependencies

- Input: a `DashboardSpec` from `analytics/dashboard_design` (`0014`), whose panels
  reference governed metrics from `metrics_semantic_layer` (`0008`).
- Reused: `PowerBIPayload` and `PowerBIPayloadValidator`
  (`src/quantsmith/agentic_code_tools/`).
- Agents: `tooling/power_bi`, `powerbi-dashboard-agent` (the Power BI review/build
  roles) and `analytics/dashboard_design` (the design source).
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Ungoverned or misleading visuals reach Power BI. | Untrustworthy dashboards. | Panels reference governed metrics; the vocabulary restricts chart types (NFR-003). |
| RISK-002 | A new payload/validator duplicates the existing one. | Divergent Power BI contracts. | Reuse `PowerBIPayload` + `PowerBIPayloadValidator` (NFR-001). |
| RISK-003 | The profile only works for Power BI. | Rework per tool. | The `DashboardSpec` is tool-agnostic; other profiles render the same contract. |
| RISK-004 | The Power BI runtime stays broken. | Dead code, no reuse. | Repair the `PowerBIPayload` contract (REQ-004). |

## Assumptions & Open Questions

- Assumption: a validated payload is the deliverable; publishing to a workspace is a
  separate deployment step.
- Open question: which profile is next (Looker vs Streamlit), decided by the consuming
  team (tracked, not silently deferred).

## Exceptions

None.
