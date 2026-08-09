"""Streamlit scaffold provider — turn a Streamlit BiDashboardPayload into an app.

Pure standard library: generates a deterministic Streamlit app (`app.py` +
`requirements.txt`) from the payload and writes it (or plans it on ``dry_run``).
Implements the Streamlit side of ``adapters/dashboard_render/``. Data is loaded from a
governed source at runtime; no data or secrets are baked into the app.
"""

from __future__ import annotations

import os
from typing import Dict

from ...pipelines.bi_profiles import BiDashboardPayload
from .result import RenderResult, contains_secret, manifest

# Streamlit object type -> a call template. Metric-bound; data is loaded at runtime.
_WIDGET = {
    "st.bar_chart": "st.bar_chart(df, y={metric!r})",
    "st.line_chart": "st.line_chart(df, y={metric!r})",
    "st.area_chart": "st.area_chart(df, y={metric!r})",
    "st.scatter_chart": "st.scatter_chart(df, y={metric!r})",
    "st.dataframe": "st.dataframe(df)",
    "st.metric": "st.metric({title!r}, float(df[{metric!r}].iloc[-1]) if len(df) else 0.0)",
    "st.plotly_chart": "st.write({title!r} + ' (gauge: ' + {metric!r} + ')')",
    "st.map": "st.map(df)",
}


def _files(payload: BiDashboardPayload) -> Dict[str, str]:
    lines = [
        "# Auto-generated Streamlit dashboard. Do not edit by hand.",
        "import os",
        "import pandas as pd",
        "import streamlit as st",
        "",
        f"DATASET = {payload.dataset!r}",
        f"FILTERS = {dict(payload.filters)!r}",
        "",
        "@st.cache_data",
        "def load_data(dataset):",
        "    # Load governed data from a server endpoint; no credentials in the app.",
        "    endpoint = os.environ.get('DATA_ENDPOINT', 'http://localhost:8000/api/data')",
        "    return pd.read_json(f'{endpoint}?dataset={dataset}')",
        "",
        f"st.title({payload.title!r})",
        "df = load_data(DATASET)",
        "",
    ]
    for e in payload.elements:
        tmpl = _WIDGET.get(e.object_type)
        call = tmpl.format(metric=e.metric, title=e.title) if tmpl else f"st.write({e.title!r})"
        lines.append(f"st.subheader({e.title!r})")
        lines.append(call)
        lines.append("")
    app_py = "\n".join(lines) + "\n"

    requirements = "streamlit==1.38.0\npandas==2.2.2\n"
    readme = (
        f"# {payload.title}\n\n"
        f"Generated Streamlit dashboard for dataset `{payload.dataset}` "
        f"(page: {payload.page}).\n\n"
        "Data is loaded from `$DATA_ENDPOINT` at runtime; credentials stay server-side.\n"
        "Run `pip install -r requirements.txt && streamlit run app.py`.\n"
    )
    return {"app.py": app_py, "requirements.txt": requirements, "README.md": readme}


def scaffold_streamlit(
    payload: BiDashboardPayload,
    destination: str,
    dry_run: bool = False,
) -> RenderResult:
    """Generate a Streamlit app from a Streamlit BiDashboardPayload.

    Deterministic: the same payload yields the same files and checksums. ``dry_run``
    plans without writing. Raises on a non-Streamlit payload or if any file would
    contain a secret.
    """
    if payload.tool != "streamlit":
        raise ValueError(f"expected a streamlit payload, got tool={payload.tool!r}")

    files = _files(payload)
    for path, content in files.items():
        if contains_secret(content):
            raise ValueError(f"generated file '{path}' would contain a secret")

    records = manifest(files)
    if dry_run:
        return RenderResult(
            adapter_name="dashboard_render",
            provider="streamlit_scaffold",
            status="planned",
            artifact_uri=None,
            files=records,
            dry_run=True,
        )

    for rel, content in files.items():
        full = os.path.join(destination, rel)
        os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)

    return RenderResult(
        adapter_name="dashboard_render",
        provider="streamlit_scaffold",
        status="generated",
        artifact_uri=destination,
        files=records,
        dry_run=False,
    )
