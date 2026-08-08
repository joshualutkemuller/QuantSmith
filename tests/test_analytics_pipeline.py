"""Acceptance tests for spec 0010 — end-to-end analytics pipeline.

Each test is named for the acceptance criterion it covers (see
``specs/0010-analytics-pipeline/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.analytics_pipeline import (
    FactSchema,
    Table,
    prepare,
    run_pipeline,
)
from quantsmith.pipelines.metrics_semantic_layer import SemanticLayer

SCHEMA = FactSchema(
    period_field="month",
    dim_fields=("region",),
    measure_fields=("amount",),
)


def build_layer() -> SemanticLayer:
    layer = SemanticLayer()
    layer.define(
        name="revenue",
        owner="analytics",
        grain="month",
        dimensions=("region",),
        source="amount",
        agg="sum",
    )
    return layer


def build_table() -> Table:
    return Table(
        name="sales",
        rows=[
            {"month": 202401, "region": "US", "amount": 100.0},
            {"month": 202401, "region": "EU", "amount": 60.0},
            {"month": 202402, "region": "US", "amount": 200.0},
        ],
    )


# --- AC-001: one call runs the chain and returns a numeric answer ---


def test_pipeline_end_to_end_AC_001():
    report = run_pipeline(build_table(), build_layer(), "revenue", SCHEMA, period=202401)
    assert report.status == "ok"
    assert report.value == 160.0  # 100 + 60


# --- AC-002: preparation dedups, types, and profiles the rows ---


def test_preparation_dedups_and_profiles_AC_002():
    rows = [
        {"month": 202401, "region": "US", "amount": 100.0},
        {"month": 202401, "region": "US", "amount": 100.0},  # exact duplicate
        {"month": 202401, "region": "EU", "amount": None},   # missing measure
        {"month": None, "region": "US", "amount": 5.0},      # missing period -> dropped
    ]
    prepared = prepare(rows, SCHEMA)
    assert prepared.profile["n_input"] == 4
    assert prepared.profile["n_duplicates_removed"] == 1
    assert prepared.profile["n_dropped_missing_period"] == 1
    assert prepared.profile["missing"]["amount"] == 1
    # Two unique, period-bearing rows become facts (US 100, EU with no amount).
    assert prepared.profile["n_facts"] == 2


# --- AC-003: report metric matches the governed semantic-layer computation ---


def test_report_matches_semantic_layer_AC_003():
    layer = build_layer()
    table = build_table()
    report = run_pipeline(table, layer, "revenue", SCHEMA, group_by="region")
    prepared = prepare(list(table.rows), SCHEMA)
    direct = layer.compute("revenue", prepared.facts, group_by="region")
    assert report.value == direct


# --- AC-004: a failing quality check blocks the report ---


def test_quality_guard_blocks_AC_004():
    # Undefined metric -> blocked with a finding.
    blocked = run_pipeline(build_table(), build_layer(), "gross_margin", SCHEMA)
    assert blocked.status == "blocked"
    assert blocked.value is None
    assert any("ungoverned" in f for f in blocked.quality.findings)

    # Empty query result -> blocked.
    empty = run_pipeline(
        build_table(), build_layer(), "revenue", SCHEMA, where={"region": "APAC"}
    )
    assert empty.status == "blocked"
    assert any("empty result" in f for f in empty.quality.findings)

    # Valid request -> ok.
    ok = run_pipeline(build_table(), build_layer(), "revenue", SCHEMA, period=202402)
    assert ok.status == "ok"
    assert ok.value == 200.0


# --- AC-005: the report carries provenance ---


def test_report_provenance_AC_005():
    report = run_pipeline(build_table(), build_layer(), "revenue", SCHEMA, period=202401)
    prov = report.provenance
    assert prov["source"] == "sales"
    assert prov["period"] == 202401
    assert prov["n_input_rows"] == 3
    assert prov["metrics_used"] == ["revenue"]
    assert prov["definition"]["owner"] == "analytics"
    assert prov["definition"]["grain"] == "month"


# --- AC-006: the run is deterministic ---


def test_pipeline_reproducible_AC_006():
    a = run_pipeline(build_table(), build_layer(), "revenue", SCHEMA, group_by="region")
    b = run_pipeline(build_table(), build_layer(), "revenue", SCHEMA, group_by="region")
    assert a == b
