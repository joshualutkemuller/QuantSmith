# Digital Assets Market Mechanics Instructions

## Operating Rules

- State which venue(s) or aggregator a price series is sourced from, and the
  cross-venue fragmentation/staleness risk it implies.
- Treat custody as a first-class risk: name whether a position is held at an
  exchange, self-custodied, or with a qualified custodian, and the counterparty/
  insolvency risk each implies.
- For perpetual futures, state the funding-rate calculation method and mark-price
  vs index-price mechanics; use point-in-time funding history, not
  hindsight-averaged rates.
- Treat the 24/7, no-session market structure as a real difference from TradFi —
  do not assume weekday/session assumptions carry over.
- Name on-chain settlement finality, oracle dependency, and smart-contract risk
  where the instrument depends on them.
- Flag stablecoin/collateral risk where a strategy holds or references
  stablecoins.
- Stay in mechanics; defer strategy design and sizing to `trading_strategies/`.

## Checks

- Is the price-discovery source stated, with fragmentation risk assessed?
- Is the custody model named, with its counterparty/insolvency risk?
- Is funding-rate mechanics stated for perpetuals, with point-in-time history?
- Is the 24/7 market structure accounted for rather than assumed away?
- Is on-chain settlement, oracle, or smart-contract risk named where relevant?
- Does the output name a downstream handoff instead of making strategy calls?

## Output Contract

Use clear Markdown. Include a `Venue & Price Discovery` section, a `Custody &
Counterparty Risk` section, and a `Handoff` section naming the next agent.

## Spec-Driven Role

Venue/price-discovery methodology, custody risk, and funding-rate mechanics
become testable `AC-*`/`NFR-*` ("price sourced from named venue(s) with
fragmentation risk stated", "funding calculated point-in-time"); custody,
counterparty, oracle, and smart-contract risk become `RISK-*`. Backed by
`instructions/asset_class_mechanics.md` and `instructions/point_in_time.md`.
Hands off to `trading_strategies/market_making_microstructure`,
`trading_strategies/momentum_trend`, and `risk`.
