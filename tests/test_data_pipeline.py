"""Acceptance tests for spec 0011 — data-pipeline orchestration.

Each test is named for the acceptance criterion it covers (see
``specs/0011-data-pipeline-orchestration/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import pytest

from quantsmith.pipelines.data_pipeline import (
    DataContract,
    Pipeline,
    Step,
    backfill,
    run,
)

CONTRACT = DataContract(
    name="rows",
    columns={"id": int, "value": float},
    required=frozenset({"id"}),
)


def source_step(inputs, partition):
    return [{"id": partition, "value": float(partition * 10)}]


def double_step(inputs, partition):
    upstream = inputs["source"]
    return [{"id": r["id"], "value": r["value"] * 2.0} for r in upstream]


def build_pipeline() -> Pipeline:
    return Pipeline([
        Step("source", source_step, contract=CONTRACT),
        Step("double", double_step, deps=("source",), contract=CONTRACT),
    ])


# --- AC-001: topological order; downstream sees upstream; cycles rejected ---


def test_topological_order_AC_001():
    manifest = run(build_pipeline(), partitions=[1])
    # double consumed source's output (1*10*2 = 20).
    double = next(r for r in manifest.results if r.step == "double")
    assert double.status == "ok"
    assert double.rows == [{"id": 1, "value": 20.0}]
    # source appears before double in the results order.
    steps_in_order = [r.step for r in manifest.results]
    assert steps_in_order.index("source") < steps_in_order.index("double")

    # A cycle is rejected at construction.
    with pytest.raises(ValueError):
        Pipeline([
            Step("a", source_step, deps=("b",)),
            Step("b", source_step, deps=("a",)),
        ])

    # A missing dependency is rejected.
    with pytest.raises(ValueError):
        Pipeline([Step("a", source_step, deps=("ghost",))])


# --- AC-002: contract validation fails a bad output ---


def test_contract_validation_AC_002():
    def bad_step(inputs, partition):
        return [{"id": None, "value": 1.0}]  # required id is null

    manifest = run(Pipeline([Step("s", bad_step, contract=CONTRACT)]), partitions=[1])
    res = manifest.results[0]
    assert res.status == "failed"
    assert any("required column 'id'" in v for v in res.violations)

    def wrong_type(inputs, partition):
        return [{"id": "x", "value": 1.0}]  # id should be int

    m2 = run(Pipeline([Step("s", wrong_type, contract=CONTRACT)]), partitions=[1])
    assert m2.results[0].status == "failed"
    assert any("expected int" in v for v in m2.results[0].violations)


# --- AC-003: idempotent skip; forced re-run reproduces output ---


def test_idempotency_AC_003():
    pipe = build_pipeline()
    state = {}
    first = run(pipe, partitions=[1], state=state)
    assert all(r.status == "ok" for r in first.results)

    # Second run over the same partition skips completed steps.
    second = run(pipe, partitions=[1], state=state)
    assert all(r.status == "skipped" for r in second.results)

    # Forced re-run recomputes and yields identical rows.
    forced = run(pipe, partitions=[1], state=state, force=True)
    assert all(r.status == "ok" for r in forced.results)
    assert [r.rows for r in forced.results] == [r.rows for r in first.results]


# --- AC-004: retries on transient failure; persistent failure recorded ---


def test_retries_AC_004():
    calls = {"n": 0}

    def flaky(inputs, partition):
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("transient")
        return [{"id": 1, "value": 1.0}]

    m = run(Pipeline([Step("s", flaky, contract=CONTRACT, max_attempts=3)]), partitions=[1])
    assert m.results[0].status == "ok"
    assert m.results[0].attempts == 3

    def always_fail(inputs, partition):
        raise RuntimeError("boom")

    m2 = run(Pipeline([Step("s", always_fail, max_attempts=3)]), partitions=[1])
    assert m2.results[0].status == "failed"
    assert m2.results[0].attempts == 3


# --- AC-005: backfill runs only missing partitions; manifest per partition ---


def test_backfill_AC_005():
    pipe = build_pipeline()
    state = {}
    run(pipe, partitions=[1], state=state)  # partition 1 complete

    manifest = backfill(pipe, partitions=[1, 2, 3], state=state)
    # Only partitions 2 and 3 ran; 1 was already complete and skipped by backfill.
    assert manifest.partitions_run() == [2, 3]
    assert manifest.status_of("double", 2) == "ok"
    assert manifest.status_of("source", 3) == "ok"


# --- AC-006: deterministic ---


def test_deterministic_AC_006():
    a = run(build_pipeline(), partitions=[1, 2, 3])
    b = run(build_pipeline(), partitions=[1, 2, 3])
    assert [(r.step, r.partition, r.status, r.rows) for r in a.results] == \
           [(r.step, r.partition, r.status, r.rows) for r in b.results]
