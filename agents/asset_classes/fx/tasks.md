# FX Market Mechanics Tasks

## Conventions Brief

Input: the currency pair(s), instrument type, and date range.

Output: settlement/value-date and spot-vs-forward/swap conventions brief.

## Carry & Forward-Points Review

Input: interest-rate data feeding a carry calculation.

Output: a point-in-time forward-points/carry treatment, with any rate-parity
look-ahead flagged.

## Fixing-Window Risk Scoping

Input: a strategy that marks to a benchmark fix.

Output: the fixing window named, with its slippage and crowding risk scoped for
handoff.

## Session & Liquidity Review

Input: an intraday or execution-timing-sensitive FX strategy.

Output: regional liquidity-window context (Asia/London/NY) and any cross-rate
triangulation risk.
