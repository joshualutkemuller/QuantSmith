# Macro & Multi-Asset Instructions

## Operating Rules

- Use point-in-time economic data: first-print vintages and correct release lags.
- Never use revised macro values that were unavailable at the decision date.
- Test correlation stability; do not rely on calm-period diversification.
- Make leverage explicit, especially under volatility targeting or risk parity.
- Characterize regime dependence and stress/scenario drawdowns.
- Include turnover and cost across the full asset menu.
- Distinguish strategic (long-run) from tactical (timing) components.

## Checks

- Is economic data point-in-time (first-print, release-lagged)?
- Is correlation stability tested, including in stress?
- Is leverage explicit and its scaling behavior understood?
- Is regime dependence and drawdown behavior characterized?
- Are costs across assets included?
- Are strategic and tactical components separated?

## Output Contract

Use clear Markdown. Include a `Data PIT` section, a `Correlation & Diversification`
section, and a `Leverage & Drawdown` section. Note regime dependence.

## Spec-Driven Role

The allocation logic becomes `REQ-*`; point-in-time data and drawdown/leverage
limits become `AC-*`/`NFR-*`; correlation-breakdown and regime risk become `RISK-*`.
Macro-data vintages are enforced by `instructions/point_in_time.md`. Hands off to
`risk` for leverage/stress sign-off and `backtest_review` for integrity.
