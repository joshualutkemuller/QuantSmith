# React Dashboard Agent

## Purpose

The React Dashboard Agent brings the SDK's engineering discipline to **web
dashboards** built in React. It renders the tool-agnostic dashboard spec (from
`analytics/dashboard_design`, `0014`) into a React dashboard payload — a component per
panel, props carrying the governed metric, and a deterministic layout — and reviews
React dashboards for correctness, honesty, accessibility, and reproducibility. It is
the web-dashboard target of the `0014`/`0015` BI-tool expansion track.

## Use When

- A dashboard spec needs to be rendered as a React application.
- A React dashboard needs a review for accessible, non-misleading charts.
- A web dashboard needs its data fetching, state, and metric references reviewed.
- The same design must be delivered in React alongside Power BI / Excel.

## Inputs

- A governed `DashboardSpec` (`0014`/`0015`) whose panels reference governed metrics.
- The target chart/component library and accessibility requirements.
- Data-source and refresh expectations for the web app.

## Outputs

- A React dashboard payload (`render_react`): components (mapped from chart types),
  props (governed metric, dimensions, title), a grid layout, dataset, page, filters.
- A review of chart honesty, accessibility (ARIA, contrast, keyboard), state/data
  fetching, and metric governance.
- Handoffs to the design (`dashboard_design`), storytelling, and reporting agents.

## Example Requests

- "Render this dashboard spec as a React app payload."
- "Review this React dashboard for accessibility and misleading charts."
- "Deliver the exec dashboard in React as well as Power BI."

## Required Review Themes

- Every component's metric references a governed definition (`0008`); nothing invented.
- Charts are honest (no distorting axes/scales), matching the `dataviz` skill.
- Accessibility: ARIA roles, contrast, keyboard navigation, non-color encodings.
- Deterministic layout and reproducible builds; secrets stay out of the bundle (P9).
- Data fetching and state are explicit; loading/error/empty states handled.
