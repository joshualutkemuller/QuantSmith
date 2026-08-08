"""Reference pipeline for spec 0011 — data-pipeline orchestration.

This module makes the ``0011-data-pipeline-orchestration`` spec *executable* and is
the first runtime for the **Data Engineer** role. It is a deterministic,
standard-library-only DAG runner that captures the core data-engineering concerns the
"planned" nodes share: a DAG of steps with declared dependencies, a data contract per
step output, idempotent partitioned execution, retries with a max attempt count,
backfill of only the missing partitions, and a run manifest for observability.

Guarantees held by construction:

* REQ-001 / NFR-002 / AC-001 — steps run in dependency (topological) order; cycles and
  missing dependencies are rejected at construction.
* REQ-002 / AC-002 — each step's output is validated against its data contract; a
  violation fails the step and is recorded (not retried).
* REQ-003 / AC-003 — a completed partition is skipped unless forced; a forced re-run
  reproduces the same output.
* REQ-004 / AC-004 — a transient failure is retried up to ``max_attempts``; a
  persistent failure is recorded as failed.
* REQ-005 / NFR-003 / AC-005 — backfill runs only missing partitions; the manifest
  records per-(step, partition) status.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, FrozenSet, List, Optional, Sequence, Tuple

Row = Dict[str, object]
Partition = int
# A step function receives its upstream outputs and the partition, and returns rows.
StepFn = Callable[[Dict[str, List[Row]], Partition], List[Row]]


# ---------------------------------------------------------------------------
# Data contract — REQ-002
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DataContract:
    """A declared schema for a step's output: column types and required columns."""

    name: str
    columns: Dict[str, type]
    required: FrozenSet[str] = frozenset()

    def validate(self, rows: Sequence[Row]) -> List[str]:
        """Return a list of contract violations (empty when the rows conform)."""
        violations: List[str] = []
        for i, row in enumerate(rows):
            for col, typ in self.columns.items():
                if col not in row:
                    violations.append(f"row {i}: missing column '{col}'")
                    continue
                val = row[col]
                if val is None:
                    if col in self.required:
                        violations.append(f"row {i}: required column '{col}' is null")
                    continue
                if not isinstance(val, typ):
                    violations.append(
                        f"row {i}: column '{col}' expected {typ.__name__}, "
                        f"got {type(val).__name__}"
                    )
        return violations


# ---------------------------------------------------------------------------
# Steps & pipeline (DAG) — REQ-001
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step:
    name: str
    fn: StepFn
    deps: Tuple[str, ...] = ()
    contract: Optional[DataContract] = None
    max_attempts: int = 1


class Pipeline:
    """A DAG of steps; construction validates dependencies and rejects cycles."""

    def __init__(self, steps: Sequence[Step]) -> None:
        self.steps: Dict[str, Step] = {s.name: s for s in steps}
        if len(self.steps) != len(steps):
            raise ValueError("duplicate step name")
        self.order: List[str] = self._toposort()

    def _toposort(self) -> List[str]:
        # Kahn's algorithm with deterministic ordering.
        for name, step in self.steps.items():
            for d in step.deps:
                if d not in self.steps:
                    raise ValueError(f"step '{name}' depends on unknown step '{d}'")
        indegree = {n: 0 for n in self.steps}
        for step in self.steps.values():
            for _ in step.deps:
                indegree[step.name] += 1
        ready = sorted(n for n, d in indegree.items() if d == 0)
        order: List[str] = []
        while ready:
            n = ready.pop(0)
            order.append(n)
            for m, step in self.steps.items():
                if n in step.deps:
                    indegree[m] -= 1
                    if indegree[m] == 0:
                        ready.append(m)
            ready.sort()
        if len(order) != len(self.steps):
            raise ValueError("pipeline has a cycle")
        return order


# ---------------------------------------------------------------------------
# Results, manifest & execution — REQ-003/004/005
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StepResult:
    step: str
    partition: Partition
    status: str  # "ok" | "failed" | "skipped"
    attempts: int
    rows: List[Row]
    violations: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class RunManifest:
    results: List[StepResult]

    def status_of(self, step: str, partition: Partition) -> Optional[str]:
        for r in self.results:
            if r.step == step and r.partition == partition:
                return r.status
        return None

    def partitions_run(self) -> List[Partition]:
        return sorted({r.partition for r in self.results})

    def ok(self) -> bool:
        return all(r.status in ("ok", "skipped") for r in self.results)


PipelineState = Dict[Tuple[str, Partition], StepResult]


def run(
    pipeline: Pipeline,
    partitions: Sequence[Partition],
    state: Optional[PipelineState] = None,
    force: bool = False,
) -> RunManifest:
    """Execute the pipeline over the partitions, idempotently and with retries.

    A completed ``(step, partition)`` in ``state`` is skipped unless ``force``. A
    step failure (persistent error or contract violation) stops that partition's
    downstream steps; other partitions still run. ``state`` is updated in place.
    """
    if state is None:
        state = {}
    results: List[StepResult] = []

    for partition in partitions:
        outputs: Dict[str, List[Row]] = {}
        for name in pipeline.order:
            step = pipeline.steps[name]
            key = (name, partition)

            if not force and key in state and state[key].status == "ok":
                prev = state[key]
                outputs[name] = prev.rows
                results.append(
                    StepResult(name, partition, "skipped", prev.attempts, prev.rows)
                )
                continue

            # A step whose dependency did not produce output cannot run.
            if any(d not in outputs for d in step.deps):
                break

            inputs = {d: outputs[d] for d in step.deps}
            result = _run_step(step, inputs, partition)
            results.append(result)
            if result.status == "ok":
                outputs[name] = result.rows
                state[key] = result
            else:
                break  # downstream steps for this partition are blocked

    return RunManifest(results)


def _run_step(step: Step, inputs: Dict[str, List[Row]], partition: Partition) -> StepResult:
    attempts = 0
    while attempts < max(step.max_attempts, 1):
        attempts += 1
        try:
            rows = list(step.fn(inputs, partition))
        except Exception:
            continue  # transient failure -> retry
        violations = step.contract.validate(rows) if step.contract else []
        if violations:
            return StepResult(step.name, partition, "failed", attempts, rows, violations)
        return StepResult(step.name, partition, "ok", attempts, rows)
    return StepResult(step.name, partition, "failed", attempts, [], ["step raised on every attempt"])


def _partition_complete(pipeline: Pipeline, partition: Partition, state: PipelineState) -> bool:
    return all(
        state.get((name, partition), None) is not None
        and state[(name, partition)].status == "ok"
        for name in pipeline.order
    )


def backfill(
    pipeline: Pipeline,
    partitions: Sequence[Partition],
    state: PipelineState,
) -> RunManifest:
    """Run only the partitions that are not already complete in ``state``."""
    missing = [p for p in partitions if not _partition_complete(pipeline, p, state)]
    return run(pipeline, missing, state=state)
