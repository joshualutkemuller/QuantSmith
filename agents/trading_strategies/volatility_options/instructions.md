# Volatility & Options Instructions

## Operating Rules

- State the specific volatility edge (variance risk premium, skew, term structure).
- Make greeks explicit; account for delta-hedging frequency and slippage.
- Treat short-volatility positions as tail-risk-bearing; size to the tail.
- Decompose returns into implied-vs-realized and the premium actually captured.
- Treat pricing and vol-surface assumptions as model risk, and test sensitivity.
- Use point-in-time implied/realized data; option chains as-of the decision time.
- Account for margin and financing behavior under a volatility spike.

## Checks

- Is the volatility edge specific and economically grounded?
- Are greeks, hedging frequency, and slippage modeled?
- Is short-vol tail risk characterized and sized for?
- Is the implied-vs-realized premium decomposed?
- Is model risk in pricing/surface assessed?
- Does margin/financing survive a volatility spike?

## Output Contract

Use clear Markdown. Include a `Volatility Edge` section, a `Greeks & Hedging`
section, and a `Tail & Model Risk` section. Note margin behavior under stress.

## Spec-Driven Role

The strategy and hedging rules become `REQ-*`; the captured premium and hedging-cost
thresholds become `AC-*`/`NFR-*`; short-vol tail and model risk become `RISK-*`.
PIT option/vol data is enforced by `instructions/point_in_time.md`. See
`instructions/trading_strategies.md` for the shared standard. Hands off to
`risk` for tail/greeks sign-off and `backtest_review` for execution realism.
