# Alpha Evaluation Instructions

## Operating Rules

- Characterize holding period and turnover before judging performance.
- Report performance net of realistic transaction costs at the alpha's turnover.
- Test dependence on volatility and known factors; strip out risk-premium mimicry.
- Measure correlation to common/known alphas; require incremental value.
- Estimate capacity from liquidity (adv) and the size at which the edge decays.
- Assess decay and crowding out-of-sample and over time, not just in-sample.
- Use point-in-time data for every statistic; no full-sample normalization.

## Checks

- Are holding period and turnover characterized?
- Does the edge survive realistic costs at that turnover?
- Is the return independent of volatility and known factors?
- Is the alpha incremental to known alphas, not redundant?
- Is capacity estimated from liquidity, and is decay assessed out-of-sample?
- Are all statistics point-in-time?

## Output Contract

Use clear Markdown. Include a `Holding Period & Turnover` section, a `Net-of-Cost
Performance` section, and a `Dependence & Correlation` section. State capacity and
decay.

## Spec-Driven Role

Evaluation thresholds are acceptance criteria: net-of-cost performance, turnover, and
capacity become `AC-*`/`NFR-*`; volatility/factor dependence and decay/crowding become
`RISK-*`. Cost realism and out-of-sample are enforced by the `backtest` gate; PIT
statistics by `instructions/point_in_time.md`. See `instructions/formulaic_alphas.md`.
Hands off to `backtest_review` and `risk`.
