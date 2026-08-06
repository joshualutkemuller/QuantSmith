# Alpha Construction Instructions

## Operating Rules

- Use only trailing data in `delay`/`delta`/`ts_*`/`correlation`/`covariance`/
  `decay_linear`/`stddev` windows; never reference the current or future period.
- Apply `rank`/`scale` cross-sectionally across the point-in-time universe.
- Compute `vwap`, `adv`, and returns point-in-time; respect execution timing.
- Neutralize deliberately (industry/sector/market) and state what remains.
- Give every alpha an economic interpretation before trusting a backtest.
- Keep windows and constants parsimonious; do not tune many parameters silently.
- Use point-in-time universe membership and industry classifications.

## Checks

- Does any operator or window use current/future data (look-ahead)?
- Are cross-sectional operators applied over the point-in-time universe?
- Are vwap/adv and execution timing point-in-time?
- Is the neutralization scheme chosen and justified?
- Is there an economic interpretation, not just a fitted stack?
- Are parameters parsimonious and the multiple testing acknowledged?

## Output Contract

Use clear Markdown. Put the formula in a fenced block. Include a `Point-in-Time
Review` section (operator by operator) and a `Neutralization & Interpretation`
section. Note fragility and parameter count.

## Spec-Driven Role

The alpha formula becomes `REQ-*`; no-look-ahead and neutralization become testable
`AC-*`; over-parameterization and crowding become `RISK-*`. Point-in-time operators
are enforced by `instructions/point_in_time.md` and the `leakage` gate; the operator
vocabulary lives in `instructions/formulaic_alphas.md`. Hands off to
`alpha_evaluation`, `backtest_review`, and `risk`.
