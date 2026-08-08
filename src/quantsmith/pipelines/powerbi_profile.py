"""Reference pipeline for spec 0015 — Power BI dashboard profile.

This module makes the ``0015-powerbi-dashboard-profile`` spec *executable*: it renders
the tool-agnostic ``DashboardSpec`` from `analytics/dashboard_design` (`0014`) into a
Power BI report payload, reusing the existing `PowerBIPayload` contract and
`PowerBIPayloadValidator`. It is the first concrete renderer for the `0014` BI-tool
expansion track — later profiles (Looker, Qlik, Superset, Streamlit) render the same
spec the same way. Deterministic and standard-library only.
"""

from __future__ import annotations

from typing import Dict

from ..agentic_code_tools.contracts import PowerBIPayload
from ..agentic_code_tools.powerbi import PowerBIPayloadValidator, PowerBIValidationError
from .dashboard_spec import DashboardSpec

# Tool-agnostic chart type -> Power BI visual name.
_CHART_TO_VISUAL: Dict[str, str] = {
    "bar": "clustered_column",
    "line": "line",
    "area": "area",
    "scatter": "scatter",
    "table": "matrix",
    "kpi": "card",
    "gauge": "gauge",
    "map": "map",
}


def render_powerbi(spec: DashboardSpec, validate: bool = True) -> PowerBIPayload:
    """Render a governed ``DashboardSpec`` into a validated Power BI payload.

    Panels map to Power BI visuals and their governed metrics to measures, both
    de-duplicated and order-preserving; the spec's filters, dataset, and page are
    carried through. The result is validated with the existing
    `PowerBIPayloadValidator` (reuse, not a new validator). Deterministic.
    """
    visuals: list = []
    for ct in spec.chart_types():
        visual = _CHART_TO_VISUAL.get(ct)
        if visual is None:  # defensive: DashboardSpec already restricts chart types
            raise PowerBIValidationError(f"no Power BI visual mapping for chart type '{ct}'")
        if visual not in visuals:
            visuals.append(visual)

    measures = list(spec.metrics())  # governed metrics, de-duplicated & ordered

    payload = PowerBIPayload(
        title=spec.title,
        dataset=spec.dataset,
        report_page=spec.page,
        visuals=visuals,
        measures=measures,
        filters=dict(spec.filters),
    )
    if validate:
        PowerBIPayloadValidator().validate(payload)
    return payload
