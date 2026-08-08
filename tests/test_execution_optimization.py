"""Acceptance tests for spec 0012 — optimal execution scheduling.

Each test is named for the acceptance criterion it covers (see
``specs/0012-execution-scheduling/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import math

from quantsmith.pipelines.execution_optimization import optimal_schedule

X = 10000.0
N = 10
ETA = 0.01
GAMMA = 0.001
SIGMA = 0.02
TAU = 1.0


# --- AC-001: schedule shape (N trades, N+1 holdings from X to 0) ---


def test_schedule_shape_AC_001():
    s = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=1e-6, tau=TAU)
    assert len(s.trades) == N
    assert len(s.holdings) == N + 1
    assert s.holdings[0] == X
    assert s.holdings[-1] == 0.0


# --- AC-002: the schedule fully liquidates ---


def test_full_liquidation_AC_002():
    s = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.001, tau=TAU)
    assert math.isclose(sum(s.trades), X, rel_tol=1e-9)
    assert math.isclose(s.holdings[-1], 0.0, abs_tol=1e-9)


# --- AC-003: TWAP at zero risk aversion; front-loaded when positive ---


def test_twap_vs_frontloaded_AC_003():
    twap = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.0, tau=TAU)
    for n in twap.trades:
        assert math.isclose(n, X / N, rel_tol=1e-9)

    aggressive = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.01, tau=TAU)
    # Front-loaded: the first trade is larger than the last.
    assert aggressive.trades[0] > aggressive.trades[-1]


# --- AC-004: risk aversion trades expected cost against variance ---


def test_cost_variance_tradeoff_AC_004():
    patient = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=1e-5, tau=TAU)
    aggressive = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.05, tau=TAU)
    # More aggressive -> lower variance, higher expected cost.
    assert aggressive.cost_variance() < patient.cost_variance()
    assert aggressive.expected_cost() > patient.expected_cost()


# --- AC-005: holdings are monotone non-increasing and non-negative ---


def test_holdings_monotone_nonneg_AC_005():
    s = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.02, tau=TAU)
    for a, b in zip(s.holdings, s.holdings[1:]):
        assert b <= a + 1e-9
        assert b >= -1e-9
    for n in s.trades:
        assert n >= -1e-9  # a pure liquidation never buys


# --- AC-006: deterministic ---


def test_deterministic_AC_006():
    a = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.01, tau=TAU)
    b = optimal_schedule(X, N, ETA, GAMMA, SIGMA, risk_aversion=0.01, tau=TAU)
    assert a == b
