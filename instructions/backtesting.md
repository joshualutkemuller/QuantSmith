# Backtesting Instructions

## Purpose

Use this instruction set to review historical strategy simulations, signal tests, portfolio experiments, and model evaluations that influence trading or allocation decisions.

## Required Inputs

- Strategy or model description.
- Universe construction rules.
- Data sources and point-in-time assumptions.
- Signal formation time.
- Rebalance and execution schedule.
- Portfolio construction rules and constraints.
- Cost, slippage, borrow, financing, and market impact assumptions.
- Metrics, benchmarks, and evaluation windows.

## Expected Output

- Simulation contract.
- Findings ordered by severity.
- Bias and leakage review.
- Execution and cost review.
- Robustness test plan.
- Risk review.
- Production-readiness recommendation.

## Standards

- Reconstruct the simulation contract before judging results.
- Separate signal time, decision time, execution time, and outcome measurement time.
- Use point-in-time universe membership and data values.
- Include realistic costs and constraints for the expected turnover and capacity.
- Compare against a relevant benchmark and a simple baseline.
- Report turnover, drawdown, exposure, concentration, capacity, and regime behavior alongside returns.
- Test robustness across windows, costs, universe definitions, parameters, and market regimes.
- Treat exceptional performance as a reason for deeper review, not immediate confidence.

## Checks

- Could any feature, filter, label, or universe rule use information unavailable at decision time?
- Does the strategy survive higher costs, delayed execution, and lower liquidity assumptions?
- Are parameter choices justified before final validation?
- Are benchmark, cash, financing, and corporate action assumptions documented?
- Are risk exposures and concentration acceptable?
- Are results stable across meaningful subperiods?
- Is implementation detail sufficient for paper trading or reproduction?

## Common Failure Modes

- Lookahead through labels, joins, adjusted values, or rebalance timing.
- Survivorship bias through current index membership or current security masters.
- Underestimated costs for high-turnover strategies.
- Overfitting through repeated parameter search.
- Weak benchmark selection.
- Hidden exposure to market, sector, style, liquidity, or volatility factors.

## Spec-Driven Alignment

This standard backs the Verify step. Backtest findings become validation evidence
mapped to the spec's `AC-*`; fragilities, exposures, and cost sensitivities become
`RISK-*`; production blockers hold the deployment gate. It is enforced by the
`backtest-check` gate (transaction costs, out-of-sample, benchmark,
turnover/capacity, multiple-testing) and applies `instructions/point_in_time.md`.
No performance `AC-*` is met without leakage-free, cost-aware, robust evidence
(constitution P3, P4).
