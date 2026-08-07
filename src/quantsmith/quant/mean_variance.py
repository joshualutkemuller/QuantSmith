"""Sample mean-variance optimization utilities.

This module implements a minimal mean-variance optimizer using the closed-form
solution for the efficient frontier.  It assumes that investors may take long or
short positions (i.e. there are no inequality constraints beyond the full
investment constraint).

The implementation follows the classic Markowitz framework:

* Weights sum to one.
* Expected returns and the covariance matrix are provided exogenously.
* Efficient frontier portfolios minimize variance for a target expected return.

The module is intentionally lightweight and depends only on NumPy so it can run
in environments where optimization libraries such as CVXOPT or CVXPY are not
available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

import numpy as np


@dataclass(frozen=True)
class PortfolioPerformance:
    """Stores the expected return and volatility of a portfolio."""

    expected_return: float
    volatility: float


class MeanVarianceOptimizer:
    """Closed-form mean-variance optimizer.

    Parameters
    ----------
    expected_returns:
        1-D iterable of expected asset returns.
    covariance:
        2-D iterable representing the covariance matrix of the asset returns.

    Notes
    -----
    The optimizer uses the analytical solution to the constrained quadratic
    program with a full-investment constraint.  Short sales are allowed, so the
    resulting weights may be negative.  If no target return is provided, the
    global minimum variance portfolio is computed.
    """

    def __init__(self, expected_returns: Iterable[float], covariance: Iterable[Iterable[float]]):
        self.expected_returns = np.asarray(expected_returns, dtype=float)
        self.covariance = np.asarray(covariance, dtype=float)

        if self.expected_returns.ndim != 1:
            raise ValueError("expected_returns must be one-dimensional")
        if self.covariance.ndim != 2:
            raise ValueError("covariance must be two-dimensional")
        n = self.expected_returns.shape[0]
        if self.covariance.shape != (n, n):
            raise ValueError("covariance shape must match (n_assets, n_assets)")

        # Pre-compute the inverse covariance matrix and auxiliary scalars used by
        # the efficient frontier calculations.
        self._inv_covariance = np.linalg.inv(self.covariance)
        ones = np.ones(n)
        mu = self.expected_returns
        inv_cov = self._inv_covariance

        self._A = float(ones @ inv_cov @ ones)
        self._B = float(ones @ inv_cov @ mu)
        self._C = float(mu @ inv_cov @ mu)
        self._delta = self._A * self._C - self._B**2
        if np.isclose(self._delta, 0.0):
            raise ValueError("Covariance matrix leads to a singular frontier (delta ≈ 0)")

        self._inv_cov_times_one = inv_cov @ ones
        self._inv_cov_times_mu = inv_cov @ mu

    @property
    def n_assets(self) -> int:
        """Number of assets in the optimization problem."""

        return self.expected_returns.size

    def global_minimum_variance_weights(self) -> np.ndarray:
        """Return the weights of the global minimum variance portfolio."""

        weights = self._inv_cov_times_one / self._A
        return weights

    def efficient_weights(self, target_return: float) -> np.ndarray:
        """Return weights that minimize variance for a target return.

        Parameters
        ----------
        target_return:
            Desired expected return of the portfolio.  The returned weights will
            achieve this return while minimizing variance (subject to the
            long-short constraint set described earlier).
        """

        term1 = (self._C - self._B * target_return) / self._delta
        term2 = (self._A * target_return - self._B) / self._delta
        weights = term1 * self._inv_cov_times_one + term2 * self._inv_cov_times_mu
        return weights

    def portfolio_performance(self, weights: Iterable[float]) -> PortfolioPerformance:
        """Compute expected return and volatility for the provided weights."""

        w = np.asarray(weights, dtype=float)
        if w.ndim != 1 or w.size != self.n_assets:
            raise ValueError("weights must be a one-dimensional array with length n_assets")

        expected_return = float(w @ self.expected_returns)
        variance = float(w @ self.covariance @ w)
        return PortfolioPerformance(expected_return=expected_return, volatility=np.sqrt(variance))

    def efficient_frontier(self, num_points: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """Sample points from the efficient frontier.

        Parameters
        ----------
        num_points:
            Number of frontier points to compute.  The frontier is sampled using
            evenly spaced target returns between the minimum and maximum asset
            returns.
        """

        if num_points < 2:
            raise ValueError("num_points must be at least 2 to compute a frontier")

        target_returns = np.linspace(self.expected_returns.min(), self.expected_returns.max(), num_points)
        volatilities = []
        for r in target_returns:
            w = self.efficient_weights(r)
            perf = self.portfolio_performance(w)
            volatilities.append(perf.volatility)
        return target_returns, np.asarray(volatilities)


def _example() -> None:
    """Run a small example using three synthetic assets."""

    expected_returns = np.array([0.08, 0.12, 0.15])
    covariance = np.array(
        [
            [0.10, 0.02, 0.04],
            [0.02, 0.08, 0.06],
            [0.04, 0.06, 0.15],
        ]
    )

    optimizer = MeanVarianceOptimizer(expected_returns, covariance)
    gmvp_weights = optimizer.global_minimum_variance_weights()
    gmvp_perf = optimizer.portfolio_performance(gmvp_weights)

    print("Global minimum variance portfolio")
    print("Weights:", np.round(gmvp_weights, 4))
    print("Expected return: {:.2%}".format(gmvp_perf.expected_return))
    print("Volatility: {:.2%}".format(gmvp_perf.volatility))

    target_return = 0.11
    efficient_w = optimizer.efficient_weights(target_return)
    efficient_perf = optimizer.portfolio_performance(efficient_w)

    print("\nEfficient portfolio for {:.0%} target return".format(target_return))
    print("Weights:", np.round(efficient_w, 4))
    print("Expected return: {:.2%}".format(efficient_perf.expected_return))
    print("Volatility: {:.2%}".format(efficient_perf.volatility))

    frontier_returns, frontier_vols = optimizer.efficient_frontier(num_points=5)
    print("\nEfficient frontier samples:")
    for r, v in zip(frontier_returns, frontier_vols):
        print("Return: {:.2%}, Volatility: {:.2%}".format(r, v))


if __name__ == "__main__":
    _example()
