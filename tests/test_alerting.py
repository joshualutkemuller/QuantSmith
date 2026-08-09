"""Acceptance tests for spec 0020 — alerting (policy evaluation + routing).

Each test is named for the acceptance criterion it covers (see
``specs/0020-alerting/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import pytest

from quantsmith.pipelines.alerting import (
    AlertPolicy,
    Observation,
    Routing,
    evaluate_policies,
    route,
)


POLICIES = [
    AlertPolicy("drift-high", "drift", "max", threshold=0.2, severity="warning"),
    AlertPolicy("decay-high", "decay", "max", threshold=0.02, severity="critical"),
    AlertPolicy("price-missing", "price", "missing", severity="critical"),
]


# --- AC-001: policy evaluation (threshold + missing) ---


def test_policy_evaluation_AC_001():
    obs = [Observation("drift", 0.35), Observation("decay", 0.005)]  # price absent
    alerts = evaluate_policies(POLICIES, obs)
    rules = {a.rule_id for a in alerts}
    assert "drift-high" in rules          # 0.35 > 0.2
    assert "decay-high" not in rules      # 0.005 !> 0.02
    assert "price-missing" in rules       # price has no observation

    # Within thresholds and present -> no alerts.
    calm = evaluate_policies(POLICIES, [Observation("drift", 0.1),
                                        Observation("decay", 0.0),
                                        Observation("price", 100.0)])
    assert calm == []


# --- AC-002: dedup + suppression ---


def test_dedup_and_suppression_AC_002():
    obs = [Observation("drift", 0.3), Observation("drift", 0.9)]  # two drift breaches
    alerts = evaluate_policies(POLICIES, obs)
    routed = route(alerts, Routing())
    drift_routed = [r for r in routed if r.alert.rule_id == "drift-high"]
    assert len(drift_routed) == 1                 # collapsed to one
    assert drift_routed[0].count == 2             # carries the dedup count

    # Suppressed rule is dropped.
    suppressed = route(alerts, Routing(suppressed={"drift-high"}))
    assert all(r.alert.rule_id != "drift-high" for r in suppressed)


# --- AC-003: owner/channel assignment + escalation ---


def test_routing_assignment_AC_003():
    obs = [Observation("decay", 0.5), Observation("price", 100.0)]  # critical decay breach
    alerts = evaluate_policies(POLICIES, obs)
    routing = Routing(
        owners={"decay-high": "quant-oncall"},
        channels={"critical": "pagerduty", "warning": "slack"},
    )
    routed = route(alerts, routing)
    decay = next(r for r in routed if r.alert.rule_id == "decay-high")
    assert decay.owner == "quant-oncall"
    assert decay.channel == "pagerduty"
    assert decay.escalated is True            # critical >= escalate_at


# --- AC-004: no secrets in alert payloads ---


def test_no_secrets_AC_004():
    from quantsmith.adapters.dashboard_render.result import contains_secret

    obs = [Observation("drift", 0.9)]
    for a in evaluate_policies(POLICIES, obs):
        assert not contains_secret(a.message)
        assert not contains_secret(a.rule_id)


# --- AC-005: deterministic ---


def test_deterministic_AC_005():
    obs = [Observation("drift", 0.3), Observation("decay", 0.1)]
    a = route(evaluate_policies(POLICIES, obs), Routing())
    b = route(evaluate_policies(POLICIES, obs), Routing())
    assert a == b


def test_policy_validation():
    with pytest.raises(ValueError):
        AlertPolicy("x", "m", "max")            # missing threshold
    with pytest.raises(ValueError):
        AlertPolicy("x", "m", "bogus", threshold=1)
    with pytest.raises(ValueError):
        AlertPolicy("x", "m", "max", threshold=1, severity="loud")
