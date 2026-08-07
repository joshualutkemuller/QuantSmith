"""Reference pipeline for spec 0007 — constrained portfolio construction.

This module makes the ``0007-portfolio-construction`` spec *executable*. It solves a
convex mean-variance quadratic program with projection onto the feasible set, so
feasibility and reproducibility hold by construction. It is standard-library only
(no numpy/scipy), so the acceptance criteria run anywhere.

Objective (minimized):

    f(w) = -alpha . w + (gamma / 2) w^T Σ w + (lambda_to / 2) || w - w_prev ||^2

subject to ``sum(w) = budget``, ``lower ≤ w ≤ upper``, and a gross-exposure cap.
Expected returns (``alpha``) are the ``0006-ml-return-forecasting`` forecast as-of
the rebalance date; the covariance is a point-in-time estimate.

Correctness properties held by construction:

* REQ-002 / NFR-002 / AC-002 — projecting every step keeps weights feasible.
* REQ-001 / AC-001 — the risk penalty makes variance non-increasing in risk aversion.
* REQ-003 / AC-003 — the turnover penalty makes turnover non-increasing in its weight.
* NFR-001 / AC-005 — the solve is deterministic given its inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

Vector = Sequence[float]
Matrix = Sequence[Sequence[float]]


# ---------------------------------------------------------------------------
# Constraints — REQ-002
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConstraintSet:
    """Budget, per-name box bounds, and a gross-exposure cap."""

    n: int
    budget: float = 1.0
    lower: float = 0.0
    upper: float = 1.0
    gross_cap: float = 1.0

    def bounds(self) -> Tuple[List[float], List[float]]:
        return [self.lower] * self.n, [self.upper] * self.n

    def is_feasible(self, budget: float) -> bool:
        # A budget is reachable iff it lies within the aggregate box range.
        return self.lower * self.n - 1e-9 <= budget <= self.upper * self.n + 1e-9


# ---------------------------------------------------------------------------
# Solver — REQ-001 / REQ-003
# ---------------------------------------------------------------------------


def solve_portfolio(
    alpha: Vector,
    cov: Matrix,
    constraints: ConstraintSet,
    gamma: float = 5.0,
    w_prev: Optional[Vector] = None,
    lambda_to: float = 0.0,
    iterations: int = 4000,
    step: Optional[float] = None,
) -> List[float]:
    """Solve the constrained mean-variance QP by projected gradient descent.

    Deterministic: the initial point is the feasible projection of the equal-budget
    portfolio, and every update is a fixed arithmetic step followed by projection,
    so the same inputs always return the same weights (NFR-001 / AC-005).
    """
    n = constraints.n
    if len(alpha) != n:
        raise ValueError("alpha length must match constraints.n")
    if not constraints.is_feasible(constraints.budget):
        raise ValueError("budget is infeasible for the given box bounds")

    prev = list(w_prev) if w_prev is not None else [0.0] * n
    if len(prev) != n:
        raise ValueError("w_prev length must match constraints.n")

    # Deterministic feasible start: equal split of the budget, then projected.
    w = _project([constraints.budget / n] * n, constraints)

    lr = step if step is not None else _default_step(cov, gamma, lambda_to)
    for _ in range(iterations):
        grad = _objective_gradient(w, alpha, cov, gamma, prev, lambda_to)
        w = _project([wi - lr * gi for wi, gi in zip(w, grad)], constraints)
    return w


def _objective_gradient(
    w: Vector,
    alpha: Vector,
    cov: Matrix,
    gamma: float,
    w_prev: Vector,
    lambda_to: float,
) -> List[float]:
    n = len(w)
    cov_w = [sum(cov[i][j] * w[j] for j in range(n)) for i in range(n)]
    return [
        -alpha[i] + gamma * cov_w[i] + lambda_to * (w[i] - w_prev[i])
        for i in range(n)
    ]


def _default_step(cov: Matrix, gamma: float, lambda_to: float) -> float:
    n = len(cov)
    # Gershgorin bound on the largest eigenvalue of the Hessian gamma*Σ + lambda_to*I.
    max_row = max(sum(abs(cov[i][j]) for j in range(n)) for i in range(n)) if n else 0.0
    lipschitz = gamma * max_row + lambda_to
    return 1.0 / lipschitz if lipschitz > 0 else 0.1


# ---------------------------------------------------------------------------
# Projection onto {lower ≤ w ≤ upper, sum w = budget} — feasibility by construction
# ---------------------------------------------------------------------------


def _project(v: Vector, constraints: ConstraintSet) -> List[float]:
    """Euclidean projection onto the box-and-budget set via bisection on tau.

    ``w_i(tau) = clip(v_i - tau, lower, upper)``; find tau so ``sum w_i = budget``.
    """
    lower, upper, budget = constraints.lower, constraints.upper, constraints.budget

    def total(tau: float) -> float:
        return sum(min(max(vi - tau, lower), upper) for vi in v)

    lo = min(v) - upper
    hi = max(v) - lower
    for _ in range(100):  # bisection to a tight tolerance, deterministic
        mid = (lo + hi) / 2.0
        if total(mid) > budget:
            lo = mid
        else:
            hi = mid
    tau = (lo + hi) / 2.0
    w = [min(max(vi - tau, lower), upper) for vi in v]

    # Enforce the gross-exposure cap (long-only budget already caps gross at budget).
    gross = sum(abs(wi) for wi in w)
    if gross > constraints.gross_cap + 1e-9 and gross > 0:
        scale = constraints.gross_cap / gross
        w = [wi * scale for wi in w]
    return w


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------


def portfolio_variance(w: Vector, cov: Matrix) -> float:
    n = len(w)
    return sum(w[i] * cov[i][j] * w[j] for i in range(n) for j in range(n))


def portfolio_alpha(w: Vector, alpha: Vector) -> float:
    return sum(wi * ai for wi, ai in zip(w, alpha))


def turnover(w: Vector, w_prev: Optional[Vector]) -> float:
    if w_prev is None:
        return sum(abs(wi) for wi in w)
    return sum(abs(wi - pi) for wi, pi in zip(w, w_prev))


def gross_exposure(w: Vector) -> float:
    return sum(abs(wi) for wi in w)


# ---------------------------------------------------------------------------
# Diagnostics — REQ-004 / AC-004
# ---------------------------------------------------------------------------


def diagnostics(
    w: Vector,
    alpha: Vector,
    cov: Matrix,
    constraints: ConstraintSet,
    gamma: float = 5.0,
    w_prev: Optional[Vector] = None,
    lambda_to: float = 0.0,
    gamma_grid: Optional[Sequence[float]] = None,
) -> Dict[str, object]:
    """Objective, maximum constraint violation, and a risk-aversion sensitivity curve."""
    prev = list(w_prev) if w_prev is not None else [0.0] * len(w)
    objective = (
        -portfolio_alpha(w, alpha)
        + 0.5 * gamma * portfolio_variance(w, cov)
        + 0.5 * lambda_to * sum((wi - pi) ** 2 for wi, pi in zip(w, prev))
    )

    lower, upper = constraints.lower, constraints.upper
    box_violation = max(
        [max(lower - wi, 0.0) for wi in w] + [max(wi - upper, 0.0) for wi in w] + [0.0]
    )
    budget_violation = abs(sum(w) - constraints.budget)
    gross_violation = max(gross_exposure(w) - constraints.gross_cap, 0.0)
    max_violation = max(box_violation, budget_violation, gross_violation)

    grid = list(gamma_grid) if gamma_grid is not None else [1.0, 5.0, 25.0, 100.0]
    sensitivity: List[Tuple[float, float]] = []
    for g in grid:
        wg = solve_portfolio(alpha, cov, constraints, gamma=g, w_prev=w_prev, lambda_to=lambda_to)
        sensitivity.append((g, portfolio_variance(wg, cov)))

    return {
        "objective": objective,
        "max_violation": max_violation,
        "gross_exposure": gross_exposure(w),
        "turnover": turnover(w, w_prev),
        "sensitivity": sensitivity,
    }
