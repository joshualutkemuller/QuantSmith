"""Reference pipeline for spec 0012 — optimal execution scheduling.

This module makes the ``0012-execution-scheduling`` spec *executable*. It is a
deterministic, standard-library-only implementation of the Almgren-Chriss optimal
execution model: given a position to liquidate over a fixed horizon, market-impact
and volatility parameters, and a risk aversion, it computes the trade schedule that
trades expected implementation-shortfall cost against the variance of that cost.

It continues the quant chain — signal (`0001`) → forecast (`0006`) → portfolio
(`0007`) → **execution (`0012`)**: once you know the target position, this decides
how to trade into it.

Guarantees held by construction:

* REQ-002 / AC-002, AC-005 — the schedule fully liquidates: holdings go from the
  full size to zero, monotonically and non-negatively.
* REQ-003 / AC-003 — zero risk aversion gives the uniform (TWAP) schedule; positive
  risk aversion front-loads trading.
* REQ-004 / NFR-003 / AC-004 — higher risk aversion lowers cost variance at the price
  of higher expected cost (the execution trade-off), both reported.
* NFR-001 / AC-006 — the schedule is deterministic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ExecutionSchedule:
    """An optimal execution trajectory.

    ``holdings[k]`` is the position remaining at time ``k`` (``holdings[0]`` is the
    full size, ``holdings[N]`` is zero). ``trades[k]`` is the quantity executed in
    period ``k+1`` (``holdings[k] - holdings[k+1]``).
    """

    holdings: List[float]
    trades: List[float]
    tau: float
    eta: float
    gamma: float
    sigma: float

    @property
    def n_periods(self) -> int:
        return len(self.trades)

    def expected_cost(self) -> float:
        """Expected implementation-shortfall cost of the schedule.

        Permanent impact ``0.5 * gamma * X^2`` plus temporary impact
        ``eta * sum(n_k^2) / tau``.
        """
        total = self.holdings[0]
        permanent = 0.5 * self.gamma * total * total
        temporary = self.eta * sum(n * n for n in self.trades) / self.tau
        return permanent + temporary

    def cost_variance(self) -> float:
        """Variance of the execution cost: ``sigma^2 * tau * sum(x_k^2)`` (k=1..N)."""
        return self.sigma * self.sigma * self.tau * sum(x * x for x in self.holdings[1:])


def optimal_schedule(
    total: float,
    n_periods: int,
    eta: float,
    gamma: float,
    sigma: float,
    risk_aversion: float,
    tau: float = 1.0,
) -> ExecutionSchedule:
    """Almgren-Chriss optimal liquidation schedule.

    Parameters
    ----------
    total: position size to liquidate (X > 0 for a sell program).
    n_periods: number of trading intervals N.
    eta: temporary market-impact coefficient.
    gamma: permanent market-impact coefficient.
    sigma: per-period price volatility.
    risk_aversion: lambda >= 0 — 0 gives TWAP, larger front-loads.
    tau: length of each interval.
    """
    X = float(total)
    N = int(n_periods)
    if N < 1:
        raise ValueError("n_periods must be >= 1")
    if tau <= 0:
        raise ValueError("tau must be positive")
    eta_tilde = eta - 0.5 * gamma * tau
    if eta_tilde <= 0:
        raise ValueError("eta - 0.5*gamma*tau must be positive")

    T = N * tau

    if risk_aversion <= 0:
        # Risk-neutral limit: linear trajectory -> uniform (TWAP) trades.
        holdings = [X * (1.0 - j / N) for j in range(N + 1)]
    else:
        arg = 1.0 + (risk_aversion * sigma * sigma * tau * tau) / (2.0 * eta_tilde)
        kappa = math.acosh(arg) / tau
        sinh_kT = math.sinh(kappa * T)
        holdings = [X * math.sinh(kappa * (T - j * tau)) / sinh_kT for j in range(N + 1)]

    holdings[0] = X
    holdings[N] = 0.0
    trades = [holdings[j - 1] - holdings[j] for j in range(1, N + 1)]
    return ExecutionSchedule(
        holdings=holdings, trades=trades, tau=tau, eta=eta, gamma=gamma, sigma=sigma
    )
