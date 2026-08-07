# Pitfalls Memory: example_prices

> What broke before and why. Reference example.

- **Using latest adjusted prices in a backtest.** Restated `close_adj` leaked future
  corporate-action information; results overstated. Use original vintage
  (see `quirks.md`).
- **Ranking across currencies.** A cross-sectional momentum signal ranked raw prices
  across mixed currencies; the signal was mostly an FX artifact.
- **Imputing zero volume as null.** Filled halted-day zero volume, corrupting a
  liquidity filter. Zero volume is a real state.
