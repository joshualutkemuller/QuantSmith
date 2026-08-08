"""Reference pipeline for spec 0016 (Excel target) — Excel dashboard profile.

Renders the tool-agnostic ``DashboardSpec`` (from `analytics/dashboard_design`, `0014`)
into an Excel workbook payload: a data sheet plus a dashboard sheet with one chart per
panel. Standard-library only and deterministic. Part of the `0014`/`0015` BI-tool
expansion track — it renders the *same* shared spec every profile renders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .dashboard_spec import DashboardSpec

# Tool-agnostic chart type -> Excel chart type.
_CHART_TO_EXCEL: Dict[str, str] = {
    "bar": "columnClustered",
    "line": "line",
    "area": "area",
    "scatter": "xyScatter",
    "table": "table",
    "kpi": "card",
    "gauge": "doughnut",   # Excel's conventional gauge substitute
    "map": "filledMap",
}


class ExcelValidationError(ValueError):
    """Raised when an Excel workbook payload is malformed."""


@dataclass(frozen=True)
class ExcelChart:
    title: str
    chart_type: str          # Excel chart type
    measure: str             # governed metric
    dimensions: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ExcelWorkbookPayload:
    title: str
    dataset: str
    data_sheet: str
    dashboard_sheet: str
    charts: Tuple[ExcelChart, ...]
    filters: Dict[str, str] = field(default_factory=dict)

    def measures(self) -> Tuple[str, ...]:
        seen: List[str] = []
        for c in self.charts:
            if c.measure not in seen:
                seen.append(c.measure)
        return tuple(seen)


def render_excel(spec: DashboardSpec, data_sheet: str = "Data") -> ExcelWorkbookPayload:
    """Render a governed ``DashboardSpec`` into an Excel workbook payload.

    Each panel becomes a chart on the dashboard sheet; the dataset lands on the data
    sheet. Chart types map to Excel chart types, governed metrics are preserved, and
    dataset/page/filters carry through. Deterministic.
    """
    charts = tuple(
        ExcelChart(
            title=p.title,
            chart_type=_CHART_TO_EXCEL[p.chart_type],  # spec restricts to known types
            measure=p.metric,
            dimensions=p.dimensions,
        )
        for p in spec.panels
    )
    payload = ExcelWorkbookPayload(
        title=spec.title,
        dataset=spec.dataset,
        data_sheet=data_sheet,
        dashboard_sheet=spec.page,
        charts=charts,
        filters=dict(spec.filters),
    )
    if not payload.charts:
        raise ExcelValidationError("an Excel workbook needs at least one chart")
    return payload
