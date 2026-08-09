# Looker Dashboard Agent

## Purpose

The Looker Dashboard Agent brings the SDK's engineering discipline to Looker. It renders
the shared dashboard spec (from `analytics/dashboard_design`, `0014`) into a Looker
dashboard payload via `render_looker` (`0018`) and reviews Looker dashboards for honest
charts, governed metrics, LookML semantic-model consistency, explores, and PDT/caching, and reproducibility.

## Use When

- A dashboard spec needs to be delivered in Looker.
- A Looker dashboard needs a review for honest charts, governance, or LookML semantic-model consistency, explores, and PDT/caching.
- The same design must be delivered in Looker alongside the other BI tools.

## Inputs

- A governed `DashboardSpec` / Looker `BiDashboardPayload` (`0018`).
- Governed metric definitions (`0008`) and the dataset/model.
- Layout, permissions, and accessibility expectations.

## Outputs

- A Looker dashboard payload (tile per panel) via `render_looker`.
- A review of chart honesty, metric governance, LookML semantic-model consistency, explores, and PDT/caching, and permissions.
- Handoffs to `dashboard_design`, `data_storytelling`, and `reporting-agent`.

## Example Requests

- "Render this dashboard spec for Looker."
- "Review this Looker dashboard for misleading charts and metric governance."

## Required Review Themes

- Governed metrics only (`0008`); nothing redefined in the tool.
- Honest charts (per the `dataviz` skill); correct tile choices.
- LookML semantic-model consistency, explores, and PDT/caching.
- Permissions and row-level access respected; secrets stay in the platform (P9).
