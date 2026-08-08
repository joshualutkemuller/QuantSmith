"""Reference pipeline for spec 0008 — metrics semantic layer.

This module makes the ``0008-metrics-semantic-layer`` spec *executable*. It is a
deterministic, standard-library-only reference for a governed metrics layer: the
single place a metric like "revenue" or "conversion rate" is defined, so every
dashboard and report computes it the same way.

The consistency guarantees hold by construction:

* REQ-001 / AC-001, AC-005 — each metric is defined exactly once; conflicting
  re-definitions and requests for undefined metrics raise ``GovernanceError``.
* REQ-002 / NFR-002 / AC-002 — a metric for a period uses only rows in that period.
* REQ-002 / NFR-003 / AC-003 — slicing by a declared dimension reconciles to the
  ungrouped total for additive metrics; an undeclared dimension is rejected.
* REQ-003 / AC-004 — derived (ratio) metrics divide two governed base measures over
  the same filtered rows, so numerator and denominator can never disagree.
* NFR-001 / AC-006 — computation is deterministic given the registry and the rows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple, Union

Number = float
MetricValue = Union[Number, Dict[Optional[str], Number]]

_AGGS = {"sum", "count", "mean"}


class GovernanceError(Exception):
    """Raised when a request or definition violates the semantic-layer contract."""


@dataclass(frozen=True)
class Fact:
    """One fact row: a period key, dimension values, and measure values."""

    period: int  # comparable period key, e.g. 202401 for Jan-2024
    dims: Dict[str, str] = field(default_factory=dict)
    measures: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricDefinition:
    """The single source of truth for one metric.

    A *measure* metric aggregates one measure (``source`` + ``agg``). A *ratio*
    metric divides two base measures (``numerator`` / ``denominator``, summed).
    """

    name: str
    owner: str
    grain: str
    dimensions: Tuple[str, ...] = ()
    source: Optional[str] = None
    agg: str = "sum"
    numerator: Optional[str] = None
    denominator: Optional[str] = None

    @property
    def kind(self) -> str:
        return "ratio" if self.numerator is not None else "measure"


class SemanticLayer:
    """A governed registry of metric definitions plus a consistent evaluator."""

    def __init__(self) -> None:
        self._defs: Dict[str, MetricDefinition] = {}

    # -- registration / governance -----------------------------------------

    def register(self, defn: MetricDefinition) -> MetricDefinition:
        """Register a metric definition, enforcing the governance contract.

        Re-registering the identical definition is idempotent; registering a
        *different* definition for an existing name is a governance error
        (single source of truth — REQ-001 / AC-001).
        """
        self._validate(defn)
        existing = self._defs.get(defn.name)
        if existing is not None and existing != defn:
            raise GovernanceError(
                f"metric '{defn.name}' already defined differently (single source of truth)"
            )
        self._defs[defn.name] = defn
        return defn

    def define(self, **kwargs) -> MetricDefinition:
        """Convenience: build a ``MetricDefinition`` and register it."""
        return self.register(MetricDefinition(**kwargs))

    def definition(self, name: str) -> MetricDefinition:
        if name not in self._defs:
            raise GovernanceError(f"undefined metric: {name}")
        return self._defs[name]

    @staticmethod
    def _validate(defn: MetricDefinition) -> None:
        if not defn.owner:
            raise GovernanceError(f"metric '{defn.name}' has no owner")
        if not defn.grain:
            raise GovernanceError(f"metric '{defn.name}' has no time grain")
        if defn.kind == "ratio":
            if not defn.numerator or not defn.denominator:
                raise GovernanceError(
                    f"ratio metric '{defn.name}' needs a numerator and a denominator"
                )
        else:
            if not defn.source:
                raise GovernanceError(f"measure metric '{defn.name}' needs a source measure")
            if defn.agg not in _AGGS:
                raise GovernanceError(
                    f"metric '{defn.name}' has unknown agg '{defn.agg}' (use {sorted(_AGGS)})"
                )

    # -- computation -------------------------------------------------------

    def compute(
        self,
        name: str,
        rows: Sequence[Fact],
        period: Optional[int] = None,
        group_by: Optional[str] = None,
    ) -> MetricValue:
        """Compute a metric value, consistently and point-in-time.

        ``period`` filters to rows in that period only (NFR-002 / AC-002).
        ``group_by`` must be a declared dimension of the metric (AC-003); it returns
        a dict of dimension value -> metric value.
        """
        defn = self.definition(name)
        if group_by is not None and group_by not in defn.dimensions:
            raise GovernanceError(
                f"dimension '{group_by}' is not declared for metric '{name}'"
            )

        rows = [r for r in rows if period is None or r.period == period]

        if group_by is None:
            return self._value(defn, rows)

        groups: Dict[Optional[str], List[Fact]] = {}
        for r in rows:
            groups.setdefault(r.dims.get(group_by), []).append(r)
        return {key: self._value(defn, g) for key, g in groups.items()}

    def _value(self, defn: MetricDefinition, rows: Sequence[Fact]) -> Number:
        if defn.kind == "ratio":
            num = self._aggregate("sum", defn.numerator, rows)
            den = self._aggregate("sum", defn.denominator, rows)
            return num / den if den != 0 else float("nan")
        return self._aggregate(defn.agg, defn.source, rows)

    @staticmethod
    def _aggregate(agg: str, measure: Optional[str], rows: Sequence[Fact]) -> Number:
        if agg == "count":
            return float(len(rows))
        values = [float(r.measures.get(measure, 0.0)) for r in rows]
        if not values:
            return 0.0
        if agg == "sum":
            return sum(values)
        if agg == "mean":
            return sum(values) / len(values)
        raise GovernanceError(f"unknown agg '{agg}'")
