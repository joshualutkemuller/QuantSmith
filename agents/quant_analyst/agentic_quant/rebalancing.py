
"""Rebalancing strategy optimization utilities for the agentic workflow."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

from .framework import Blackboard
from .agents import MarketData, PortfolioPlan


@dataclass(frozen=True)
class RebalancingScenario:
    """Performance statistics for a specific rebalancing frequency."""

    frequency: int
    annualized_return: float
    annualized_volatility: float
    average_turnover: float
    expected_annual_cost: float
    net_annualized_return: float

    def as_dict(self) -> dict[str, float | int]:
        """Serialize the scenario metrics for downstream consumers."""

        return {
            "frequency": int(self.frequency),
            "annualized_return": float(self.annualized_return),
            "annualized_volatility": float(self.annualized_volatility),
            "average_turnover": float(self.average_turnover),
            "expected_annual_cost": float(self.expected_annual_cost),
            "net_annualized_return": float(self.net_annualized_return),
        }


@dataclass(frozen=True)
class RebalancingReport:
    """Summary of the evaluated rebalancing strategies."""

    scenarios: tuple[RebalancingScenario, ...]
    recommended_frequency: int
    transaction_cost: float

    def as_dict(self) -> dict[str, Any]:
        """Return the report in a JSON-serializable structure."""

        return {
            "recommended_frequency": int(self.recommended_frequency),
            "transaction_cost": float(self.transaction_cost),
            "scenarios": [scenario.as_dict() for scenario in self.scenarios],
        }

    def pretty_format(self) -> str:
        """Render a human-readable table of the simulated scenarios."""

        if not self.scenarios:
            return "(no scenarios evaluated)"

        headers = (
            "Freq",
            "Ann Return",
            "Ann Vol",
            "Avg Turnover",
            "Annual Cost",
            "Net Return",
        )
        rows = [headers]
        for scenario in self.scenarios:
            rows.append(
                (
                    f"{scenario.frequency:>5d}",
                    f"{scenario.annualized_return:>10.2%}",
                    f"{scenario.annualized_volatility:>10.2%}",
                    f"{scenario.average_turnover:>12.2%}",
                    f"{scenario.expected_annual_cost:>11.2%}",
                    f"{scenario.net_annualized_return:>10.2%}",
                )
            )

        col_widths = [max(len(row[idx]) for row in rows) for idx in range(len(headers))]
        formatted_rows = []
        for row in rows:
            formatted_rows.append(
                " ".join(cell.rjust(col_widths[idx]) for idx, cell in enumerate(row))
            )
        summary = (
            f"Recommended frequency: every {self.recommended_frequency} trading days\n"
        )
        summary += "Transaction cost assumption: "
        summary += f"{self.transaction_cost:.4%}\n"
        summary += "\n".join(formatted_rows)
        return summary


class RebalancingOptimizationAgent:
    """Simulates multiple rebalancing schedules and selects the best option."""

    def __init__(
        self,
        frequencies: Sequence[int] | None = None,
        *,
        transaction_cost: float = 0.001,
        trading_days_per_year: float = 252.0,
    ) -> None:
        self.name = "rebalancing_agent"
        if transaction_cost < 0:
            raise ValueError("transaction_cost must be non-negative")
        if trading_days_per_year <= 0:
            raise ValueError("trading_days_per_year must be positive")

        if frequencies is None:
            frequencies = (1, 5, 21, 63)

        sanitized = sorted({int(freq) for freq in frequencies if int(freq) > 0})
        if not sanitized:
            raise ValueError("frequencies must contain at least one positive integer")

        self._frequencies = tuple(sanitized)
        self._transaction_cost = float(transaction_cost)
        self._trading_days_per_year = float(trading_days_per_year)

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("market_data", "portfolio_plan")
        market_data: MarketData = blackboard["market_data"]
        plan: PortfolioPlan = blackboard["portfolio_plan"]

        if market_data.returns.size == 0:
            raise ValueError("market data does not contain any return observations")

        scenarios = []
        for frequency in self._frequencies:
            scenario = self._evaluate_frequency(plan, market_data, frequency)
            scenarios.append(scenario)

        best = max(
            scenarios,
            key=lambda sc: (sc.net_annualized_return, -sc.average_turnover),
        )

        report = RebalancingReport(
            scenarios=tuple(scenarios),
            recommended_frequency=best.frequency,
            transaction_cost=self._transaction_cost,
        )
        blackboard["rebalancing_report"] = report
        blackboard["recommended_rebalance_frequency"] = best.frequency

    def _evaluate_frequency(
        self,
        plan: PortfolioPlan,
        market_data: MarketData,
        frequency: int,
    ) -> RebalancingScenario:
        returns = market_data.returns
        if returns.ndim != 2:
            raise ValueError("market data returns must be a 2D array")

        target_weights = np.asarray(plan.weights, dtype=float)
        if target_weights.ndim != 1:
            raise ValueError("portfolio weights must be a 1D array")
        if target_weights.size != returns.shape[1]:
            raise ValueError("portfolio weights must align with return series")

        if not np.isfinite(target_weights).all():
            raise ValueError("portfolio weights must be finite values")

        capital = 1.0
        holdings = target_weights * capital

        turnovers: list[float] = []
        daily_returns: list[float] = []
        rebalance_interval = int(frequency)

        for idx, asset_returns in enumerate(returns):
            prev_capital = capital
            holdings *= (1.0 + asset_returns)
            capital = float(np.sum(holdings))
            if capital <= 0:
                raise ValueError("portfolio value collapsed to zero or below during simulation")
            portfolio_return = capital / prev_capital - 1.0
            daily_returns.append(portfolio_return)

            if (idx + 1) % rebalance_interval == 0:
                target_holdings = target_weights * capital
                turnover = float(
                    np.sum(np.abs(target_holdings - holdings)) / (2.0 * capital)
                )
                turnovers.append(turnover)
                holdings = target_holdings.copy()

        daily_returns_arr = np.asarray(daily_returns, dtype=float)
        if daily_returns_arr.size == 0:
            raise ValueError("insufficient return observations to evaluate rebalancing")

        growth = float((1.0 + daily_returns_arr).prod())
        ann_return = growth ** (
            self._trading_days_per_year / daily_returns_arr.size
        ) - 1.0
        if daily_returns_arr.size > 1:
            ann_vol = float(
                daily_returns_arr.std(ddof=1) * np.sqrt(self._trading_days_per_year)
            )
        else:
            ann_vol = 0.0

        avg_turnover = float(np.mean(turnovers)) if turnovers else 0.0
        events_per_year = self._trading_days_per_year / float(rebalance_interval)
        expected_cost = avg_turnover * self._transaction_cost * events_per_year
        net_return = ann_return - expected_cost

        return RebalancingScenario(
            frequency=rebalance_interval,
            annualized_return=float(ann_return),
            annualized_volatility=ann_vol,
            average_turnover=avg_turnover,
            expected_annual_cost=float(expected_cost),
            net_annualized_return=float(net_return),
        )
