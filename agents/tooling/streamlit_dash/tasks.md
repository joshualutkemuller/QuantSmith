# Streamlit Dashboard Tasks

## Render A Dashboard Spec To Streamlit

Input: a governed `DashboardSpec` / Streamlit `BiDashboardPayload` (`0018`).

Output: a Streamlit app (`app.py`, `requirements.txt`) via `scaffold_streamlit`.

## Review A Streamlit App

Input: an existing Streamlit app.

Output: a review of caching/state, chart honesty, data loading, and secrets handling,
with concrete fixes.

## Deliver A Design Across Tools

Input: a dashboard spec already rendered to Power BI / Excel / React.

Output: the equivalent Streamlit app from the same spec, consistent across tools.

## Harden For Reproducibility

Input: a working Streamlit app.

Output: pinned requirements, deterministic caching, and confirmation that secrets stay
in the environment.
