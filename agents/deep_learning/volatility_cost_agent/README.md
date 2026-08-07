# Volatility Cost Agent

## Purpose

Reviews volatility scaling, risk targeting, transaction costs, turnover, and capacity for deep-learning portfolio strategies.

## Use When

- A portfolio model uses volatility targeting or ex-ante volatility estimates.
- Strategy performance must be compared at a common risk level.
- Transaction costs, turnover, slippage, or capacity can change conclusions.
- A daily reallocation model is being compared with low-turnover allocation rules.

## Inputs

- Portfolio weights, asset returns, and rebalance cadence.
- Volatility target and volatility estimator.
- Cost rate, spread/slippage assumptions, and traded-value calculation.
- Baseline strategy weights and turnover.

## Outputs

- Volatility-scaling design and lag review.
- Transaction-cost model and turnover diagnostics.
- Performance table before and after costs.
- Capacity and robustness concerns.

## Required Review Themes

- Risk targeting can make returns more comparable, but it is not free leverage.
- Daily neural allocations can look strong before turnover drag.
- Cost assumptions must be stress-tested across rates and regimes.
