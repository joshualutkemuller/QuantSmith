"""Acceptance tests for spec 0019 — data-pipeline observability.

Each test is named for the acceptance criterion it covers (see
``specs/0019-pipeline-observability/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.data_pipeline import DataContract, Pipeline, Step, backfill, run
from quantsmith.pipelines.pipeline_observability import observe

CONTRACT = DataContract(name="rows", columns={"id": int}, required=frozenset({"id"}))


def source(inputs, partition):
    return [{"id": partition}]


def double(inputs, partition):
    return [{"id": r["id"] * 2} for r in inputs["source"]]


def build_pipeline() -> Pipeline:
    return Pipeline([
        Step("source", source, contract=CONTRACT),
        Step("double", double, deps=("source",), contract=CONTRACT),
    ])


# --- AC-001: per-step health from a manifest ---


def test_step_health_AC_001():
    manifest = run(build_pipeline(), partitions=[1, 2, 3])
    report = observe(manifest, watermark=3)
    src = report.health_of("source")
    assert src is not None
    assert src.ok == 3
    assert src.failed == 0
    assert src.latest_ok_partition == 3
    assert src.max_attempts == 1


# --- AC-002: freshness against a watermark ---


def test_freshness_AC_002():
    manifest = run(build_pipeline(), partitions=[1, 2])  # latest ok = 2
    fresh = observe(manifest, watermark=2)
    assert fresh.health_of("double").fresh is True
    assert fresh.freshness_breaches == []

    stale = observe(manifest, watermark=5)  # expected to reach 5, only at 2
    assert stale.health_of("double").fresh is False
    assert "double" in stale.freshness_breaches
    assert stale.status() == "degraded"


# --- AC-003: data-downtime detection ---


def test_downtime_AC_003():
    # A contract-violating step fails its partition -> downtime.
    def bad(inputs, partition):
        return [{"id": None}]  # required id null

    manifest = run(Pipeline([Step("s", bad, contract=CONTRACT)]), partitions=[1])
    report = observe(manifest, watermark=1)
    assert report.health_of("s").downtime is True
    assert "s" in report.downtime_steps
    assert report.sla_ok is False

    # A clean run has no downtime.
    clean = observe(run(build_pipeline(), partitions=[1]), watermark=1)
    assert clean.downtime_steps == []


# --- AC-004: SLA verdict + lineage from the pipeline ---


def test_sla_and_lineage_AC_004():
    pipe = build_pipeline()
    manifest = run(pipe, partitions=[1, 2, 3])
    report = observe(manifest, watermark=3, pipeline=pipe, max_attempts_sla=1)
    assert report.sla_ok is True
    assert report.status() == "healthy"
    # Lineage reflects the DAG dependencies.
    assert report.lineage["double"] == ["source"]
    assert report.lineage["source"] == []


# --- AC-005: deterministic ---


def test_deterministic_AC_005():
    pipe = build_pipeline()
    m = run(pipe, partitions=[1, 2, 3])
    a = observe(m, watermark=3, pipeline=pipe)
    b = observe(m, watermark=3, pipeline=pipe)
    assert a == b


# --- reuse check: observability reads a backfill manifest too ---


def test_reads_backfill_manifest():
    pipe = build_pipeline()
    state = {}
    run(pipe, partitions=[1], state=state)
    backfilled = backfill(pipe, partitions=[1, 2, 3], state=state)
    report = observe(backfilled, watermark=3)
    # Backfill ran only partitions 2 and 3.
    assert report.health_of("source").latest_ok_partition == 3
