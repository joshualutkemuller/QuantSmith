# Qlik Dashboard Tasks

## Render A Dashboard Spec To Qlik

Input: a governed `DashboardSpec` / Qlik `BiDashboardPayload` (`0018`).

Output: a Qlik dashboard payload (object per panel) via `render_qlik`.

## Review A Qlik Dashboard

Input: an existing Qlik dashboard.

Output: a review of chart honesty, metric governance, the associative data model, set analysis, and section-access security, and permissions, with
concrete fixes.

## Deliver A Design Across Tools

Input: a dashboard spec already rendered to another BI tool.

Output: the equivalent Qlik payload from the same spec, consistent across tools.

## Govern Metrics And Access

Input: a Qlik dashboard and its metric/permission model.

Output: confirmation that metrics trace to governed definitions and that permissions
and row-level access are correct.
