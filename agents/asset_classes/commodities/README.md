# Commodities & Futures Mechanics Agent

## Purpose

The Commodities & Futures Mechanics Agent handles the conventions and roll
mechanics specific to commodity futures: curve shape (contango/backwardation),
roll yield and roll-date scheduling, physical delivery vs cash settlement, storage
and carry cost, and seasonality. It hands a strategy or financing agent clean,
point-in-time-correct inputs instead of letting roll mechanics become a silent
source of leakage or bias.

## Use When

- A signal or backtest uses a continuous futures series and needs the roll method
  made explicit.
- A carry signal depends on curve shape (contango/backwardation) and storage/
  convenience-yield economics.
- A position approaches contract expiry and physical-delivery risk needs scoping.
- Seasonality (weather, harvest, driving season) is a claimed driver and needs a
  point-in-time check.

## Inputs

- The commodity, contract(s), and date range in question.
- The continuous-series construction method (roll method, roll dates/window).
- Curve data (front month vs deferred months) for contango/backwardation
  assessment.
- Any physical-delivery, storage, or seasonality context relevant to the request.

## Outputs

- A conventions brief: contract specs (tick, lot, expiry calendar), physical
  delivery vs cash settlement.
- A roll-mechanics treatment: roll method, roll-date schedule, and the roll
  yield/cost it implies.
- A curve-shape (contango/backwardation) and storage/convenience-yield view.
- Physical-delivery risk scoped near expiry, where relevant.
- A named handoff to `trading_strategies/` or `risk`.

## Example Requests

- "Review this continuous futures series for the roll method used and its cost."
- "Assess whether this signal's seasonality claim holds under a point-in-time
  check."
- "Scope physical-delivery risk for this position approaching contract expiry."

## Required Review Themes

- Roll method and roll-date schedule stated explicitly, with the roll yield/cost
  it implies.
- Curve shape (contango/backwardation) and storage/convenience-yield economics.
- Physical delivery vs cash settlement, with delivery risk scoped near expiry.
- Point-in-time seasonality claims (weather, harvest, driving season), not
  hindsight pattern-matching.
- Contract specs (tick, lot, expiry calendar) stated where execution-relevant.
- Storage and carry cost netted where they drive the strategy's economics.
