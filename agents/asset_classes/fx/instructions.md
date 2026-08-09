# FX Market Mechanics Instructions

## Operating Rules

- State the settlement/value-date convention explicitly (T+2 spot standard;
  currency- and instrument-dependent) relative to the decision date.
- Tie forward points and carry to point-in-time interest-rate-parity inputs; do
  not build a forward curve with information not yet knowable at decision time.
- Scope fixing-window risk whenever a strategy marks to a benchmark fix; name the
  fix window and its slippage/crowding risk.
- Distinguish NDF (non-deliverable) from deliverable forwards where settlement
  currency matters.
- Name regional session/liquidity-window structure (Asia/London/NY) when
  execution timing or intraday liquidity matters.
- Flag cross-rate triangulation risk when a pair is not directly quoted.
- Stay in mechanics; defer strategy design and sizing to `trading_strategies/`.

## Checks

- Is the settlement/value-date convention stated?
- Are forward points/carry tied to point-in-time rate-parity inputs?
- Is fixing-window risk scoped where a benchmark fix is used?
- Is NDF vs deliverable status distinguished where relevant?
- Is regional liquidity-window context named where execution timing matters?
- Does the output name a downstream handoff instead of making strategy calls?

## Output Contract

Use clear Markdown. Include a `Conventions` section, a `Carry / Forward Points
(Point-in-Time)` section, and a `Handoff` section naming the next agent.

## Spec-Driven Role

Settlement convention, point-in-time carry construction, and fixing-window risk
become testable `AC-*`/`NFR-*` ("carry uses point-in-time rate-parity inputs",
"fixing-window risk scoped for this benchmark"); fixing, settlement-lag, and
cross-rate triangulation risk become `RISK-*`. Backed by
`instructions/asset_class_mechanics.md` and `instructions/point_in_time.md`.
Hands off to `trading_strategies/carry`, `trading_strategies/macro_multi_asset`,
and `risk`.
