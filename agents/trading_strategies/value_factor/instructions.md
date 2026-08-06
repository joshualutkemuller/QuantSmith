# Value & Factor Instructions

## Operating Rules

- Use point-in-time fundamentals: respect reporting lags and original vintages.
- Never use restated values that were unavailable at the decision date.
- Test definition robustness; small changes should not flip the result.
- Assess crowding and decay against known factors before claiming novelty.
- Neutralize deliberately (sector, size, beta) and state the residual exposure.
- Report the premium net of costs, turnover, and capacity.
- Control for multiple testing across the factors and variants screened.

## Checks

- Are fundamentals point-in-time, with reporting lag and restatement handled?
- Is the factor robust to reasonable definition changes?
- Is it distinct from known factors, or crowded/decayed?
- Are neutralizations appropriate, and what exposure remains?
- Does a net premium survive costs and capacity?
- Is multiple testing across variants controlled?

## Output Contract

Use clear Markdown. Include a `Construction & PIT` section, a `Robustness &
Crowding` section, and a `Net Premium` section. State neutralizations explicitly.

## Spec-Driven Role

Factor definitions become `REQ-*`; point-in-time construction and net-premium
thresholds become `AC-*`/`NFR-*`; crowding and decay become `RISK-*`. Fundamental
leakage is enforced by `instructions/point_in_time.md` and the `leakage` gate;
data provenance via a data contract. Hands off to `feature_engineering` (construction),
`modeling` (validation), and `risk` (exposures).
