"""Acceptance tests for spec 0018 — remaining BI dashboard profiles + Streamlit scaffold.

Each test is named for the acceptance criterion it covers (see
``specs/0018-remaining-dashboard-profiles/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import os

import pytest

from quantsmith.adapters.dashboard_render import scaffold_streamlit
from quantsmith.adapters.dashboard_render.result import contains_secret
from quantsmith.pipelines.bi_profiles import (
    render_looker,
    render_qlik,
    render_streamlit,
    render_superset,
)
from quantsmith.pipelines.dashboard_spec import DashboardSpec, DashboardSpecError, Panel


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


# --- AC-001: each renderer maps panels to the tool's object types ---


def test_tool_mappings_AC_001():
    spec = sample_spec()
    assert [e.object_type for e in render_streamlit(spec).elements] == [
        "st.bar_chart", "st.line_chart", "st.metric"]
    assert [e.object_type for e in render_looker(spec).elements] == [
        "looker_column", "looker_line", "single_value"]
    assert [e.object_type for e in render_superset(spec).elements] == [
        "echarts_timeseries_bar", "echarts_timeseries_line", "big_number_total"]
    assert [e.object_type for e in render_qlik(spec).elements] == [
        "barchart", "linechart", "kpi"]


# --- AC-002: governed measures + carry-through, all four tools ---


def test_measures_and_carry_through_AC_002():
    spec = sample_spec()
    for render in (render_streamlit, render_looker, render_superset, render_qlik):
        p = render(spec)
        assert p.measures() == ("revenue", "conversion_rate")
        assert p.dataset == "sales"
        assert p.page == "Exec"
        assert p.filters == {"region": "ALL"}
        assert set(p.measures()) == set(spec.metrics())


# --- AC-003: every renderer is deterministic ---


def test_deterministic_AC_003():
    spec = sample_spec()
    for render in (render_streamlit, render_looker, render_superset, render_qlik):
        assert render(spec) == render(spec)


# --- AC-004: ungoverned/empty specs refused upstream ---


def test_ungoverned_refused_AC_004():
    with pytest.raises(DashboardSpecError):
        render_qlik(DashboardSpec(title="t", dataset="d", panels=()))
    with pytest.raises(DashboardSpecError):
        Panel(title="x", chart_type="bar", metric="")


# --- AC-005: Streamlit scaffolder writes a runnable, secret-free app ---


def test_streamlit_scaffold_AC_005(tmp_path):
    payload = render_streamlit(sample_spec())
    result = scaffold_streamlit(payload, str(tmp_path))
    assert result.status == "generated"
    assert os.path.isfile(tmp_path / "app.py")
    assert os.path.isfile(tmp_path / "requirements.txt")
    app = (tmp_path / "app.py").read_text()
    assert not contains_secret(app)
    assert "st.title('Revenue Overview')" in app
    assert "conversion_rate" in app          # governed metric present
    assert "DATA_ENDPOINT" in app            # data via endpoint, not embedded

    # Non-streamlit payload is rejected.
    with pytest.raises(ValueError):
        scaffold_streamlit(render_qlik(sample_spec()), str(tmp_path / "x"))


# --- AC-006: Streamlit scaffold dry-run plans without writing; deterministic ---


def test_streamlit_dry_run_and_determinism_AC_006(tmp_path):
    payload = render_streamlit(sample_spec())
    planned = scaffold_streamlit(payload, str(tmp_path), dry_run=True)
    assert planned.status == "planned"
    assert os.listdir(tmp_path) == []
    a = scaffold_streamlit(payload, str(tmp_path / "a"))
    b = scaffold_streamlit(payload, str(tmp_path / "b"))
    assert [(f.path, f.checksum) for f in a.files] == [(f.path, f.checksum) for f in b.files]
