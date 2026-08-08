# React Dashboard Tasks

## Render A Dashboard Spec To React

Input: a governed `DashboardSpec` (`0014`/`0015`).

Output: a React dashboard payload (components, props, grid layout, dataset, page,
filters) via `render_react`.

## Review A React Dashboard

Input: an existing React dashboard.

Output: a review of chart honesty, accessibility (ARIA, contrast, keyboard), state and
data fetching, metric governance, and secrets handling, with concrete fixes.

## Deliver A Design Across Tools

Input: a dashboard spec already rendered to Power BI or Excel.

Output: the equivalent React payload from the same spec, so the design is consistent
across web and BI tools.

## Harden A Dashboard For Production

Input: a working React dashboard.

Output: loading/error/empty-state handling, reproducible build notes, and confirmation
that secrets/config stay out of the client bundle.
