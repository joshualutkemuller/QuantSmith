# Volatility Cost Agent Instructions

## Operating Rules

- Use lagged volatility estimates only; never current or future realized volatility.
- State the volatility estimator, window, annualization, and target.
- Report performance with and without volatility scaling when relevant.
- Calculate turnover from actual position changes after scaling and constraints.
- Stress transaction costs across at least a base and adverse rate.
- Compare high-turnover neural methods against low-turnover allocation baselines fairly.

## Checks

- Are volatility estimates available before the trade?
- Is scaling creating hidden leverage or liquidity needs?
- Does the cost model match traded value and rebalance cadence?
- Does the strategy still beat baselines at adverse cost rates?
- Is turnover concentrated in stressed regimes?

## Output Contract

Use sections: `Volatility Scaling`, `Cost Model`, `Turnover Diagnostics`, `Performance Impact`, `Capacity Review`, and `Acceptance Criteria`.

## Spec-Driven Role

Specs must include the volatility target, estimator, cost rates, turnover calculation, and required stress levels. Acceptance criteria must pass both base-cost and adverse-cost evaluation.
