"""Acceptance tests for spec 0007 — constrained portfolio construction.

Each test is named for the acceptance criterion it covers (see
``specs/0007-portfolio-construction/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.portfolio_construction import (
    ConstraintSet,
    diagnostics,
    portfolio_variance,
    solve_portfolio,
    turnover,
)

# A small, well-conditioned problem: 4 names, positive-definite covariance.
ALPHA = [0.02, 0.05, -0.01, 0.03]
COV = [
    [0.10, 0.02, 0.01, 0.00],
    [0.02, 0.12, 0.02, 0.01],
    [0.01, 0.02, 0.09, 0.02],
    [0.00, 0.01, 0.02, 0.11],
]
CONSTRAINTS = ConstraintSet(n=4, budget=1.0, lower=0.0, upper=0.5, gross_cap=1.0)
TOL = 1e-6


# --- AC-001: higher risk aversion does not increase variance ---


def test_risk_aversion_reduces_variance_AC_001():
    w_low = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=1.0)
    w_high = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=50.0)
    assert portfolio_variance(w_high, COV) <= portfolio_variance(w_low, COV) + TOL


# --- AC-002: returned weights satisfy budget, box, and gross cap ---


def test_constraints_satisfied_AC_002():
    w = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=10.0)
    # Box bounds.
    for wi in w:
        assert CONSTRAINTS.lower - TOL <= wi <= CONSTRAINTS.upper + TOL
    # Budget.
    assert abs(sum(w) - CONSTRAINTS.budget) <= 1e-6
    # Gross-exposure cap.
    assert sum(abs(wi) for wi in w) <= CONSTRAINTS.gross_cap + 1e-6


# --- AC-003: higher turnover penalty does not increase turnover ---


def test_turnover_penalty_reduces_turnover_AC_003():
    prior = [0.25, 0.25, 0.25, 0.25]
    w_free = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=10.0, w_prev=prior, lambda_to=0.0)
    w_sticky = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=10.0, w_prev=prior, lambda_to=50.0)
    assert turnover(w_sticky, prior) <= turnover(w_free, prior) + TOL


# --- AC-004: diagnostics emit objective, violation, and a sensitivity curve ---


def test_diagnostics_emitted_AC_004():
    w = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=10.0)
    report = diagnostics(w, ALPHA, COV, CONSTRAINTS, gamma=10.0)
    for key in ("objective", "max_violation", "gross_exposure", "turnover", "sensitivity"):
        assert key in report
    # Feasible solution -> negligible violation.
    assert report["max_violation"] <= 1e-6
    # Sensitivity curve is a non-empty list of (gamma, variance) pairs.
    assert isinstance(report["sensitivity"], list) and report["sensitivity"]
    for g, var in report["sensitivity"]:
        assert isinstance(g, float) and var >= 0.0
    # Variance should be (weakly) decreasing along an increasing gamma grid.
    variances = [var for _g, var in report["sensitivity"]]
    for a, b in zip(variances, variances[1:]):
        assert b <= a + 1e-6


# --- AC-005: the solve is reproducible ---


def test_solver_reproducible_AC_005():
    w1 = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=7.0, w_prev=[0.1, 0.2, 0.3, 0.4], lambda_to=3.0)
    w2 = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=7.0, w_prev=[0.1, 0.2, 0.3, 0.4], lambda_to=3.0)
    assert w1 == w2


def test_alpha_tilts_toward_higher_forecast():
    # Sanity: with low risk aversion, the highest-alpha name gets the most weight.
    w = solve_portfolio(ALPHA, COV, CONSTRAINTS, gamma=0.5)
    assert w[1] == max(w)  # name index 1 has the highest alpha (0.05)
