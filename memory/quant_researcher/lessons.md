# Quant Researcher Lessons

> Cross-dataset lessons for the Quant Researcher workflow. Reference example.

- **Always check the vintage before backtesting.** Restated fields (adjusted prices,
  fundamentals) are the most common leakage source across datasets.
- **Cross-sectional operations need a common unit.** Convert currencies / normalize
  before ranking, everywhere.
- **A zero is a state, not a gap.** Confirm what zero means per field before imputing.
