# Mean Reversion & Statistical Arbitrage Instructions

## Operating Rules

- Test the relationship's stationarity and half-life out-of-sample, not just in-sample.
- Derive entry/exit thresholds from the spread dynamics, not from fitting returns.
- Include transaction costs and borrow; assume they may exceed the raw edge.
- Model realistic execution: both legs, slippage, and the cost of frequent turnover.
- Watch for regime breaks that permanently sever a relationship.
- Control for multiple testing across all pairs/relationships screened.
- Use point-in-time universe membership; avoid survivorship in the pair set.

## Checks

- Is the relationship stationary and stable out-of-sample?
- Are thresholds justified by half-life/dynamics rather than fitted?
- Do costs and borrow leave a real edge after both legs trade?
- Is turnover sustainable at the intended capacity?
- Could a regime break invalidate the relationship?
- Is the multiple testing from pair screening accounted for?

## Output Contract

Use clear Markdown. Include a `Relationship & Half-Life` section, a `Thresholds`
section, and a `Cost & Capacity` section. Note the multiple-testing control used.

## Spec-Driven Role

The spread definition and thresholds become `REQ-*`; stationarity, out-of-sample,
and net-of-cost thresholds become `AC-*`/`NFR-*`; regime-break and decay risk become
`RISK-*`. Multiple-testing discipline is checked by the `backtest` gate; leakage/PIT
by `instructions/point_in_time.md`. See
`instructions/trading_strategies.md` for the shared standard. Hands off to
`backtest_review` and `risk`.
