"""Acceptance tests for spec 0021 — model/signal monitoring.

Each test is named for the acceptance criterion it covers (see
``specs/0021-signal-monitoring/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.alerting import AlertPolicy, evaluate_policies, route, Routing
from quantsmith.pipelines.signal_monitoring import (
    MonitorThresholds,
    monitor_signal,
)

REFERENCE = [0.01, -0.02, 0.03, 0.00, -0.01, 0.02, 0.01, -0.01]


# --- AC-001: health metrics computed ---


def test_health_metrics_AC_001():
    stable = [0.011, -0.019, 0.031, 0.001, -0.009, 0.021, 0.011, -0.009]
    health = monitor_signal(REFERENCE, stable, baseline_ic=0.05, live_ic=0.049)
    assert health.healthy is True
    assert health.breaches == []
    assert health.drift >= 0.0 and health.calibration >= 0.0


# --- AC-002: breaches flagged against thresholds ---


def test_breaches_flagged_AC_002():
    # Large positive shift -> drift + calibration breach; big IC drop -> decay breach.
    shifted = [x + 0.5 for x in REFERENCE]
    health = monitor_signal(REFERENCE, shifted, baseline_ic=0.05, live_ic=-0.03)
    assert health.healthy is False
    kinds = " ".join(health.breaches)
    assert "calibration" in kinds
    assert "decay" in kinds


# --- AC-003: monitoring emits observations the alerting engine evaluates ---


def test_feeds_alerting_AC_003():
    shifted = [x + 0.5 for x in REFERENCE]
    health = monitor_signal(REFERENCE, shifted, baseline_ic=0.05, live_ic=-0.03)
    policies = [
        AlertPolicy("decay-high", "decay", "max", threshold=0.02, severity="critical"),
        AlertPolicy("calib-high", "calibration", "max", threshold=0.05, severity="warning"),
    ]
    alerts = evaluate_policies(policies, health.observations())
    routed = route(alerts, Routing(escalate_at="critical"))
    rules = {r.alert.rule_id for r in routed}
    assert "decay-high" in rules
    assert any(r.escalated for r in routed if r.alert.severity == "critical")


# --- AC-004: regime shift detected ---


def test_regime_shift_AC_004():
    calm = [0.01, -0.01, 0.01, -0.01, 0.01, -0.01]
    volatile = [0.10, -0.10, 0.10, -0.10, 0.10, -0.10]  # ~10x vol
    health = monitor_signal(calm, volatile, baseline_ic=0.05, live_ic=0.05,
                            thresholds=MonitorThresholds(regime=0.5))
    assert health.regime_shift > 0.5
    assert any("regime" in b for b in health.breaches)


# --- AC-005: deterministic ---


def test_deterministic_AC_005():
    a = monitor_signal(REFERENCE, REFERENCE, 0.05, 0.05)
    b = monitor_signal(REFERENCE, REFERENCE, 0.05, 0.05)
    assert a == b
