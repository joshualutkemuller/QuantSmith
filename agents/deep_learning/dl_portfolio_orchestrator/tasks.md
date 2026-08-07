# DL Portfolio Orchestrator Tasks

## Standard Tasks

1. Define the portfolio decision, universe, cadence, and risk target.
2. Select the agent route and review order.
3. Require a baseline ladder before neural modeling.
4. Capture data, feature, and point-in-time requirements.
5. Decompose the model into architecture, objective, constraints, cost/risk, and explainability workstreams.
6. Define acceptance criteria and stop conditions.
7. Produce an implementation handoff for `specs/` or `src/quantsmith/`.

## Evidence to Collect

- Baseline performance table.
- Out-of-sample split description.
- Transaction-cost and turnover assumptions.
- Volatility-scaling or risk-targeting assumptions.
- Crisis/regime behavior review.
- Feature sensitivity or attribution artifacts.

## Red Flags

- Neural model proposed before the baseline.
- Sharpe improvement without turnover and cost drag.
- Random train/test split on financial time series.
- Portfolio weights that violate business or exposure constraints.
- Strong backtest with no explanation for crash periods.
