# Formulaic Alphas Instructions

## Purpose

Use this instruction set when constructing, combining, or evaluating formulaic
alphas — tradable signals expressed as explicit formulas over market inputs, in the
methodology of *101 Formulaic Alphas* (Kakushadze, 2016). It is the shared standard
behind the `agents/formulaic_alphas/` group and defines the operator vocabulary.

## Operator Library

**Inputs:** `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`,
`adv{d}` (average daily dollar volume over `d` days), `cap` (market cap).

**Cross-sectional operators** (act across the universe on a given day):

- `rank(x)` — cross-sectional rank, normalized to [0, 1].
- `scale(x, a=1)` — rescale so the sum of absolute values equals `a`.
- `indneutralize(x, g)` — demean `x` within each group `g` (industry/sector).
- `signedpower(x, a)` — `sign(x) * abs(x)^a`.

**Time-series operators** (act over a trailing window of `d` days — past data only):

- `delay(x, d)`, `delta(x, d) = x - delay(x, d)`.
- `ts_rank(x, d)`, `ts_min(x, d)`, `ts_max(x, d)`, `ts_argmin(x, d)`, `ts_argmax(x, d)`.
- `sum(x, d)`, `product(x, d)`, `stddev(x, d)`.
- `decay_linear(x, d)` — linearly-weighted moving average over `d` days.
- `correlation(x, y, d)`, `covariance(x, y, d)`.

**Conditionals:** `(condition ? a : b)`.

## Standards

- **Point-in-time by construction.** Every time-series operator and window uses only
  trailing data; `vwap`, `adv`, and returns are point-in-time. No operator references
  the current-decision or future period. See `instructions/point_in_time.md`.
- **Cross-sectional and neutralized.** Alphas are ranked across the point-in-time
  universe and neutralized (industry/sector/market) to isolate the intended edge.
- **Economic interpretation.** Every alpha has a reason it should work
  (mean-reversion, momentum, price-volume interaction), not just a fitted stack.
- **Parsimony and multiple testing.** Operators can generate endless formulas;
  keep parameters few and control for the multiple testing implied by the search.
- **Low correlation is the value.** A book of many weakly-correlated alphas beats any
  single one; manage pairwise correlation and test spanning.
- **Costs and capacity.** Short holding periods make turnover and transaction costs
  (cents-per-share) decisive; capacity follows liquidity (`adv`).

## Checks

- Does any operator/window use current or future data (look-ahead)?
- Are cross-sectional operators applied over the point-in-time universe?
- Is neutralization chosen and justified, with residual exposure stated?
- Does the alpha have an economic interpretation?
- Are parameters parsimonious and multiple testing controlled?
- Is correlation to the existing book and to known factors assessed?
- Does a net-of-cost edge survive at the alpha's turnover and capacity?

## Common Failure Modes

- Look-ahead via a mis-specified `ts_`/`correlation` window or same-day inputs.
- Full-sample normalization instead of point-in-time cross-sectional operations.
- Over-parameterized formulas mined from an operator search with no economic story.
- Adding an alpha that is spanned by (redundant with) the existing book.
- Reporting gross returns for a high-turnover alpha that costs erase.
- Mistaking a volatility or known-factor exposure for a genuine alpha.

## Spec-Driven Alignment

This standard backs the `agents/formulaic_alphas/` group across Research and Testing.
The alpha formula and combination method become `REQ-*`; no-look-ahead, neutralization,
net-of-cost, and correlation/spanning thresholds become `AC-*`/`NFR-*`; over-fitting,
crowding, and factor-mimicry become `RISK-*`. Point-in-time construction is enforced
by `instructions/point_in_time.md` and the `leakage` gate; cost, out-of-sample, and
multiple-testing by the `backtest` gate (constitution P3, P4).
