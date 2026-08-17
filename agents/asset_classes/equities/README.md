# Equities Market Mechanics Agent

## Purpose

The Equities Market Mechanics Agent handles the market-structure and data
mechanics specific to listed equities: venues, sessions, corporate actions, index
membership, short-sale mechanics, and settlement. It hands a strategy or risk
agent clean, point-in-time-correct inputs instead of letting instrument mechanics
become a silent source of leakage or bias.

## Use When

- A signal or backtest uses equity price/volume series that need corporate-action
  adjustment.
- A universe needs point-in-time index membership (not today's constituents).
- A strategy shorts equities and needs locate/hard-to-borrow mechanics scoped.
- Venue fragmentation (primary exchange vs ATS/dark pools), auctions, halts, or
  tick/lot conventions affect execution or signal timing.

## Inputs

- The instrument(s), venue(s), and the date range in question.
- Raw price/volume series and their adjustment status.
- The universe definition and its membership/reconstitution rule.
- Any short-sale, locate, or borrow context relevant to the request.

## Outputs

- A market-structure brief: venue(s), session structure, tick/lot size, settlement
  lag (T+1/T+2).
- The corporate-action adjustment method used (splits, dividends, spin-offs) and
  its look-ahead risk.
- A point-in-time index-membership treatment (reconstitution dates, no
  survivorship).
- Short-sale mechanics scoped for handoff: locate requirement, Reg SHO relevance,
  hard-to-borrow flag.
- A named handoff to `trading_strategies/` or `risk`.

## Example Requests

- "Review this momentum universe for point-in-time index membership."
- "Check whether this backtest's price series is correctly split/dividend-adjusted."
- "Scope the short-sale/locate mechanics for this pairs-trade candidate before
  risk review."

## Required Review Themes

- Corporate-action adjustment method and its look-ahead risk.
- Point-in-time index membership; no future reconstitution look-ahead.
- Venue/session structure: continuous vs auction, primary exchange vs ATS/dark pool.
- Settlement lag (T+1 US / T+2 elsewhere) relative to signal decision time.
- Short-sale mechanics scoped (locate, Reg SHO, hard-to-borrow).
- Halts, circuit breakers, and tick/lot conventions where they affect execution.
