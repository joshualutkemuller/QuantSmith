# Streamlit Dashboard Agent

## Purpose

The Streamlit Dashboard Agent brings engineering discipline to Python-native
dashboards built in Streamlit. It renders the shared dashboard spec (from
`analytics/dashboard_design`, `0014`) into a Streamlit app via `render_streamlit`
(`0018`) and the executable `scaffold_streamlit` adapter, and reviews Streamlit apps
for honest charts, caching/state correctness, reproducibility, and secrets hygiene.

## Use When

- A dashboard spec needs to be delivered as a Streamlit app.
- A Streamlit app needs a review for caching, reruns, honest charts, or secrets.
- The same design must be delivered in Streamlit alongside Power BI / Excel / React.

## Inputs

- A governed `DashboardSpec` / Streamlit `BiDashboardPayload` (`0018`).
- Governed metric definitions (`0008`) and the data source / endpoint.
- Caching, layout, and accessibility expectations.

## Outputs

- A Streamlit app (`app.py`, `requirements.txt`) via `scaffold_streamlit`.
- A review of `@st.cache_data` usage, rerun/state correctness, chart honesty, and
  secrets kept out of the app.
- Handoffs to `dashboard_design`, `data_storytelling`, and `reporting-agent`.

## Example Requests

- "Render this dashboard spec as a Streamlit app."
- "Review this Streamlit app for caching correctness and misleading charts."

## Required Review Themes

- Governed metrics only (`0008`); nothing recomputed or invented in the app.
- Correct caching (`@st.cache_data`) and rerun/state handling.
- Honest charts (per the `dataviz` skill); loading/empty states handled.
- Data loaded from a governed endpoint; secrets stay in the environment, never in code.
- Deterministic scaffold and pinned, reproducible requirements.
