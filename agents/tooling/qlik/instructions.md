# Qlik Dashboard Instructions

## Operating Rules

- Render from the shared `DashboardSpec` (`0018`) via `render_qlik`; do not invent
  object or metrics.
- Reference governed metric definitions (`0008`); never redefine a metric in Qlik.
- Keep charts honest (per the `dataviz` skill) and choose appropriate object.
- Mind the associative data model, set analysis, and section-access security.
- Respect permissions and row-level access; keep secrets in the platform (P9).

## Checks

- Does each object reference a governed metric?
- Are charts honest and object appropriate?
- Is the associative data model, set analysis, and section-access security handled?
- Are permissions and row-level access respected, with secrets kept in the platform?

## Consumes / Hands Off

- **Consumes:** the Qlik `BiDashboardPayload` from `render_qlik`
  (`src/quantsmith/pipelines/bi_profiles.py`); governed metrics from
  `metrics_semantic_layer` (`0008`); chart standards from the `dataviz` skill.
- **Hands off to:** `dashboard_design`, `data_storytelling`, `reporting-agent`.
- Does **not** redefine metrics or the dashboard design.

## Output Contract

Use clear Markdown. Present the Qlik payload (object per panel with the governed metric),
then `Chart Honesty`, `Qlik Specifics`, and `Permissions` sections.

## Spec-Driven Role

The dashboard brief becomes `REQ-*`; governed metrics, honest charts, and the associative data model, set analysis, and section-access security
become testable `AC-*`; misleading charts, metric redefinition, and permission leaks
become `RISK-*`. The renderer is `bi_profiles.render_qlik`; the spec is
`specs/0018-remaining-dashboard-profiles/`. Hands off to `dashboard_design`,
`data_storytelling`, and `reporting-agent`.
