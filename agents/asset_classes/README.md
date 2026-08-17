# Asset Class Mechanics Agents

This folder groups agents by **asset class** rather than strategy archetype: each
agent owns the market-structure and data mechanics specific to one asset class —
conventions, settlement, sessions, corporate actions/roll, curve construction, and
custody. They exist because the same strategy archetype (see
`agents/trading_strategies/`) behaves differently in equities vs FX vs commodities
vs digital assets, and that difference is mechanical, not strategic.

## Note On Scope

These agents are **mechanics-only**. They do not design or size trading
strategies (`agents/trading_strategies/`). Their job is to hand `trading_strategies/`
and `data_quality`, `risk`, and `optimization` — clean, point-in-time-correct inputs:
adjusted prices, point-in-time universes and curves, named settlement/session
conventions, and scoped custody/counterparty risk. A strategy's edge, sizing, and
risk limits are still decided by the agents that already own those concerns.

## Agents (by asset class)

| Agent | Handles | Typical strategy handoff |
| --- | --- | --- |
| `equities/` | Venues/sessions, corporate-action adjustment, point-in-time index membership, short-sale mechanics, settlement | `trading_strategies/momentum_trend`, `mean_reversion_statarb`, `value_factor`, `event_driven_arbitrage` |
| `fixed_income_rates/` | Day-count/accrual conventions, clean vs dirty price, point-in-time curve construction, credit spreads/ratings, auction/on-the-run status | `trading_strategies/carry`, `macro_multi_asset`, `event_driven_arbitrage`; `optimization/` |
| `fx/` | Spot/forward/swap conventions, settlement/value dates, fixing-window risk, regional session structure | `trading_strategies/carry`, `macro_multi_asset` |
| `commodities/` | Futures curve shape, roll mechanics and roll yield, physical delivery vs cash settlement, storage/carry cost, seasonality | `trading_strategies/carry`, `momentum_trend`, `macro_multi_asset` |
| `digital_assets/` | Venue fragmentation, custody/counterparty risk, perpetual-funding mechanics, 24/7 session structure, on-chain/oracle risk | `trading_strategies/market_making_microstructure`, `momentum_trend` |

## Shared Principles

Every asset-class agent upholds the constitution and the shared standard
`instructions/asset_class_mechanics.md`:

- **Mechanics, not strategy.** State market structure and data handling; leave
  edge, sizing, and signal design to `trading_strategies/`.
- **Point-in-time conventions.** Index membership, curve nodes, ratings, and
  corporate-action adjustments are snapshotted as of the decision date. See
  `instructions/point_in_time.md`.
- **Name settlement and session reality.** Settlement lag and session structure
  change what is tradable and knowable at decision time.
- **Corporate actions and roll are leakage surfaces**, not incidental data.
- **Custody, counterparty, and delivery risk are named**, not assumed away.

## Where They Fit

Asset-class agents supply the Planning and Testing stages, upstream of
`trading_strategies/` and alongside `data_quality`. A request that names both a
strategy archetype and an asset class (e.g. "review this momentum signal on
crypto perpetuals") routes through the relevant asset-class agent first for
mechanics, then to the matching `trading_strategies/` agent for design and review.

## Taxonomy Note

The five asset classes here are a taxonomy applied with judgment: fixed income and
credit are grouped together because their conventions (curves, spreads, ratings)
are closely coupled; commodities and futures mechanics are grouped because most
commodity exposure is expressed through futures. Add a new asset-class agent only
when a class's mechanics are genuinely distinct from the five covered — not to
mirror every instrument type.
