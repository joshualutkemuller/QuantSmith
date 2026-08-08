"""Acceptance tests for spec 0016 — Excel and React dashboard profiles.

Each test is named for the acceptance criterion it covers (see
``specs/0016-excel-react-dashboard-profiles/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.dashboard_spec import DashboardSpec, Panel
from quantsmith.pipelines.excel_profile import ExcelWorkbookPayload, render_excel
from quantsmith.pipelines.react_profile import ReactDashboardPayload, render_react


def sample_spec() -> DashboardSpec:
    return DashboardSpec(
        title="Revenue Overview",
        dataset="sales",
        page="Exec",
        panels=(
            Panel(title="Revenue by region", chart_type="bar", metric="revenue", dimensions=("region",)),
            Panel(title="Revenue trend", chart_type="line", metric="revenue"),
            Panel(title="Conversion rate", chart_type="kpi", metric="conversion_rate"),
        ),
        filters={"region": "ALL"},
    )


# --- AC-001: Excel render maps each panel to an Excel chart ---


def test_excel_render_AC_001():
    wb = render_excel(sample_spec())
    assert isinstance(wb, ExcelWorkbookPayload)
    assert wb.title == "Revenue Overview"
    assert wb.dataset == "sales"
    assert wb.dashboard_sheet == "Exec"
    assert wb.data_sheet == "Data"
    assert [c.chart_type for c in wb.charts] == ["columnClustered", "line", "card"]
    assert [c.measure for c in wb.charts] == ["revenue", "revenue", "conversion_rate"]
    assert wb.measures() == ("revenue", "conversion_rate")  # de-duplicated


# --- AC-002: React render maps each panel to a component with a deterministic layout ---


def test_react_render_AC_002():
    app = render_react(sample_spec())
    assert isinstance(app, ReactDashboardPayload)
    assert [c.component for c in app.components] == ["BarChart", "LineChart", "KpiCard"]
    assert [c.props["metric"] for c in app.components] == ["revenue", "revenue", "conversion_rate"]
    # One layout item per panel, deterministic 12-col grid (2 columns of width 6).
    assert len(app.layout) == 3
    assert (app.layout[0].x, app.layout[0].y) == (0, 0)
    assert (app.layout[1].x, app.layout[1].y) == (6, 0)
    assert (app.layout[2].x, app.layout[2].y) == (0, 4)


# --- AC-003: both preserve dataset/page/filters and panel order; governed metrics only ---


def test_carry_through_and_governed_AC_003():
    spec = sample_spec()
    wb = render_excel(spec)
    app = render_react(spec)
    assert wb.filters == {"region": "ALL"}
    assert app.filters == {"region": "ALL"}
    assert app.page == "Exec"
    # Measures are exactly the governed metrics from the spec.
    assert set(wb.measures()) <= set(spec.metrics())
    assert set(app.measures()) <= set(spec.metrics())
    assert wb.measures() == spec.metrics()
    assert app.measures() == spec.metrics()


# --- AC-004: both renderers are deterministic ---


def test_deterministic_AC_004():
    spec = sample_spec()
    assert render_excel(spec) == render_excel(spec)
    assert render_react(spec) == render_react(spec)


# --- AC-005: an ungoverned/empty spec is refused upstream by DashboardSpec ---


def test_ungoverned_spec_refused_AC_005():
    import pytest

    from quantsmith.pipelines.dashboard_spec import DashboardSpecError

    with pytest.raises(DashboardSpecError):
        render_excel(DashboardSpec(title="t", dataset="d", panels=()))
    with pytest.raises(DashboardSpecError):
        render_react(DashboardSpec(title="t", dataset="d", panels=()))
    with pytest.raises(DashboardSpecError):
        Panel(title="x", chart_type="bar", metric="")  # ungoverned panel
