# Trading Strategy Agents

This folder operationalizes the strategy families catalogued in *151 Trading
Strategies* (Kakushadze & Serur) as a set of archetype agents. The book organizes
strategies by asset class; the same archetypes recur across those classes, and
each archetype has its own design and review concerns. These agents capture the
archetypes so a quant can design or review a candidate strategy with the right lens.

They are design and review roles, not signal generators. Every candidate a
strategy agent helps shape still goes through the spec-driven flow and the
leakage/backtest gates before it is trusted.

## Agents (by archetype)

| Agent | Archetype | Typical asset classes |
| --- | --- | --- |
| `momentum_trend/` | Cross-sectional & time-series momentum, trend-following | equities, futures, FX, commodities |
| `mean_reversion_statarb/` | Mean reversion, pairs/stat-arb, index & ETF arbitrage | equities, ETFs, futures |
| `carry/` | Carry and roll-down (FX, rates, commodity, dividend) | FX, fixed income, commodities |
| `value_factor/` | Value, quality, size, low-vol and other factor styles | equities, multi-asset |
| `volatility_options/` | Variance risk premium, vol arbitrage, options overlays | options, volatility, equities |
| `event_driven_arbitrage/` | Merger/risk arb, index rebalancing, earnings, convertibles | equities, credit, convertibles |
| `macro_multi_asset/` | Global macro, allocation, risk parity, tactical tilts | multi-asset |
| `market_making_microstructure/` | Liquidity provision, execution alpha, order-book strategies | equities, futures, FX, crypto |

## Shared Principles

Every strategy agent upholds the constitution and the shared standard
`instructions/trading_strategies.md`:

- **Economic rationale first.** State why the edge should exist and persist before
  any backtest; a pattern without a mechanism is a coincidence until proven.
- **Point-in-time and leakage-free.** Signals use only information available at the
  decision time; universes and fundamentals are point-in-time. See
  `instructions/point_in_time.md`.
- **Costs and capacity are core, not afterthoughts.** Transaction costs, slippage,
  borrow/financing, turnover, and capacity decide whether an edge survives.
- **Overfitting discipline.** Record the number of configurations tried and correct
  for multiple testing; prefer robustness over a single impressive number.
- **Risk is characterized, not assumed.** Exposures, tail behavior, crowding, and
  regime dependence are examined for every archetype.

## Where They Fit

Strategy agents supply the Research/Planning and Testing stages and lean on the
existing domain agents: `research_analyst` (plan), `feature_engineering` and
`modeling` (construction and validation), `backtest_review` (integrity), and
`risk` (exposures and limits). A candidate becomes a spec (`REQ-*`/`AC-*`/`RISK-*`)
and is proven through the `leakage` and `backtest` gates.

## Note On Scope

This is a taxonomy applied with judgment, not a reproduction of the source text.
Each agent describes how to design and review its archetype; specific parameters,
universes, and formulas belong in the strategy's own spec.
