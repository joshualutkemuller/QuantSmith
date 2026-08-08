"""Tool-agnostic dashboard spec — the code contract for `analytics/dashboard_design`.

Spec ``0014-data-analyst-storytelling`` defines a tool-agnostic dashboard spec that
BI-tool profiles render. This module makes that contract concrete so every profile
(Power BI first, others later) renders the *same* structure. Standard-library only.

A ``DashboardSpec`` is a governed design: each ``Panel`` names a governed metric (from
`metrics_semantic_layer`, `0008`) and a tool-agnostic chart type. Renderers map these
to a specific BI tool's payload; the spec itself is never tied to one tool.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

# Tool-agnostic chart types a dashboard spec may use.
CHART_TYPES = ("bar", "line", "area", "scatter", "table", "kpi", "gauge", "map")


class DashboardSpecError(ValueError):
    """Raised when a dashboard spec is malformed or ungoverned."""


@dataclass(frozen=True)
class Panel:
    """One panel: a governed metric shown with a tool-agnostic chart type."""

    title: str
    chart_type: str
    metric: str                      # a governed metric name (0008)
    dimensions: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.metric:
            raise DashboardSpecError(f"panel '{self.title}' has no governed metric")
        if self.chart_type not in CHART_TYPES:
            raise DashboardSpecError(
                f"panel '{self.title}' has unknown chart_type '{self.chart_type}' "
                f"(use one of {list(CHART_TYPES)})"
            )


@dataclass(frozen=True)
class DashboardSpec:
    """A tool-agnostic dashboard: ordered panels over a dataset, plus filters."""

    title: str
    dataset: str
    panels: Tuple[Panel, ...]
    filters: Dict[str, str] = field(default_factory=dict)
    page: str = "Overview"

    def __post_init__(self) -> None:
        if not self.panels:
            raise DashboardSpecError("a dashboard spec needs at least one panel")

    def metrics(self) -> Tuple[str, ...]:
        """Governed metrics used, in first-seen order, de-duplicated."""
        seen: list = []
        for p in self.panels:
            if p.metric not in seen:
                seen.append(p.metric)
        return tuple(seen)

    def chart_types(self) -> Tuple[str, ...]:
        """Chart types used, in first-seen order, de-duplicated."""
        seen: list = []
        for p in self.panels:
            if p.chart_type not in seen:
                seen.append(p.chart_type)
        return tuple(seen)
