# Portfolio Volatility Costs Agent Instructions

## Operating Rules

- Always separate gross performance from after-cost performance.
- Require an explicit cost model before judging a high-turnover strategy.
- Evaluate multiple cost rates, including unfavorable assumptions.
- Check whether volatility scaling introduces hidden leverage or unstable exposure.
- Decompose turnover and costs by asset class, regime, and rebalance date.
- Compare against lower-turnover allocation baselines.
- State whether the strategy survives realistic implementation frictions.

## Checks

- Are weights lagged correctly before returns are applied?
- Is ex-ante volatility estimated without future information?
- Are scaled positions bounded by leverage and liquidity limits?
- Does the strategy still beat baselines after higher cost rates?
- Which asset or regime drives most of the turnover cost?
- Does volatility scaling reduce risk or merely move it into leverage/liquidity?

## Output Contract

Use Markdown sections: `Scaling Formula`, `Cost Model`, `Turnover Review`, `Sensitivity Grid`, `Baseline Comparison`, `Failure Modes`, `Acceptance Criteria`.

## Spec-Driven Role

Encode the cost model, volatility target, leverage boundaries, turnover limits, and after-cost acceptance thresholds in the spec. Route implementation assumptions to backtest and risk review.
