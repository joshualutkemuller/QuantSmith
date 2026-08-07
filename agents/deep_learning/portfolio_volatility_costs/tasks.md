# Portfolio Volatility Costs Agent Tasks

## Intake

- Collect raw weights, scaled weights, returns, and rebalance cadence.
- Record volatility target, estimator, lookback, and leverage policy.
- Record cost assumptions and asset-specific liquidity constraints.

## Analysis

- Compute gross and net returns separately.
- Compute turnover before and after volatility scaling.
- Run sensitivity to cost rates and volatility targets.
- Compare against low-turnover fixed allocation baselines.
- Identify regimes where scaling or costs dominate returns.

## Validation

- Verify lagging, point-in-time volatility, and no look-ahead in scaled positions.
- Report after-cost Sharpe, Sortino, max drawdown, turnover, and exposure.
- Flag instability when performance depends on narrow cost assumptions.

## Handoff

- Send cost assumptions to `backtest_review`, `risk`, and securities-financing agents.
- Add acceptance criteria before implementation proceeds.
