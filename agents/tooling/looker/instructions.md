# Looker Dashboard Instructions

## Operating Rules

- Render from the shared `DashboardSpec` (`0018`) via `render_looker`; do not invent
  tile or metrics.
- Reference governed metric definitions (`0008`); never redefine a metric in Looker.
- Keep charts honest (per the `dataviz` skill) and choose appropriate tile.
- Mind LookML semantic-model consistency, explores, and PDT/caching.
- Respect permissions and row-level access; keep secrets in the platform (P9).

## Checks

- Does each tile reference a governed metric?
- Are charts honest and tile appropriate?
- Is LookML semantic-model consistency, explores, and PDT/caching handled?
- Are permissions and row-level access respected, with secrets kept in the platform?

## Consumes / Hands Off

- **Consumes:** the Looker `BiDashboardPayload` from `render_looker`
  (`src/quantsmith/pipelines/bi_profiles.py`); governed metrics from
  `metrics_semantic_layer` (`0008`); chart standards from the `dataviz` skill.
- **Hands off to:** `dashboard_design`, `data_storytelling`, `reporting-agent`.
- Does **not** redefine metrics or the dashboard design.

## Output Contract

Use clear Markdown. Present the Looker payload (tile per panel with the governed metric),
then `Chart Honesty`, `Looker Specifics`, and `Permissions` sections.

## Spec-Driven Role

The dashboard brief becomes `REQ-*`; governed metrics, honest charts, and LookML semantic-model consistency, explores, and PDT/caching
become testable `AC-*`; misleading charts, metric redefinition, and permission leaks
become `RISK-*`. The renderer is `bi_profiles.render_looker`; the spec is
`specs/0018-remaining-dashboard-profiles/`. Hands off to `dashboard_design`,
`data_storytelling`, and `reporting-agent`.
