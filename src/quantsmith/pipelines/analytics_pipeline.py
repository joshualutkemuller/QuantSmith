"""Reference pipeline for spec 0010 — end-to-end analytics pipeline.

This module makes the ``0010-analytics-pipeline`` spec *executable* and ties the
whole **Data Analyst** chain together into one deterministic, standard-library-only
runtime: query -> prepare -> profile -> metrics -> quality guard -> report.

It reuses the governed metrics layer from spec ``0008`` so the report's numbers come
from a single source of truth rather than an ad-hoc recomputation, and it produces a
report artifact carrying provenance. The pipeline is the runnable counterpart of the
analytics agents (`sql-integration-agent`, `data-prep-agent`, `eda-specialist-agent`,
`analytics/metrics_semantic_layer`, `quality-guard-agent`, `reporting-agent`).

Guarantees held by construction:

* REQ-001 / AC-001 — one call runs the chain from a source to a report.
* REQ-002 / AC-002 — preparation dedups, types, and profiles the rows.
* REQ-003 / AC-003 — metric values are computed through the semantic layer, so the
  report agrees with the governed layer exactly.
* REQ-004 / AC-004 — a failing quality check blocks the report with findings.
* REQ-005 / AC-005 — the report carries provenance (source, period, row counts,
  metric definitions used).
* NFR-001 / AC-006 — the whole run is deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from .metrics_semantic_layer import Fact, GovernanceError, SemanticLayer

Row = Dict[str, object]


# ---------------------------------------------------------------------------
# Source & query
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Table:
    """An in-memory source table (the reference stand-in for a warehouse query)."""

    name: str
    rows: Sequence[Row] = field(default_factory=tuple)


def run_query(table: Table, where: Optional[Dict[str, object]] = None) -> List[Row]:
    """Return rows from the table, optionally filtered by exact-match predicates.

    A deterministic stand-in for `sql-integration-agent`; real deployments swap in a
    parameterized warehouse query behind the same interface.
    """
    rows = list(table.rows)
    if where:
        rows = [r for r in rows if all(r.get(k) == v for k, v in where.items())]
    return rows


# ---------------------------------------------------------------------------
# Preparation & profiling
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FactSchema:
    """How a source row maps onto a governed ``Fact``."""

    period_field: str
    dim_fields: Sequence[str] = ()
    measure_fields: Sequence[str] = ()


@dataclass(frozen=True)
class PreparedData:
    facts: List[Fact]
    profile: Dict[str, object]


def prepare(rows: Sequence[Row], schema: FactSchema) -> PreparedData:
    """Clean, deduplicate, type, and profile rows into governed facts.

    The reference stand-in for `data-prep-agent` + `data_quality`. It removes exact
    duplicate rows, records missingness per field, and converts rows to ``Fact``
    objects. Rows missing the period field are dropped and counted.
    """
    fields = [schema.period_field, *schema.dim_fields, *schema.measure_fields]
    missing: Dict[str, int] = {f: 0 for f in fields}

    seen = set()
    unique: List[Row] = []
    duplicates = 0
    for r in rows:
        key = tuple((f, r.get(f)) for f in fields)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(r)

    facts: List[Fact] = []
    dropped = 0
    for r in unique:
        for f in fields:
            if r.get(f) is None:
                missing[f] += 1
        if r.get(schema.period_field) is None:
            dropped += 1
            continue
        facts.append(
            Fact(
                period=int(r[schema.period_field]),
                dims={d: str(r.get(d)) for d in schema.dim_fields if r.get(d) is not None},
                measures={
                    m: float(r[m]) for m in schema.measure_fields if r.get(m) is not None
                },
            )
        )

    profile = {
        "n_input": len(rows),
        "n_unique": len(unique),
        "n_duplicates_removed": duplicates,
        "n_dropped_missing_period": dropped,
        "n_facts": len(facts),
        "missing": missing,
    }
    return PreparedData(facts=facts, profile=profile)


def profile_facts(facts: Sequence[Fact], measure: Optional[str] = None) -> Dict[str, object]:
    """Lightweight EDA summary (the reference stand-in for `eda-specialist-agent`)."""
    summary: Dict[str, object] = {"n": len(facts), "periods": sorted({f.period for f in facts})}
    if measure is not None:
        values = [f.measures[measure] for f in facts if measure in f.measures]
        if values:
            summary[measure] = {
                "count": len(values),
                "sum": sum(values),
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values),
            }
    return summary


# ---------------------------------------------------------------------------
# Quality guard & report
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QualityResult:
    ok: bool
    findings: List[str]


@dataclass(frozen=True)
class Report:
    metric: str
    value: object  # scalar, {slice: value}, or None when blocked
    quality: QualityResult
    profile: Dict[str, object]
    eda: Dict[str, object]
    provenance: Dict[str, object]

    @property
    def status(self) -> str:
        return "ok" if self.quality.ok else "blocked"


def run_pipeline(
    table: Table,
    layer: SemanticLayer,
    metric: str,
    schema: FactSchema,
    period: Optional[int] = None,
    group_by: Optional[str] = None,
    where: Optional[Dict[str, object]] = None,
) -> Report:
    """Run the Data Analyst chain end-to-end and return a governed report.

    query -> prepare -> profile -> metric (via the semantic layer) -> quality guard
    -> report. The report is "blocked" (value ``None``) when a quality check fails.
    """
    rows = run_query(table, where=where)
    prepared = prepare(rows, schema)

    findings: List[str] = []

    # Governance: the metric must be defined in the semantic layer (spec 0008).
    metric_defined = True
    definition = None
    try:
        definition = layer.definition(metric)
    except GovernanceError as exc:
        metric_defined = False
        findings.append(f"ungoverned metric: {exc}")

    if not prepared.facts:
        findings.append("empty result: no facts after query and preparation")

    value: object = None
    if metric_defined and prepared.facts:
        value = layer.compute(metric, prepared.facts, period=period, group_by=group_by)
        # Reconciliation guard for additive metrics sliced by a dimension.
        if group_by is not None and definition is not None and definition.kind == "measure" \
                and definition.agg in ("sum", "count"):
            total = layer.compute(metric, prepared.facts, period=period)
            sliced = sum(v for v in value.values())  # type: ignore[union-attr]
            if abs(sliced - total) > 1e-9:
                findings.append(
                    f"reconciliation failed: slices {sliced} != total {total}"
                )

    measure = definition.source if (definition and definition.kind == "measure") else None
    eda = profile_facts(prepared.facts, measure=measure)

    provenance = {
        "source": table.name,
        "period": period,
        "group_by": group_by,
        "where": where or {},
        "n_input_rows": prepared.profile["n_input"],
        "n_facts": prepared.profile["n_facts"],
        "metrics_used": [metric] if metric_defined else [],
        "definition": {
            "owner": definition.owner,
            "grain": definition.grain,
            "kind": definition.kind,
        } if definition is not None else None,
    }

    quality = QualityResult(ok=not findings, findings=findings)
    return Report(
        metric=metric,
        value=value,
        quality=quality,
        profile=prepared.profile,
        eda=eda,
        provenance=provenance,
    )
