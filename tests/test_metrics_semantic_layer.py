"""Acceptance tests for spec 0008 — metrics semantic layer.

Each test is named for the acceptance criterion it covers (see
``specs/0008-metrics-semantic-layer/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import math

import pytest

from quantsmith.pipelines.metrics_semantic_layer import (
    Fact,
    GovernanceError,
    MetricDefinition,
    SemanticLayer,
)


def sample_layer() -> SemanticLayer:
    layer = SemanticLayer()
    layer.define(
        name="revenue",
        owner="analytics",
        grain="month",
        dimensions=("region",),
        source="amount",
        agg="sum",
    )
    layer.define(
        name="conversion_rate",
        owner="analytics",
        grain="month",
        dimensions=("region",),
        numerator="conversions",
        denominator="sessions",
    )
    return layer


def sample_rows():
    return [
        Fact(period=202401, dims={"region": "US"}, measures={"amount": 100.0, "conversions": 3, "sessions": 30}),
        Fact(period=202401, dims={"region": "EU"}, measures={"amount": 60.0, "conversions": 2, "sessions": 40}),
        Fact(period=202402, dims={"region": "US"}, measures={"amount": 200.0, "conversions": 5, "sessions": 50}),
    ]


# --- AC-001: conflicting re-definition is rejected ---


def test_conflicting_definition_rejected_AC_001():
    layer = sample_layer()
    with pytest.raises(GovernanceError):
        layer.define(
            name="revenue",  # same name, different measure -> conflict
            owner="finance",
            grain="month",
            source="net_amount",
            agg="sum",
        )
    # Re-registering the identical definition is idempotent (no error).
    layer.define(name="revenue", owner="analytics", grain="month", dimensions=("region",), source="amount", agg="sum")


# --- AC-002: a metric for a period uses only rows in that period ---


def test_period_filter_is_point_in_time_AC_002():
    layer = sample_layer()
    rows = sample_rows()
    jan = layer.compute("revenue", rows, period=202401)
    assert jan == 160.0  # 100 + 60, February's 200 excluded

    # Adding a later-period row must not change the January value.
    rows2 = rows + [Fact(period=202403, dims={"region": "US"}, measures={"amount": 999.0})]
    assert layer.compute("revenue", rows2, period=202401) == jan


# --- AC-003: declared-dimension slices reconcile to the total; undeclared rejected ---


def test_dimension_slices_reconcile_AC_003():
    layer = sample_layer()
    rows = sample_rows()
    total = layer.compute("revenue", rows)  # all periods, ungrouped
    by_region = layer.compute("revenue", rows, group_by="region")
    assert isinstance(by_region, dict)
    assert math.isclose(sum(by_region.values()), total)

    # Grouping by an undeclared dimension is a governance error.
    with pytest.raises(GovernanceError):
        layer.compute("revenue", rows, group_by="product")


# --- AC-004: a ratio metric divides governed base measures over the same rows ---


def test_ratio_metric_consistent_AC_004():
    layer = sample_layer()
    rows = sample_rows()
    rate = layer.compute("conversion_rate", rows, period=202401)
    # (3 + 2) conversions / (30 + 40) sessions
    assert math.isclose(rate, 5.0 / 70.0)


# --- AC-005: an undefined metric raises, naming the metric ---


def test_undefined_metric_rejected_AC_005():
    layer = sample_layer()
    with pytest.raises(GovernanceError) as exc:
        layer.compute("gross_margin", sample_rows())
    assert "gross_margin" in str(exc.value)


# --- AC-006: computation is deterministic ---


def test_computation_reproducible_AC_006():
    layer = sample_layer()
    rows = sample_rows()
    a = layer.compute("revenue", rows, group_by="region")
    b = layer.compute("revenue", rows, group_by="region")
    assert a == b


# --- governance: owner and grain are required at registration ---


def test_missing_owner_or_grain_rejected():
    layer = SemanticLayer()
    with pytest.raises(GovernanceError):
        layer.define(name="x", owner="", grain="month", source="amount")
    with pytest.raises(GovernanceError):
        layer.define(name="y", owner="analytics", grain="", source="amount")
    with pytest.raises(GovernanceError):
        MetricDefinition and layer.define(name="z", owner="analytics", grain="month", source="amount", agg="median")
