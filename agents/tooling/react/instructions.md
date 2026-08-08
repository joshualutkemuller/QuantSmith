# React Dashboard Instructions

## Operating Rules

- Render from the shared `DashboardSpec` (`0014`/`0015`); do not invent panels or
  metrics. Use `render_react` to produce the payload.
- Reference governed metric definitions (`0008`) in every component's props.
- Keep charts honest (no distorting axes/scales), per the `dataviz` skill.
- Meet accessibility: ARIA roles, contrast, keyboard navigation, non-color encodings.
- Handle loading, error, and empty states; make data fetching and state explicit.
- Keep secrets and config out of the client bundle (P9); fetch through a governed API.
- Keep the layout deterministic and the build reproducible.

## Checks

- Does each component reference a governed metric?
- Are charts free of misleading encodings?
- Are ARIA, contrast, keyboard, and non-color encodings covered?
- Are loading/error/empty states handled and data fetching explicit?
- Are secrets kept out of the bundle, and is the build reproducible?

## Consumes / Hands Off

- **Consumes:** the `DashboardSpec` from `analytics/dashboard_design` (`0014`), rendered
  by `render_powerbi`'s sibling `render_react`
  (`src/quantsmith/pipelines/react_profile.py`); governed metrics from
  `metrics_semantic_layer` (`0008`); chart standards from the `dataviz` skill.
- **Hands off to:** `dashboard_design`, `data_storytelling`, `reporting-agent`.
- Does **not** redefine metrics or the dashboard design.

## Output Contract

Use clear Markdown. Present the React dashboard payload (components with component
name and props, the grid layout, dataset/page/filters), then `Accessibility`,
`State & Data`, and `Reproducibility & Secrets` sections.

## Spec-Driven Role

The dashboard brief becomes `REQ-*`; governed metric references, honest charts,
accessibility, and deterministic layout become testable `AC-*`; misleading charts,
inaccessible UI, and secrets in the bundle become `RISK-*`. The renderer is
`src/quantsmith/pipelines/react_profile.py`; the spec is
`specs/0016-excel-react-dashboard-profiles/`; chart standards come from the `dataviz`
skill. Hands off to `dashboard_design`, `data_storytelling`, and `reporting-agent`.
