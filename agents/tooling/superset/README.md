# Superset Dashboard Agent

## Purpose

The Superset Dashboard Agent brings the SDK's engineering discipline to Superset. It renders
the shared dashboard spec (from `analytics/dashboard_design`, `0014`) into a Superset
dashboard payload via `render_superset` (`0018`) and reviews Superset dashboards for honest
charts, governed metrics, SQL/dataset governance, Jinja templating safety, and caching, and reproducibility.

## Use When

- A dashboard spec needs to be delivered in Superset.
- A Superset dashboard needs a review for honest charts, governance, or SQL/dataset governance, Jinja templating safety, and caching.
- The same design must be delivered in Superset alongside the other BI tools.

## Inputs

- A governed `DashboardSpec` / Superset `BiDashboardPayload` (`0018`).
- Governed metric definitions (`0008`) and the dataset/model.
- Layout, permissions, and accessibility expectations.

## Outputs

- A Superset dashboard payload (chart per panel) via `render_superset`.
- A review of chart honesty, metric governance, SQL/dataset governance, Jinja templating safety, and caching, and permissions.
- Handoffs to `dashboard_design`, `data_storytelling`, and `reporting-agent`.

## Example Requests

- "Render this dashboard spec for Superset."
- "Review this Superset dashboard for misleading charts and metric governance."

## Required Review Themes

- Governed metrics only (`0008`); nothing redefined in the tool.
- Honest charts (per the `dataviz` skill); correct chart choices.
- SQL/dataset governance, Jinja templating safety, and caching.
- Permissions and row-level access respected; secrets stay in the platform (P9).
