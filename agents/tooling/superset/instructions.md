# Superset Dashboard Instructions

## Operating Rules

- Render from the shared `DashboardSpec` (`0018`) via `render_superset`; do not invent
  chart or metrics.
- Reference governed metric definitions (`0008`); never redefine a metric in Superset.
- Keep charts honest (per the `dataviz` skill) and choose appropriate chart.
- Mind SQL/dataset governance, Jinja templating safety, and caching.
- Respect permissions and row-level access; keep secrets in the platform (P9).

## Checks

- Does each chart reference a governed metric?
- Are charts honest and chart appropriate?
- Is SQL/dataset governance, Jinja templating safety, and caching handled?
- Are permissions and row-level access respected, with secrets kept in the platform?

## Consumes / Hands Off

- **Consumes:** the Superset `BiDashboardPayload` from `render_superset`
  (`src/quantsmith/pipelines/bi_profiles.py`); governed metrics from
  `metrics_semantic_layer` (`0008`); chart standards from the `dataviz` skill.
- **Hands off to:** `dashboard_design`, `data_storytelling`, `reporting-agent`.
- Does **not** redefine metrics or the dashboard design.

## Output Contract

Use clear Markdown. Present the Superset payload (chart per panel with the governed metric),
then `Chart Honesty`, `Superset Specifics`, and `Permissions` sections.

## Spec-Driven Role

The dashboard brief becomes `REQ-*`; governed metrics, honest charts, and SQL/dataset governance, Jinja templating safety, and caching
become testable `AC-*`; misleading charts, metric redefinition, and permission leaks
become `RISK-*`. The renderer is `bi_profiles.render_superset`; the spec is
`specs/0018-remaining-dashboard-profiles/`. Hands off to `dashboard_design`,
`data_storytelling`, and `reporting-agent`.
