"""Acceptance tests for spec 0017 — dashboard render adapters (executable providers).

Each test is named for the acceptance criterion it covers (see
``specs/0017-dashboard-render-adapters/tasks.md``). The React tests are
standard-library only; the real-xlsx-write test skips if openpyxl is absent.
"""

from __future__ import annotations

import os

import pytest

from quantsmith.adapters.dashboard_render import scaffold_react, write_xlsx
from quantsmith.adapters.dashboard_render.result import contains_secret
from quantsmith.pipelines.dashboard_spec import DashboardSpec, Panel
from quantsmith.pipelines.excel_profile import render_excel
from quantsmith.pipelines.react_profile import render_react


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


# --- AC-001: React scaffolder writes the expected project files ---


def test_react_scaffold_writes_files_AC_001(tmp_path):
    payload = render_react(sample_spec())
    result = scaffold_react(payload, str(tmp_path))
    assert result.status == "generated"
    assert result.provider == "react_scaffold"
    for expected in ("package.json", "src/Dashboard.jsx", "src/useData.js", "src/components/registry.jsx"):
        assert os.path.isfile(tmp_path / expected)
    # Manifest matches what was written.
    assert set(result.paths()) == set(
        f.replace(os.sep, "/") for f in (
            "package.json", "README.md", ".gitignore",
            "src/main.jsx", "src/Dashboard.jsx", "src/useData.js", "src/components/registry.jsx",
        )
    )


# --- AC-002: dry-run plans files without writing ---


def test_react_dry_run_plans_only_AC_002(tmp_path):
    payload = render_react(sample_spec())
    result = scaffold_react(payload, str(tmp_path), dry_run=True)
    assert result.status == "planned"
    assert result.files  # a manifest was produced
    assert os.listdir(tmp_path) == []  # nothing written


# --- AC-003: no secrets in generated output; data fetched from an endpoint ---


def test_react_no_secrets_AC_003(tmp_path):
    payload = render_react(sample_spec())
    scaffold_react(payload, str(tmp_path))
    dash = (tmp_path / "src" / "Dashboard.jsx").read_text()
    hook = (tmp_path / "src" / "useData.js").read_text()
    assert not contains_secret(dash)
    assert not contains_secret(hook)
    assert "/api/data" in hook          # data via endpoint, not embedded
    assert "conversion_rate" in dash    # governed metric present in props


# --- AC-004: xlsx dry-run plans; real write produces a loadable workbook ---


def test_xlsx_dry_run_AC_004(tmp_path):
    payload = render_excel(sample_spec())
    planned = write_xlsx(payload, str(tmp_path), dry_run=True)
    assert planned.status == "planned"
    assert os.listdir(tmp_path) == []


def test_xlsx_real_write_AC_004():
    openpyxl = pytest.importorskip("openpyxl")
    import tempfile

    payload = render_excel(sample_spec())
    with tempfile.TemporaryDirectory() as d:
        result = write_xlsx(payload, d)
        assert result.status == "generated"
        assert result.artifact_uri.endswith(".xlsx")
        wb = openpyxl.load_workbook(result.artifact_uri)
        assert wb.sheetnames == ["Data", "Exec"]  # data_sheet + dashboard_sheet
        # Header row carries the governed measures.
        headers = [c.value for c in wb["Data"][1]]
        assert "revenue" in headers and "conversion_rate" in headers


# --- AC-005: deterministic — same payload, same manifest ---


def test_deterministic_AC_005(tmp_path):
    payload = render_react(sample_spec())
    a = scaffold_react(payload, str(tmp_path / "a"))
    b = scaffold_react(payload, str(tmp_path / "b"))
    assert [(f.path, f.checksum) for f in a.files] == [(f.path, f.checksum) for f in b.files]


# --- AC-006: renders only the payload (governed components only) ---


def test_renders_only_payload_AC_006(tmp_path):
    payload = render_react(sample_spec())
    scaffold_react(payload, str(tmp_path))
    registry = (tmp_path / "src" / "components" / "registry.jsx").read_text()
    # Exactly the used component names appear (BarChart, LineChart, KpiCard).
    for name in ("BarChart", "LineChart", "KpiCard"):
        assert f"export function {name}(" in registry
    assert "ScatterChart" not in registry  # not used by this spec
