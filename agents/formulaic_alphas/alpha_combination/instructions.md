# Alpha Combination Instructions

## Operating Rules

- Measure pairwise correlation across the alpha set; low correlation is the value.
- Test spanning: regress a new alpha on the existing book; judge incremental value.
- Prefer robust weighting (equal, shrunk) over optimizer weights that overfit covariance.
- Estimate the covariance point-in-time; do not use full-sample statistics.
- Measure diversification in stress, not only in calm periods.
- Account for the combined signal's turnover and cost, not just the components'.
- Watch for crowding: correlated alphas across the book concentrate risk.

## Checks

- Is the pairwise-correlation structure characterized?
- Is a new alpha's spanning/incremental value tested?
- Are weights robust rather than overfit to a noisy covariance?
- Is the covariance point-in-time?
- Does diversification hold in stress?
- Is the combined book's turnover and cost accounted for?

## Output Contract

Use clear Markdown. Include a `Correlation & Spanning` section, a `Weighting`
section, and a `Diversification` section. Note combined turnover and cost.

## Spec-Driven Role

The combination method becomes `REQ-*`; correlation and incremental-value thresholds
become `AC-*`/`NFR-*`; crowding and weight-overfit become `RISK-*`. Point-in-time
covariance is a `leakage`/`instructions/point_in_time.md` concern; combined-book cost
realism a `backtest` gate concern. See `instructions/formulaic_alphas.md`. Hands off
to `alpha_evaluation`, `backtest_review`, and `risk`.
