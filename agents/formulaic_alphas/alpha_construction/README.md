# Alpha Construction Agent

## Purpose

The Alpha Construction Agent builds and reviews formulaic alphas from the operator
library. It composes cross-sectional and time-series operators over market inputs
into an explicit, point-in-time signal, and reviews candidate formulas for
look-ahead, neutralization, and economic sense.

## Use When

- A formulaic alpha needs designing from the operator language.
- A candidate formula needs a look-ahead and neutralization review.
- An idea (mean-reversion, momentum, volume/price interaction) needs expressing as a formula.
- An existing alpha's construction needs auditing operator by operator.

## Inputs

- The idea or edge to express, and the universe and asset class.
- Available inputs (`open/high/low/close/volume/vwap/returns/adv/cap`), point-in-time.
- Intended holding period and neutralization scheme.
- Any existing formula to review.

## Outputs

- A formulaic alpha expression using the operator library.
- A per-operator point-in-time / look-ahead review.
- The neutralization scheme (industry/sector/market) and rationale.
- The economic interpretation (why this should be an edge).
- Notes on where the formula is fragile or over-parameterized.

## Example Requests

- "Express this volume-price reversal idea as a formulaic alpha."
- "Review this formula for look-ahead in its ts_ and correlation windows."
- "Add industry neutralization to this alpha and explain the effect."

## Required Review Themes

- Point-in-time operators: `delay`/`delta`/`ts_*`/`correlation`/`decay_linear`
  windows use only trailing data.
- Cross-sectional `rank`/`scale` applied across the point-in-time universe.
- Neutralization (industry/sector/market) chosen and justified.
- An economic interpretation, not just a fitted operator stack.
- Parameter parsimony: windows and constants that are not silently overfit.
