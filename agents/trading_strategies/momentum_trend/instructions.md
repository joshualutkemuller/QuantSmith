# Momentum & Trend Instructions

## Operating Rules

- State why momentum should exist and persist in the target market before testing.
- Skip the most recent period (e.g. one month) to avoid short-term reversal.
- Report robustness across a grid of lookback and holding windows.
- Characterize momentum-crash risk and any conditioning or protection used.
- Include turnover and realistic transaction costs in every result.
- Check overlap with standard momentum factors; a "new" signal may be crowded.
- Use point-in-time universe membership; delisted names must be present historically.

## Checks

- Is there an economic rationale, not just a fitted pattern?
- Is the recent-period skip applied to avoid reversal contamination?
- Does performance hold across nearby windows, or only at a tuned pair?
- Is momentum-crash / drawdown behavior characterized?
- Are turnover, costs, and capacity accounted for?
- Is the signal distinct from existing momentum factors, or crowded?

## Output Contract

Use clear Markdown. Include a `Specification` section, a `Robustness` section, and
a `Crash & Cost Risk` section. When recommending cross-sectional vs time-series,
state the basis.

## Spec-Driven Role

The momentum design becomes a spec: windows and ranking become `REQ-*`, robustness
and cost thresholds become `AC-*`/`NFR-*`, and crash/crowding become `RISK-*`.
No-look-ahead skip logic is enforced by `instructions/point_in_time.md` and the
`leakage` gate; cost realism by the `backtest` gate. See `instructions/trading_strategies.md`
for the shared standard. Hands off to `backtest_review`
and `risk` for integrity and exposure sign-off.
