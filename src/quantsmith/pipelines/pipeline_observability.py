"""Reference pipeline for spec 0019 — data-pipeline observability.

Consumes the ``RunManifest`` that the ``0011`` DAG runner emits and turns it into an
observability read: per-step health, freshness against a watermark, data-downtime
detection, an SLA verdict, and a lineage view from the pipeline's dependencies. This is
the Data Engineer observability node — it reuses ``0011`` rather than re-orchestrating.
Standard-library only and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from .data_pipeline import Pipeline, RunManifest

# A watermark / attempts SLA may be one value for all steps, or per-step via a dict.
Watermark = Union[int, Dict[str, int]]
AttemptsSLA = Optional[Union[int, Dict[str, int]]]


def _per_step(value, step: str):
    """Resolve a scalar-or-dict threshold for a step (None when a dict omits it)."""
    if isinstance(value, dict):
        return value.get(step)
    return value


@dataclass(frozen=True)
class StepHealth:
    step: str
    latest_ok_partition: Optional[int]
    ok: int
    failed: int
    skipped: int
    max_attempts: int
    fresh: bool          # latest_ok_partition >= watermark
    downtime: bool       # has an unrecovered failed partition


@dataclass(frozen=True)
class ObservabilityReport:
    steps: List[StepHealth]
    freshness_breaches: List[str]        # step names behind the watermark
    downtime_steps: List[str]            # step names with a failed partition
    sla_ok: bool
    sla_breaches: List[str]
    lineage: Dict[str, List[str]] = field(default_factory=dict)

    def status(self) -> str:
        return "healthy" if self.sla_ok else "degraded"

    def health_of(self, step: str) -> Optional[StepHealth]:
        for s in self.steps:
            if s.step == step:
                return s
        return None


def observe(
    manifest: RunManifest,
    watermark: Watermark,
    pipeline: Optional[Pipeline] = None,
    max_attempts_sla: AttemptsSLA = None,
) -> ObservabilityReport:
    """Turn a run manifest into an observability report.

    ``watermark`` is the partition each step is expected to have reached; a step whose
    latest successful partition is behind it is *stale*. A step with a failed partition
    is in *downtime*. The SLA passes when no step is stale, none is in downtime, and no
    step exceeded ``max_attempts_sla`` (when given).

    ``watermark`` and ``max_attempts_sla`` accept either one value for all steps or a
    per-step ``{step: value}`` dict; a step omitted from a dict has no threshold (its
    freshness only requires that it produced data at all).
    """
    # Group results by step, preserving first-seen order.
    order: List[str] = []
    ok: Dict[str, List[int]] = {}
    failed: Dict[str, List[int]] = {}
    skipped: Dict[str, int] = {}
    attempts: Dict[str, int] = {}
    for r in manifest.results:
        if r.step not in order:
            order.append(r.step)
            ok[r.step], failed[r.step], skipped[r.step], attempts[r.step] = [], [], 0, 0
        if r.status == "ok":
            ok[r.step].append(r.partition)
        elif r.status == "failed":
            failed[r.step].append(r.partition)
        elif r.status == "skipped":
            skipped[r.step] += 1
        attempts[r.step] = max(attempts[r.step], r.attempts)

    steps: List[StepHealth] = []
    freshness_breaches: List[str] = []
    downtime_steps: List[str] = []
    sla_breaches: List[str] = []

    for name in order:
        latest_ok = max(ok[name]) if ok[name] else None
        wm = _per_step(watermark, name)
        if wm is None:
            fresh = latest_ok is not None            # no watermark: just needs data
        else:
            fresh = latest_ok is not None and latest_ok >= wm
        downtime = len(failed[name]) > 0
        steps.append(
            StepHealth(
                step=name,
                latest_ok_partition=latest_ok,
                ok=len(ok[name]),
                failed=len(failed[name]),
                skipped=skipped[name],
                max_attempts=attempts[name],
                fresh=fresh,
                downtime=downtime,
            )
        )
        if not fresh:
            freshness_breaches.append(name)
            sla_breaches.append(f"{name}: stale (latest ok {latest_ok} < watermark {wm})")
        if downtime:
            downtime_steps.append(name)
            sla_breaches.append(f"{name}: downtime (failed partitions {sorted(failed[name])})")
        attempts_sla = _per_step(max_attempts_sla, name)
        if attempts_sla is not None and attempts[name] > attempts_sla:
            sla_breaches.append(f"{name}: {attempts[name]} attempts > SLA {attempts_sla}")

    lineage: Dict[str, List[str]] = {}
    if pipeline is not None:
        for name, step in pipeline.steps.items():
            lineage[name] = list(step.deps)

    return ObservabilityReport(
        steps=steps,
        freshness_breaches=freshness_breaches,
        downtime_steps=downtime_steps,
        sla_ok=not sla_breaches,
        sla_breaches=sla_breaches,
        lineage=lineage,
    )
