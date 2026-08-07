# Formulaic Alpha Agents

This folder operationalizes the formulaic-alpha methodology of *101 Formulaic
Alphas* (Kakushadze, 2016): building tradable alphas as explicit formulas from a
library of operators, combining many weakly-correlated alphas, and evaluating them.

This is a distinct capability from the other agent groups. Unlike
`feature_engineering/` (features that feed a model) or `modeling/` (ML models), a
formulaic alpha *is* the tradable signal, expressed directly as a formula. Unlike
`trading_strategies/` (strategy archetypes), these agents work in the operator
language that constructs signals.

## Agents

| Agent | Handles |
| --- | --- |
| `alpha_construction/` | Building and reviewing formulaic alphas from the operator library — cross-sectional and time-series operators, inputs, neutralization, point-in-time correctness. |
| `alpha_combination/` | Combining many alphas into a portfolio — pairwise correlation, spanning/regression, weighting, and diversification. |
| `alpha_evaluation/` | Evaluating an alpha — holding period, turnover, volatility dependence, correlation, capacity, and decay/crowding. |

## Group Workflow

```
alpha_construction → alpha_combination → alpha_evaluation
```

Construct point-in-time candidate formulas, combine weakly correlated survivors into
a diversified alpha book, then evaluate turnover, capacity, decay, crowding, and
net performance. Failed evaluation feeds a new construction or combination cycle.

## The Operator Language

Formulaic alphas compose a small set of operators over market inputs (see
`instructions/formulaic_alphas.md` for the full reference):

- **Cross-sectional:** `rank`, `scale`, `indneutralize`, `signedpower`.
- **Time-series:** `delay`, `delta`, `ts_rank`, `ts_min`/`ts_max`,
  `ts_argmin`/`ts_argmax`, `sum`, `product`, `stddev`, `decay_linear`,
  `correlation`, `covariance`.
- **Inputs:** `open`, `high`, `low`, `close`, `volume`, `vwap`, `returns`,
  `adv{d}` (average daily dollar volume), `cap`.

## Shared Principles

- **Point-in-time by construction.** Time-series operators and windows use only
  trailing data; `vwap`, `adv`, and neutralization groups are point-in-time. A
  formulaic alpha that peeks ahead is a defect. See `instructions/point_in_time.md`.
- **Cross-sectional and neutralized.** Alphas are ranked across the universe and
  neutralized (industry/sector/market) to isolate the intended edge.
- **Low correlation is the goal.** The value is a book of many weakly-correlated
  alphas, not one; correlation and spanning are first-class concerns.
- **Costs and capacity decide survival.** Short holding periods mean turnover and
  transaction costs (cents-per-share) dominate; capacity follows liquidity.
- **Overfitting discipline.** With operators that can generate endless formulas,
  multiple-testing control and out-of-sample validation are essential.

## Where They Fit

Formulaic alpha agents feed Research and Testing, and lean on `feature_engineering`
(point-in-time inputs), `backtest_review` (integrity), and `risk` (exposures). A
candidate alpha becomes a spec and is proven through the `leakage` and `backtest`
gates.

## Note On Scope

This applies the paper's methodology and operator language; it does not reproduce
the 101 formulas. Specific alpha expressions belong in a strategy's own spec.
