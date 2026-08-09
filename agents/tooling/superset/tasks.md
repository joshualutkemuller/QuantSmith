# Superset Dashboard Tasks

## Render A Dashboard Spec To Superset

Input: a governed `DashboardSpec` / Superset `BiDashboardPayload` (`0018`).

Output: a Superset dashboard payload (chart per panel) via `render_superset`.

## Review A Superset Dashboard

Input: an existing Superset dashboard.

Output: a review of chart honesty, metric governance, SQL/dataset governance, Jinja templating safety, and caching, and permissions, with
concrete fixes.

## Deliver A Design Across Tools

Input: a dashboard spec already rendered to another BI tool.

Output: the equivalent Superset payload from the same spec, consistent across tools.

## Govern Metrics And Access

Input: a Superset dashboard and its metric/permission model.

Output: confirmation that metrics trace to governed definitions and that permissions
and row-level access are correct.
