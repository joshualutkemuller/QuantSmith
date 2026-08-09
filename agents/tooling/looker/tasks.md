# Looker Dashboard Tasks

## Render A Dashboard Spec To Looker

Input: a governed `DashboardSpec` / Looker `BiDashboardPayload` (`0018`).

Output: a Looker dashboard payload (tile per panel) via `render_looker`.

## Review A Looker Dashboard

Input: an existing Looker dashboard.

Output: a review of chart honesty, metric governance, LookML semantic-model consistency, explores, and PDT/caching, and permissions, with
concrete fixes.

## Deliver A Design Across Tools

Input: a dashboard spec already rendered to another BI tool.

Output: the equivalent Looker payload from the same spec, consistent across tools.

## Govern Metrics And Access

Input: a Looker dashboard and its metric/permission model.

Output: confirmation that metrics trace to governed definitions and that permissions
and row-level access are correct.
