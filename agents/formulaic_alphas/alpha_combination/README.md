# Alpha Combination Agent

## Purpose

The Alpha Combination Agent combines many formulaic alphas into a portfolio. The
value of formulaic alphas is a book of many weakly-correlated signals, not any one:
this agent manages pairwise correlation, tests whether a new alpha is spanned by the
existing set, and weights alphas for diversified aggregate performance.

## Use When

- Multiple alphas need combining into a single tradable signal.
- A new alpha's incremental value over the existing book needs assessment (spanning).
- Alpha weights need setting (equal, regression, or optimization).
- The correlation structure of an alpha book needs review.

## Inputs

- The set of alphas and their historical signal/return series.
- The existing combined book, if any.
- Weighting approach and any constraints (turnover, exposure).
- Correlation and capacity considerations.

## Outputs

- A pairwise-correlation assessment of the alpha set.
- A spanning/regression test: does a new alpha add beyond the existing book?
- A weighting scheme (equal, regression, optimized) with rationale.
- The diversification benefit and combined-book characteristics.
- Turnover and cost implications of the combination.

## Example Requests

- "Assess whether this new alpha is spanned by our existing book."
- "Combine these alphas with correlation-aware weights and report diversification."
- "Review the correlation structure and redundancy of this alpha set."

## Required Review Themes

- Pairwise correlation; the book's value comes from low correlation.
- Spanning: incremental value of a new alpha net of the existing set.
- Weighting robustness; optimized weights can overfit the covariance.
- Diversification measured honestly, including in stress.
- Turnover and cost of the combined signal, not just the components.
