# Plan: Excel and React dashboard profiles

- **Spec:** 0016-excel-react-dashboard-profiles (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Two more renderers on the `0015` pattern: each maps the shared `DashboardSpec` onto a
tool-specific payload, deterministically, using only governed metrics. Governance holds
by construction because the shared spec already rejects ungoverned panels and unknown
chart types; the renderers only translate. Pure Python; the Excel and React payloads
are plain dataclasses defined in their profile modules.

## Agent Routing

```text
analytics/dashboard_design (DashboardSpec)
  -> [render_powerbi]  -> tooling/power_bi          (spec 0015)
  -> [render_excel]    -> tooling/excel             (this spec)
  -> [render_react]    -> tooling/react (new)       (this spec)
```

One design, three renderers; metrics come from `metrics_semantic_layer` (`0008`).

## Architecture & Components

- `excel_profile.py` — `ExcelWorkbookPayload` / `ExcelChart` and `render_excel(spec)`:
  each panel → a chart on the dashboard sheet (named for the spec page), plus a data
  sheet; chart types map via `_CHART_TO_EXCEL`.
- `react_profile.py` — `ReactDashboardPayload` / `ReactComponent` / `GridItem` and
  `render_react(spec)`: each panel → a component (via `_CHART_TO_REACT`) with the
  governed metric in props and a deterministic 12-column grid layout.
- `tooling/react/` — a new agent for web-dashboard review (honesty, accessibility,
  state/data, secrets, reproducibility).

## Interfaces & Data Contracts

- Input: a `DashboardSpec` (`0014`/`0015`) with governed-metric panels.
- Excel output: `ExcelWorkbookPayload(title, dataset, data_sheet, dashboard_sheet,
  charts, filters)`.
- React output: `ReactDashboardPayload(title, dataset, page, components, layout,
  filters)`.
- Chart vocabularies map the shared types to Excel chart types and React components.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Shared spec rejects ungoverned/unknown; renderers are deterministic translations. |
| P5 Reversibility | yes | Payloads are build artifacts; re-render from the spec. |
| P6 Observability | yes | Payloads expose their measures and layout explicitly. |
| P9 Security & data | yes | No secrets in payloads; the React agent keeps secrets server-side. |
| P10 Honest reporting | yes | Governed metrics only; documented chart mappings avoid misleading substitution. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `render_excel` + `ExcelWorkbookPayload` | T-001 |
| REQ-002 | `render_react` + `ReactDashboardPayload` | T-002 |
| REQ-003 | shared `DashboardSpec`; carry-through | T-001, T-002 |
| REQ-004 | `tooling/react` agent | T-003 |
| NFR-001 | deterministic mapping | T-001, T-002 |
| NFR-002 | one shared spec | T-001, T-002 |
| NFR-003 | governed metrics + chart vocabularies | T-001, T-002 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Payloads | Dataclasses in the profile modules | Add to shared contracts | Keeps each profile self-contained; no existing Excel/React contract to reuse. |
| Excel gauge | Map to doughnut | Reject gauge | Doughnut is Excel's conventional gauge substitute; documented for review. |
| React output | Serializable component + grid spec | Emit JSX/source | A payload is testable and framework-version-agnostic; codegen is downstream. |
| React agent | Add `tooling/react` | Reuse a generic tooling agent | Web dashboards have distinct review rules (accessibility, state, bundle secrets). |

## Validation Strategy

- AC-001/002: render to Excel and React; assert chart/component mappings and layout.
- AC-003: assert dataset/page/filters/order carry through and measures equal the spec's
  governed metrics.
- AC-004: render twice; assert identical payloads.
- AC-005: assert empty/ungoverned specs are refused by the shared contract.

## Rollout, Observability & Rollback

Renderers imported by the Excel and React agents. Rollout adds them; rollback removes
them. The `DashboardSpec` stays the tool-agnostic source of truth, re-renderable to any
target.

## Open Questions

- Whether to add a live `.xlsx` writer and a React scaffold behind the adapter
  contract, and which BI tool (Looker/Qlik/Superset/Streamlit) is next.
