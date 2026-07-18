"""Domain-specific agents that collaborate on quantitative workflows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, List, Sequence, TYPE_CHECKING

import numpy as np

from .framework import Blackboard
from mean_variance import MeanVarianceOptimizer, PortfolioPerformance

if TYPE_CHECKING:  # pragma: no cover - import for type checking only
    from .rebalancing import RebalancingReport


@dataclass(frozen=True)
class MarketData:
    """Historical market data generated or retrieved by the data agent."""

    tickers: Sequence[str]
    prices: np.ndarray
    returns: np.ndarray


@dataclass(frozen=True)
class SignalReport:
    """Expected return estimates and diagnostics from the signal agent."""

    tickers: Sequence[str]
    expected_returns: np.ndarray
    annualization_factor: float


@dataclass(frozen=True)
class RiskReport:
    """Covariance matrix and metadata from the risk agent."""

    tickers: Sequence[str]
    covariance: np.ndarray
    lookback: int


@dataclass(frozen=True)
class PortfolioPlan:
    """Portfolio weights and analytics produced by the optimizer agent."""

    tickers: Sequence[str]
    target_return: float
    weights: np.ndarray
    performance: PortfolioPerformance
    gmvp_weights: np.ndarray
    gmvp_performance: PortfolioPerformance


class DataAgent:
    """Generates synthetic price series for a collection of assets."""

    def __init__(
        self,
        tickers: Sequence[str],
        periods: int = 252,
        seed: int | None = 7,
        drift: Iterable[float] | float = 0.08,
        volatility: Iterable[float] | float = 0.2,
    ) -> None:
        if periods < 2:
            raise ValueError("periods must be at least 2")
        self.name = "data_agent"
        self._tickers = list(tickers)
        self._periods = periods
        self._seed = seed
        self._drift = drift
        self._volatility = volatility

    def run(self, blackboard: Blackboard) -> None:
        rng = np.random.default_rng(self._seed)
        n_assets = len(self._tickers)
        drift = np.broadcast_to(np.asarray(self._drift, dtype=float), n_assets)
        vol = np.broadcast_to(np.asarray(self._volatility, dtype=float), n_assets)

        dt = 1.0 / 252.0
        prices = np.empty((self._periods, n_assets), dtype=float)
        prices[0] = 100.0
        for t in range(1, self._periods):
            shocks = rng.normal(loc=0.0, scale=1.0, size=n_assets)
            growth = (drift - 0.5 * vol**2) * dt + vol * np.sqrt(dt) * shocks
            prices[t] = prices[t - 1] * np.exp(growth)
        returns = np.diff(prices, axis=0) / prices[:-1]

        market_data = MarketData(tickers=self._tickers, prices=prices, returns=returns)
        blackboard["market_data"] = market_data


class YahooFinanceDataAgent:
    """Fetches historical prices from Yahoo Finance using :mod:`yfinance`."""

    def __init__(
        self,
        tickers: Sequence[str],
        *,
        period: str | None = "5y",
        start: str | None = None,
        end: str | None = None,
        interval: str = "1d",
        auto_adjust: bool = True,
        min_history: int = 252,
    ) -> None:
        if not tickers:
            raise ValueError("tickers must contain at least one symbol")
        if min_history < 2:
            raise ValueError("min_history must be at least 2")
        self.name = "data_agent"
        self._tickers = list(tickers)
        self._period = period
        self._start = start
        self._end = end
        self._interval = interval
        self._auto_adjust = auto_adjust
        self._min_history = int(min_history)

    def run(self, blackboard: Blackboard) -> None:
        try:
            import pandas as pd  # type: ignore
        except ImportError as exc:  # pragma: no cover - defensive import
            raise RuntimeError(
                "pandas is required to fetch historical data via Yahoo Finance"
            ) from exc

        try:
            import yfinance as yf  # type: ignore
        except ImportError as exc:  # pragma: no cover - defensive import
            raise RuntimeError(
                "yfinance is required to fetch historical data via Yahoo Finance"
            ) from exc

        data = yf.download(
            tickers=" ".join(self._tickers),
            period=self._period,
            start=self._start,
            end=self._end,
            interval=self._interval,
            auto_adjust=self._auto_adjust,
            progress=False,
        )

        if data.empty:
            raise ValueError("No price history returned from Yahoo Finance")

        if isinstance(data.columns, pd.MultiIndex):
            # Prioritize adjusted close; fall back to close if necessary.
            if ("Adj Close" in data.columns.levels[0]) or (
                "Adj Close" in data.columns.get_level_values(0)
            ):
                prices = data["Adj Close"].copy()
            elif ("Close" in data.columns.levels[0]) or (
                "Close" in data.columns.get_level_values(0)
            ):
                prices = data["Close"].copy()
            else:
                raise ValueError("Unable to locate close price columns in Yahoo data")
        else:
            # Single ticker download returns a flat frame with close prices.
            prices = data.copy()
            if "Adj Close" in prices:
                prices = prices[["Adj Close"]]
            elif "Close" in prices:
                prices = prices[["Close"]]

        if isinstance(prices, pd.Series):
            prices = prices.to_frame(name=self._tickers[0])

        prices = prices.dropna(how="any")
        if prices.shape[0] < self._min_history:
            raise ValueError(
                "Not enough observations returned from Yahoo Finance for the requested window"
            )

        # Ensure the columns align with the requested ticker order.
        missing = [ticker for ticker in self._tickers if ticker not in prices.columns]
        if missing:
            raise ValueError(f"Missing data for tickers: {', '.join(missing)}")
        prices = prices.loc[:, self._tickers]

        prices_np = prices.to_numpy(dtype=float)
        returns_np = np.diff(prices_np, axis=0) / prices_np[:-1]

        market_data = MarketData(
            tickers=self._tickers,
            prices=prices_np,
            returns=returns_np,
        )
        blackboard["market_data"] = market_data


class PandasDataReaderDataAgent:
    """Fetches historical prices using :mod:`pandas_datareader`."""

    def __init__(
        self,
        tickers: Sequence[str],
        *,
        data_source: str = "stooq",
        start: str | None = None,
        end: str | None = None,
        min_history: int = 252,
        skip_failed: bool = True,
    ) -> None:
        if not tickers:
            raise ValueError("tickers must contain at least one symbol")
        if min_history < 2:
            raise ValueError("min_history must be at least 2")
        self.name = "data_agent"
        self._tickers = list(tickers)
        self._data_source = data_source
        self._start = start
        self._end = end
        self._min_history = int(min_history)
        self._skip_failed = bool(skip_failed)

    def run(self, blackboard: Blackboard) -> None:
        try:
            import pandas as pd  # type: ignore
        except ImportError as exc:  # pragma: no cover - defensive import
            raise RuntimeError(
                "pandas is required to fetch historical data via pandas_datareader"
            ) from exc

        try:
            from pandas_datareader import data as pdr  # type: ignore
        except ImportError as exc:  # pragma: no cover - defensive import
            raise RuntimeError(
                "pandas_datareader is required to fetch historical market data"
            ) from exc

        start_input = self._start
        end_input = self._end
        today = date.today()
        default_start_date = today - timedelta(days=365 * 5)

        if start_input is None:
            start_date = default_start_date
            start_adjusted = False
        else:
            try:
                start_date = date.fromisoformat(start_input)
            except ValueError as exc:  # pragma: no cover - user input validation
                raise ValueError(
                    f"Invalid start date '{start_input}'. Expected YYYY-MM-DD format."
                ) from exc
            if start_date > today:
                start_date = default_start_date
                start_adjusted = True
            else:
                start_adjusted = False

        if end_input is None:
            end_date = today
            end_adjusted = False
        else:
            try:
                end_date = date.fromisoformat(end_input)
            except ValueError as exc:  # pragma: no cover - user input validation
                raise ValueError(
                    f"Invalid end date '{end_input}'. Expected YYYY-MM-DD format."
                ) from exc
            if end_date > today:
                end_date = today
                end_adjusted = True
            else:
                end_adjusted = False

        if start_date > end_date:
            raise ValueError(
                "Start date must be on or before the end date after adjustments."
            )

        start = start_date.isoformat()
        end = end_date.isoformat()

        frames: list[pd.Series] = []
        failed: list[str] = []
        for ticker in self._tickers:
            try:
                frame = pdr.DataReader(
                    ticker,
                    self._data_source,
                    start=start,
                    end=end,
                )
            except Exception as exc:  # pragma: no cover - network / API errors
                if self._skip_failed:
                    failed.append(ticker)
                    continue
                raise RuntimeError(
                    f"Failed to download data for {ticker} from {self._data_source}"
                ) from exc

            if frame.empty:
                if self._skip_failed:
                    failed.append(ticker)
                    continue
                raise ValueError(
                    f"No price history returned for {ticker} from {self._data_source}"
                )

            frame = frame.sort_index()
            if "Adj Close" in frame:
                series = frame["Adj Close"].copy()
            elif "Close" in frame:
                series = frame["Close"].copy()
            else:
                if self._skip_failed:
                    failed.append(ticker)
                    continue
                raise ValueError(
                    "Unable to locate close price columns in pandas_datareader output"
                )

            series = series.dropna()
            if series.empty:
                if self._skip_failed:
                    failed.append(ticker)
                    continue
                raise ValueError(
                    f"Price history for {ticker} is empty after dropping missing values"
                )

            frames.append(series.rename(ticker))

        if not frames:
            raise RuntimeError(
                "Failed to download market data for all requested tickers. "
                f"Examples of failures: {', '.join(failed[:5])}"
            )

        prices = pd.concat(frames, axis=1, join="inner").dropna(how="any")

        if prices.shape[0] < self._min_history:
            raise ValueError(
                "Not enough observations returned from pandas_datareader for the requested window"
            )

        missing = [ticker for ticker in self._tickers if ticker not in prices.columns]
        if missing:
            if not self._skip_failed:
                raise ValueError(f"Missing data for tickers: {', '.join(missing)}")
            failed.extend(missing)

        available = [ticker for ticker in self._tickers if ticker not in failed]
        if not available:
            raise RuntimeError(
                "Unable to assemble any price history from pandas_datareader "
                "after dropping failures"
            )

        prices = prices.loc[:, available]

        prices_np = prices.to_numpy(dtype=float)
        returns_np = np.diff(prices_np, axis=0) / prices_np[:-1]

        market_data = MarketData(
            tickers=tuple(available),
            prices=prices_np,
            returns=returns_np,
        )
        blackboard["market_data"] = market_data

        if failed or start_adjusted or end_adjusted:
            existing = blackboard.get("data_warnings", {})
            warnings = dict(existing)
            if failed:
                warnings["missing_tickers"] = sorted(set(failed))
            if start_adjusted or end_adjusted:
                warnings["date_adjustments"] = {
                    "start": start_input,
                    "end": end_input,
                    "resolved_start": start,
                    "resolved_end": end,
                }
            blackboard["data_warnings"] = warnings


class FactorSignalAgent:
    """Computes expected returns using a simple momentum factor model."""

    def __init__(self, lookback: int = 63, annualization_factor: float = 252.0) -> None:
        if lookback < 2:
            raise ValueError("lookback must be at least 2")
        self.name = "signal_agent"
        self._lookback = lookback
        self._annualization_factor = float(annualization_factor)

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("market_data")
        market_data: MarketData = blackboard["market_data"]
        if market_data.returns.shape[0] < self._lookback:
            raise ValueError("Not enough return observations for the requested lookback window")

        window = market_data.returns[-self._lookback :]
        # Use a normalized momentum score as expected return proxy.
        mean_returns = window.mean(axis=0)
        volatility = window.std(axis=0, ddof=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            sharpes = np.divide(mean_returns, volatility, where=volatility > 0)
        sharpes = np.nan_to_num(sharpes)
        expected_returns = mean_returns + 0.5 * sharpes * volatility
        expected_returns = expected_returns * self._annualization_factor

        report = SignalReport(
            tickers=market_data.tickers,
            expected_returns=expected_returns,
            annualization_factor=self._annualization_factor,
        )
        blackboard["signal_report"] = report


class RiskAgent:
    """Estimates covariance matrices from historical returns."""

    def __init__(self, lookback: int = 252) -> None:
        if lookback < 2:
            raise ValueError("lookback must be at least 2")
        self.name = "risk_agent"
        self._lookback = lookback

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("market_data")
        market_data: MarketData = blackboard["market_data"]
        if market_data.returns.shape[0] < self._lookback:
            raise ValueError("Not enough return observations for the requested lookback window")

        window = market_data.returns[-self._lookback :]
        covariance = np.cov(window, rowvar=False, ddof=1)

        report = RiskReport(
            tickers=market_data.tickers,
            covariance=covariance,
            lookback=self._lookback,
        )
        blackboard["risk_report"] = report


class PortfolioConstructionAgent:
    """Builds an efficient portfolio using the Markowitz optimizer."""

    def __init__(self, target_return: float | None = None) -> None:
        self.name = "portfolio_agent"
        self._target_return = target_return

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("signal_report", "risk_report")
        signals: SignalReport = blackboard["signal_report"]
        risk: RiskReport = blackboard["risk_report"]

        optimizer = MeanVarianceOptimizer(signals.expected_returns, risk.covariance)
        gmvp_weights = optimizer.global_minimum_variance_weights()
        gmvp_perf = optimizer.portfolio_performance(gmvp_weights)

        if self._target_return is None:
            target_return = float(np.mean(signals.expected_returns))
        else:
            target_return = float(self._target_return)

        weights = optimizer.efficient_weights(target_return)
        performance = optimizer.portfolio_performance(weights)

        plan = PortfolioPlan(
            tickers=signals.tickers,
            target_return=target_return,
            weights=weights,
            performance=performance,
            gmvp_weights=gmvp_weights,
            gmvp_performance=gmvp_perf,
        )
        blackboard["portfolio_plan"] = plan


class RiskOverlayAgent:
    """Applies simple exposure limits to the constructed portfolio."""

    def __init__(self, max_leverage: float = 1.5, max_single_weight: float = 0.5) -> None:
        if max_leverage <= 0:
            raise ValueError("max_leverage must be positive")
        if not (0 < max_single_weight <= 1.0):
            raise ValueError("max_single_weight must be in (0, 1]")
        self.name = "risk_overlay_agent"
        self._max_leverage = float(max_leverage)
        self._max_single_weight = float(max_single_weight)

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("portfolio_plan", "signal_report", "risk_report")
        plan: PortfolioPlan = blackboard["portfolio_plan"]
        signals: SignalReport = blackboard["signal_report"]
        risk: RiskReport = blackboard["risk_report"]
        weights = plan.weights.copy()
        gross = float(np.sum(np.abs(weights)))
        if gross > self._max_leverage:
            weights *= self._max_leverage / gross

        max_abs_weight = np.max(np.abs(weights))
        if max_abs_weight > self._max_single_weight:
            scale = self._max_single_weight / max_abs_weight
            weights *= scale

        # Renormalize to keep the portfolio fully invested.
        total = float(np.sum(weights))
        if not np.isclose(total, 0.0):
            weights /= total

        optimizer = MeanVarianceOptimizer(signals.expected_returns, risk.covariance)
        performance = optimizer.portfolio_performance(weights)
        optimized_plan = PortfolioPlan(
            tickers=plan.tickers,
            target_return=plan.target_return,
            weights=weights,
            performance=performance,
            gmvp_weights=plan.gmvp_weights,
            gmvp_performance=plan.gmvp_performance,
        )
        blackboard["portfolio_plan"] = optimized_plan
        blackboard["risk_overlay"] = {
            "gross_leverage": float(np.sum(np.abs(weights))),
            "max_single_weight": float(np.max(np.abs(weights))),
        }


class ReportAgent:
    """Synthesizes a human-readable report of the pipeline outputs."""

    def __init__(self) -> None:
        self.name = "report_agent"

    def run(self, blackboard: Blackboard) -> None:
        blackboard.require("portfolio_plan", "risk_overlay")
        plan: PortfolioPlan = blackboard["portfolio_plan"]
        overlay = blackboard["risk_overlay"]

        lines: List[str] = []
        lines.append("Agentic Quantitative Portfolio Construction Report")
        lines.append("=" * 55)
        lines.append(f"Target annualized return: {plan.target_return:.2%}")
        lines.append(
            "Achieved by "
            f"{plan.performance.expected_return:.2%} expected return "
            f"with {plan.performance.volatility:.2%} volatility"
        )
        lines.append("\nWeights after risk overlay:")
        for ticker, weight in zip(plan.tickers, plan.weights):
            lines.append(f"  {ticker}: {weight:.2%}")
        lines.append(
            "\nGlobal minimum variance portfolio (reference): "
            f"{plan.gmvp_performance.expected_return:.2%} expected return, "
            f"{plan.gmvp_performance.volatility:.2%} volatility"
        )
        lines.append(
            "Risk overlay diagnostics: "
            f"gross leverage={overlay['gross_leverage']:.2f}, "
            f"max single weight={overlay['max_single_weight']:.2%}"
        )

        rebalancing_report: "RebalancingReport | None" = blackboard.get(
            "rebalancing_report"
        )
        if rebalancing_report:
            lines.append("\nRebalancing strategy analysis:")
            for scenario in rebalancing_report.scenarios:
                lines.append(
                    "  Every "
                    f"{scenario.frequency} trading days: "
                    f"net return {scenario.net_annualized_return:.2%}, "
                    f"gross return {scenario.annualized_return:.2%}, "
                    f"turnover {scenario.average_turnover:.2%}, "
                    f"annual cost {scenario.expected_annual_cost:.2%}"
                )
            lines.append(
                "Recommended cadence: rebalance every "
                f"{rebalancing_report.recommended_frequency} trading days"
            )
            if rebalancing_report.transaction_cost > 0:
                lines.append(
                    "(transaction cost assumption: "
                    f"{rebalancing_report.transaction_cost:.2%} per unit turnover)"
                )

        blackboard["report"] = "\n".join(lines)
