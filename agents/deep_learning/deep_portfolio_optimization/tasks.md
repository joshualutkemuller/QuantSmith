# Deep Portfolio Optimization Agent Tasks

## Intake

- Identify the allocation decision, rebalance cadence, and tradable universe.
- Define the available point-in-time feature set and lookback window.
- Record objective, constraints, cost model, and risk target.

## Design

- Specify the direct portfolio objective.
- Choose the neural family only after documenting baselines.
- Define output activation or projection for feasible weights.
- Add ablations for features, lookback, architecture, and objective variants.

## Validation

- Build time-ordered train/validation/test windows.
- Compare against fixed allocation, mean-variance, maximum diversification, and naive no-trade baselines where applicable.
- Report Sharpe, Sortino, expected return, volatility, downside deviation, max drawdown, hit rate, turnover, and after-cost returns.

## Handoff

- Produce acceptance criteria for implementation.
- Escalate broad builds to a numbered spec.
- Send model-risk concerns to `model_selection_validation`, `backtest_review`, and `risk`.
