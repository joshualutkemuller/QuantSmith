"""Reference pipeline for spec 0018 — remaining BI dashboard profiles.

Renders the shared tool-agnostic ``DashboardSpec`` (from `analytics/dashboard_design`,
`0014`/`0015`) into the remaining common BI targets — Streamlit, Looker, Superset, and
Qlik — completing the renderer set (Power BI/Excel/React ship in `0015`/`0016`). The
renderers differ only by their chart-type mapping, so they share one payload type and
one mapping helper. Standard-library only and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .dashboard_spec import DashboardSpec

# Per-tool: tool-agnostic chart type -> that tool's object/visual type.
# Every tool covers all of dashboard_spec.CHART_TYPES.
_CHART_MAPS: Dict[str, Dict[str, str]] = {
    "streamlit": {
        "bar": "st.bar_chart", "line": "st.line_chart", "area": "st.area_chart",
        "scatter": "st.scatter_chart", "table": "st.dataframe", "kpi": "st.metric",
        "gauge": "st.plotly_chart", "map": "st.map",
    },
    "looker": {
        "bar": "looker_column", "line": "looker_line", "area": "looker_area",
        "scatter": "looker_scatter", "table": "looker_grid", "kpi": "single_value",
        "gauge": "looker_pie", "map": "looker_map",
    },
    "superset": {
        "bar": "echarts_timeseries_bar", "line": "echarts_timeseries_line",
        "area": "echarts_area", "scatter": "echarts_timeseries_scatter",
        "table": "table", "kpi": "big_number_total", "gauge": "gauge_chart",
        "map": "country_map",
    },
    "qlik": {
        "bar": "barchart", "line": "linechart", "area": "areachart",
        "scatter": "scatterplot", "table": "table", "kpi": "kpi",
        "gauge": "gauge", "map": "map",
    },
}


@dataclass(frozen=True)
class BiElement:
    title: str
    object_type: str        # the tool's object/visual type
    metric: str             # governed metric
    dimensions: Tuple[str, ...] = ()


@dataclass(frozen=True)
class BiDashboardPayload:
    tool: str               # streamlit | looker | superset | qlik
    title: str
    dataset: str
    page: str
    elements: Tuple[BiElement, ...]
    filters: Dict[str, str] = field(default_factory=dict)

    def measures(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for e in self.elements:
            if e.metric not in seen:
                seen.append(e.metric)
        return tuple(seen)

    def object_types(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for e in self.elements:
            if e.object_type not in seen:
                seen.append(e.object_type)
        return tuple(seen)


def _render(spec: DashboardSpec, tool: str) -> BiDashboardPayload:
    chart_map = _CHART_MAPS[tool]
    elements = tuple(
        BiElement(
            title=p.title,
            object_type=chart_map[p.chart_type],   # spec restricts to known chart types
            metric=p.metric,
            dimensions=p.dimensions,
        )
        for p in spec.panels
    )
    return BiDashboardPayload(
        tool=tool,
        title=spec.title,
        dataset=spec.dataset,
        page=spec.page,
        elements=elements,
        filters=dict(spec.filters),
    )


def render_streamlit(spec: DashboardSpec) -> BiDashboardPayload:
    """Render a DashboardSpec into a Streamlit app payload."""
    return _render(spec, "streamlit")


def render_looker(spec: DashboardSpec) -> BiDashboardPayload:
    """Render a DashboardSpec into a Looker (LookML) dashboard payload."""
    return _render(spec, "looker")


def render_superset(spec: DashboardSpec) -> BiDashboardPayload:
    """Render a DashboardSpec into an Apache Superset dashboard payload."""
    return _render(spec, "superset")


def render_qlik(spec: DashboardSpec) -> BiDashboardPayload:
    """Render a DashboardSpec into a Qlik app payload."""
    return _render(spec, "qlik")
