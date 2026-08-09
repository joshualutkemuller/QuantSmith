# Qlik Dashboard Agent

## Purpose

The Qlik Dashboard Agent brings the SDK's engineering discipline to Qlik. It renders
the shared dashboard spec (from `analytics/dashboard_design`, `0014`) into a Qlik
dashboard payload via `render_qlik` (`0018`) and reviews Qlik dashboards for honest
charts, governed metrics, the associative data model, set analysis, and section-access security, and reproducibility.

## Use When

- A dashboard spec needs to be delivered in Qlik.
- A Qlik dashboard needs a review for honest charts, governance, or the associative data model, set analysis, and section-access security.
- The same design must be delivered in Qlik alongside the other BI tools.

## Inputs

- A governed `DashboardSpec` / Qlik `BiDashboardPayload` (`0018`).
- Governed metric definitions (`0008`) and the dataset/model.
- Layout, permissions, and accessibility expectations.

## Outputs

- A Qlik dashboard payload (object per panel) via `render_qlik`.
- A review of chart honesty, metric governance, the associative data model, set analysis, and section-access security, and permissions.
- Handoffs to `dashboard_design`, `data_storytelling`, and `reporting-agent`.

## Example Requests

- "Render this dashboard spec for Qlik."
- "Review this Qlik dashboard for misleading charts and metric governance."

## Required Review Themes

- Governed metrics only (`0008`); nothing redefined in the tool.
- Honest charts (per the `dataviz` skill); correct object choices.
- the associative data model, set analysis, and section-access security.
- Permissions and row-level access respected; secrets stay in the platform (P9).
