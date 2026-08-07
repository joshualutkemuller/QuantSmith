# Decisions Memory: quant_researcher × example_prices

> Decisions made and why. Reference example. Links back to the owning spec where one exists.

- **Use original-vintage adjusted prices** (not latest). Rationale: latest restated
  prices leak corporate-action information. Ref: `specs/0001-daily-momentum-signal/`.
- **Liquidity filter = universe percentile**, not a fixed dollar threshold.
  Rationale: a fixed threshold drifts across regimes.
- **Exclude halted (zero-volume) days** from the liquidity metric. Rationale: zero
  volume is a real state and distorts the median otherwise.
