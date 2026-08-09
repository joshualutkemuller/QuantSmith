# Streamlit Dashboard Instructions

## Operating Rules

- Render from the shared `DashboardSpec` (`0018`); do not invent widgets or metrics.
  Use `render_streamlit` + `scaffold_streamlit`.
- Reference governed metric definitions (`0008`) in every widget.
- Use `@st.cache_data` for data loading; keep reruns deterministic.
- Handle loading and empty states; keep charts honest (per the `dataviz` skill).
- Load data from a governed endpoint/source; keep secrets in the environment, never in
  `app.py`.
- Pin `requirements.txt` for reproducible installs.

## Checks

- Does each widget reference a governed metric?
- Is caching correct and are reruns deterministic?
- Are charts honest and empty states handled?
- Are secrets kept out of the app code?
- Are requirements pinned?

## Consumes / Hands Off

- **Consumes:** the Streamlit `BiDashboardPayload` from `render_streamlit`
  (`src/quantsmith/pipelines/bi_profiles.py`) and `scaffold_streamlit`
  (`src/quantsmith/adapters/dashboard_render/streamlit_scaffold.py`); governed metrics
  from `metrics_semantic_layer` (`0008`); chart standards from the `dataviz` skill.
- **Hands off to:** `dashboard_design`, `data_storytelling`, `reporting-agent`.
- Does **not** redefine metrics or the dashboard design.

## Output Contract

Use clear Markdown. Present the generated files (`app.py`, `requirements.txt`), then
`Caching & State`, `Chart Honesty`, and `Secrets & Reproducibility` sections.

## Spec-Driven Role

The dashboard brief becomes `REQ-*`; governed metrics, caching/state correctness,
honest charts, and reproducible requirements become testable `AC-*`; misleading charts,
cache misuse, and secrets in code become `RISK-*`. The renderer is
`bi_profiles.render_streamlit`; the scaffolder is `scaffold_streamlit`; specs are
`specs/0018-remaining-dashboard-profiles/` and `specs/0017-dashboard-render-adapters/`.
Hands off to `dashboard_design`, `data_storytelling`, and `reporting-agent`.
