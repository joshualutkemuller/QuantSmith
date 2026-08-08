"""Reference pipeline for spec 0016 (React target) — React dashboard profile.

Renders the tool-agnostic ``DashboardSpec`` (from `analytics/dashboard_design`, `0014`)
into a serializable React dashboard payload: one component per panel with a mapped
component name, props carrying the governed metric, and a deterministic grid layout a
React app consumes. Standard-library only and deterministic. Part of the `0014`/`0015`
BI-tool expansion track — it renders the *same* shared spec every profile renders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .dashboard_spec import DashboardSpec

# Tool-agnostic chart type -> React component name.
_CHART_TO_REACT: Dict[str, str] = {
    "bar": "BarChart",
    "line": "LineChart",
    "area": "AreaChart",
    "scatter": "ScatterChart",
    "table": "DataTable",
    "kpi": "KpiCard",
    "gauge": "GaugeChart",
    "map": "ChoroplethMap",
}

_GRID_COLUMNS = 2
_PANEL_W = 6            # half of a 12-column grid
_PANEL_H = 4


class ReactValidationError(ValueError):
    """Raised when a React dashboard payload is malformed."""


@dataclass(frozen=True)
class ReactComponent:
    id: str
    component: str                       # React component name
    props: Dict[str, object]


@dataclass(frozen=True)
class GridItem:
    i: str
    x: int
    y: int
    w: int
    h: int


@dataclass(frozen=True)
class ReactDashboardPayload:
    title: str
    dataset: str
    page: str
    components: Tuple[ReactComponent, ...]
    layout: Tuple[GridItem, ...]
    filters: Dict[str, str] = field(default_factory=dict)

    def measures(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for c in self.components:
            m = c.props.get("metric")
            if isinstance(m, str) and m not in seen:
                seen.append(m)
        return tuple(seen)


def render_react(spec: DashboardSpec) -> ReactDashboardPayload:
    """Render a governed ``DashboardSpec`` into a React dashboard payload.

    Each panel becomes a React component (mapped from its chart type) whose props carry
    the governed metric, and is placed on a deterministic 12-column grid. Dataset/page/
    filters carry through. Deterministic.
    """
    components: List[ReactComponent] = []
    layout: List[GridItem] = []
    for idx, p in enumerate(spec.panels):
        pid = f"panel-{idx}"
        components.append(
            ReactComponent(
                id=pid,
                component=_CHART_TO_REACT[p.chart_type],  # spec restricts to known types
                props={"title": p.title, "metric": p.metric, "dimensions": list(p.dimensions)},
            )
        )
        col = idx % _GRID_COLUMNS
        row = idx // _GRID_COLUMNS
        layout.append(
            GridItem(i=pid, x=col * _PANEL_W, y=row * _PANEL_H, w=_PANEL_W, h=_PANEL_H)
        )

    payload = ReactDashboardPayload(
        title=spec.title,
        dataset=spec.dataset,
        page=spec.page,
        components=tuple(components),
        layout=tuple(layout),
        filters=dict(spec.filters),
    )
    if not payload.components:
        raise ReactValidationError("a React dashboard needs at least one component")
    return payload
