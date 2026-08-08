# Spec: Excel and React dashboard profiles

- **ID:** 0016-excel-react-dashboard-profiles
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Two more BI-tool profiles from the `0014`/`0015` expansion track: render the shared
> tool-agnostic dashboard spec to Excel and to a React web dashboard.

## Problem & Context

Spec `0015` established the pattern — a tool-agnostic `DashboardSpec` and a renderer
per BI tool (Power BI first). Two common delivery targets were still missing: **Excel**
(the analyst's most common surface, with an existing `tooling/excel` agent but no
renderer) and **React** (web dashboards, with no agent at all). This spec adds both
renderers on the same shared spec, and adds a `tooling/react` agent for the web target,
so one governed design can be delivered as Power BI, Excel, or a React app without
rework.

## Goals

- Render a `DashboardSpec` into an Excel workbook payload (data sheet + dashboard sheet
  with a chart per panel).
- Render a `DashboardSpec` into a React dashboard payload (a component per panel with a
  deterministic grid layout).
- Reuse the shared `DashboardSpec` (`0014`/`0015`) — one design contract, three
  renderers — with governed metrics only.
- Add a `tooling/react` agent for web-dashboard review (the Excel agent already exists).

## Non-Goals

- Writing real `.xlsx` files or a running React app (the profiles produce validated
  payloads; file/bundle generation is a downstream/deployment concern).
- New dashboard *design* or metric semantics (owned by `0014` and `0008`).
- Additional BI tools (Looker, Qlik, Superset, Streamlit remain the tracked backlog).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Render a `DashboardSpec` into an Excel workbook payload: a data sheet and a dashboard sheet with one chart per panel, chart types mapped to Excel chart types, governed metrics preserved. | must |
| REQ-002 | Render a `DashboardSpec` into a React dashboard payload: one component per panel (mapped from the chart type) with props carrying the governed metric and a deterministic grid layout. | must |
| REQ-003 | Both renderers shall reuse the shared `DashboardSpec` and carry dataset, page, and filters and panel order; only governed metrics appear. | must |
| REQ-004 | Add a `tooling/react` agent for web-dashboard review; the existing `tooling/excel` agent covers the Excel target. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same `DashboardSpec` renders to identical Excel and React payloads every time. |
| NFR-002 | Reuse | Both renderers consume the one shared `DashboardSpec`; no new design contract is introduced. |
| NFR-003 | Honesty & governance | Only governed metrics are rendered; chart-type mappings preserve the intended encoding (no misleading substitution). |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a `DashboardSpec`, when rendered to Excel, then each panel becomes a chart with its mapped Excel chart type and governed measure, on a dashboard sheet named for the page. | REQ-001 |
| AC-002 | Given a `DashboardSpec`, when rendered to React, then each panel becomes a mapped component with the governed metric in its props and a deterministic grid layout (one item per panel). | REQ-002 |
| AC-003 | Given a spec, when rendered to either target, then dataset, page, filters, and panel order are carried through and the measures are exactly the spec's governed metrics. | REQ-003, NFR-003 |
| AC-004 | Given the same spec, when rendered twice to either target, then the payloads are identical. | NFR-001 |
| AC-005 | Given an empty or ungoverned spec, when rendering is attempted, then it is refused (by the shared `DashboardSpec` contract). | REQ-003, NFR-002 |

## Data & Dependencies

- Input: a `DashboardSpec` from `analytics/dashboard_design` (`0014`/`0015`), panels
  referencing governed metrics (`0008`).
- Agents: `tooling/excel` (existing) and the new `tooling/react`; upstream
  `analytics/dashboard_design`.
- No new external contracts; the Excel and React payloads are defined in their profile
  modules.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Ungoverned or misleading visuals reach Excel/React. | Untrustworthy dashboards. | Governed metrics only; the shared spec's chart vocabulary restricts types (NFR-003). |
| RISK-002 | Divergent design contracts per tool. | Rework, inconsistency. | One shared `DashboardSpec`; three renderers (NFR-002). |
| RISK-003 | Secrets leak into a React bundle. | Credential exposure. | The `tooling/react` agent enforces secrets stay server-side (P9). |
| RISK-004 | Excel's missing chart types (e.g. gauge) misrepresented. | Misleading charts. | Explicit, documented mappings (gauge → doughnut) reviewed by `tooling/excel`. |

## Assumptions & Open Questions

- Assumption: a validated payload is the deliverable; `.xlsx` generation and React
  bundling are downstream steps.
- Open question: whether to add a live `.xlsx` writer / React scaffold behind the
  adapter contract (tracked, not silently deferred).

## Exceptions

None.
