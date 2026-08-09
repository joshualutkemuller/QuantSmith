"""Reference pipeline for spec 0020 — alerting (policy evaluation + routing).

Turns monitoring observations into actionable, routed notifications without coupling
detection to a delivery vendor: evaluate alert policies (threshold and missing-data
rules) into alerts, then route them — deduplicate, suppress muted rules, assign an
owner and channel, and escalate high-severity alerts. Delivery itself is the
`adapters/alert_delivery/` contract's job; this produces the routed payloads.
Standard-library only and deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set

SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2}


@dataclass(frozen=True)
class Observation:
    """A monitored value (``value`` is None when the metric is missing)."""

    metric: str
    value: Optional[float] = None


@dataclass(frozen=True)
class AlertPolicy:
    """A rule evaluated against observations.

    ``kind`` is ``max`` (fire when value > threshold), ``min`` (value < threshold), or
    ``missing`` (fire when the metric has no non-null observation).
    """

    rule_id: str
    metric: str
    kind: str
    threshold: Optional[float] = None
    severity: str = "warning"

    def __post_init__(self) -> None:
        if self.kind not in ("max", "min", "missing"):
            raise ValueError(f"unknown policy kind '{self.kind}'")
        if self.kind in ("max", "min") and self.threshold is None:
            raise ValueError(f"policy '{self.rule_id}' needs a threshold")
        if self.severity not in SEVERITY_ORDER:
            raise ValueError(f"unknown severity '{self.severity}'")


@dataclass(frozen=True)
class Alert:
    rule_id: str
    metric: str
    severity: str
    dedup_key: str
    message: str
    value: Optional[float] = None


def evaluate_policies(
    policies: Sequence[AlertPolicy],
    observations: Sequence[Observation],
) -> List[Alert]:
    """Fire an alert for each policy breach. Deterministic (policy order preserved)."""
    by_metric: Dict[str, List[float]] = {}
    for o in observations:
        if o.value is not None:
            by_metric.setdefault(o.metric, []).append(o.value)

    alerts: List[Alert] = []
    for p in policies:
        values = by_metric.get(p.metric, [])
        dedup = f"{p.rule_id}:{p.metric}"
        if p.kind == "missing":
            if not values:
                alerts.append(Alert(p.rule_id, p.metric, p.severity, dedup,
                                     f"{p.metric} missing (no data)"))
            continue
        for v in values:
            breach = (p.kind == "max" and v > p.threshold) or \
                     (p.kind == "min" and v < p.threshold)
            if breach:
                alerts.append(Alert(
                    p.rule_id, p.metric, p.severity, dedup,
                    f"{p.metric}={v} breaches {p.kind} {p.threshold}", value=v))
    return alerts


@dataclass(frozen=True)
class Routing:
    """How alerts are owned, channelled, suppressed, and escalated."""

    owners: Dict[str, str] = field(default_factory=dict)        # rule_id -> owner
    channels: Dict[str, str] = field(default_factory=dict)      # severity -> channel
    suppressed: Set[str] = field(default_factory=set)           # muted rule_ids
    escalate_at: str = "critical"                               # severity that pages
    default_owner: str = "unassigned"
    default_channel: str = "email"


@dataclass(frozen=True)
class RoutedAlert:
    alert: Alert
    owner: str
    channel: str
    escalated: bool
    count: int             # how many raw alerts collapsed into this one


def route(alerts: Sequence[Alert], routing: Routing) -> List[RoutedAlert]:
    """Deduplicate, suppress, assign owner/channel, and escalate.

    Alerts sharing a ``dedup_key`` collapse to one (the highest-severity instance),
    carrying a count. Suppressed rules are dropped. High-severity alerts are escalated.
    """
    # Deduplicate by key, keeping the highest-severity instance and a count.
    groups: Dict[str, List[Alert]] = {}
    order: List[str] = []
    for a in alerts:
        if a.dedup_key not in groups:
            groups[a.dedup_key] = []
            order.append(a.dedup_key)
        groups[a.dedup_key].append(a)

    routed: List[RoutedAlert] = []
    for key in order:
        members = groups[key]
        chosen = max(members, key=lambda a: SEVERITY_ORDER[a.severity])
        if chosen.rule_id in routing.suppressed:
            continue
        owner = routing.owners.get(chosen.rule_id, routing.default_owner)
        channel = routing.channels.get(chosen.severity, routing.default_channel)
        escalated = SEVERITY_ORDER[chosen.severity] >= SEVERITY_ORDER[routing.escalate_at]
        routed.append(RoutedAlert(
            alert=chosen, owner=owner, channel=channel,
            escalated=escalated, count=len(members)))
    return routed
