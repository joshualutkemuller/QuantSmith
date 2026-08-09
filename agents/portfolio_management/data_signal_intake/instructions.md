# Data Signal Intake Instructions

## Operating Rules

- Identify prediction time, decision time, holding period, and data availability.
- Require source provenance, data grain, refresh cadence, and owner for every input.
- Distinguish raw signal strength from allocation-ready expected return, risk, or constraint inputs.
- Name stale, missing, or low-confidence inputs and required fallbacks.

## Checks

- Are forecasts calibrated and aligned to the rebalance horizon?
- Are holdings, benchmark, risk, cost, and price data as-of the same decision time?
- Is the baseline portfolio decision defined if a signal is unavailable?

## Output Contract

Use sections: `Input Inventory`, `Timing`, `Signal Evidence`, `Readiness`,
`Risks`, `Validation`, `Workflow Handoff`, and `Spec Updates`.
