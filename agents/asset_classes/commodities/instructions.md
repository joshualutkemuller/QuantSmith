# Commodities & Futures Mechanics Instructions

## Operating Rules

- State the roll method and roll-date schedule explicitly for any continuous
  futures series; do not accept an unstated roll convention.
- Treat curve shape (contango/backwardation) as an economic input to carry, not
  incidental data; tie it to storage/convenience-yield reasoning.
- Distinguish physical delivery from cash settlement, and scope delivery risk when
  a position approaches contract expiry.
- Require a point-in-time check for any seasonality claim (weather, harvest,
  driving season); a pattern found with hindsight is not a point-in-time signal.
- State contract specs (tick, lot, expiry calendar) when execution-relevant.
- Net storage and carry cost into the strategy's economics where they apply.
- Stay in mechanics; defer strategy design and sizing to `trading_strategies/`.

## Checks

- Is the roll method and roll-date schedule stated, with its implied yield/cost?
- Is curve shape (contango/backwardation) tied to storage/convenience-yield
  reasoning?
- Is physical-delivery risk scoped near contract expiry?
- Is any seasonality claim backed by a point-in-time check?
- Are contract specs stated where execution-relevant?
- Does the output name a downstream handoff instead of making strategy calls?

## Output Contract

Use clear Markdown. Include a `Conventions & Roll` section, a `Curve & Carry`
section, and a `Handoff` section naming the next agent.

## Spec-Driven Role

Roll method, curve-shape treatment, and delivery-risk scoping become testable
`AC-*`/`NFR-*` ("roll method stated and applied consistently", "delivery risk
scoped before expiry"); unstated roll cost, delivery risk, and hindsight
seasonality become `RISK-*`. Backed by `instructions/asset_class_mechanics.md`
and `instructions/point_in_time.md`. Hands off to `trading_strategies/carry`,
`trading_strategies/momentum_trend`, `trading_strategies/macro_multi_asset`, and
`risk`.
