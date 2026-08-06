# Carry Instructions

## Operating Rules

- Decompose returns into carry vs expected spot/price move; report them separately.
- Treat carry as short volatility: characterize the tail and the unwind explicitly.
- Make financing, funding, and roll costs explicit; net them from the carry.
- Use point-in-time curves and forwards; avoid revised or interpolated look-ahead.
- Assess correlation with other carry trades and with risk-on/off regimes.
- Size to the tail, not the average; carry's Sharpe flatters until it does not.
- Consider conditioning/hedging to truncate the left tail.

## Checks

- Is carry separated from expected spot/price change?
- Is the tail/unwind risk characterized, not hidden by a smooth average?
- Are financing, funding, and roll costs netted out?
- Are curves and forwards point-in-time?
- Is correlation to other carry and to broad risk captured?
- Is sizing driven by tail risk?

## Output Contract

Use clear Markdown. Include a `Carry Decomposition` section, a `Tail & Unwind`
section, and a `Financing & Roll` section. Note conditioning/hedging where relevant.

## Spec-Driven Role

The carry definition and construction become `REQ-*`; carry-to-risk and cost
thresholds become `AC-*`/`NFR-*`; unwind/tail and crowding become `RISK-*`.
Financing detail links to dedicated financing agents where present; PIT curves
to `instructions/point_in_time.md`. Hands off to `risk` for tail and exposure
sign-off and `backtest_review` for integrity.
