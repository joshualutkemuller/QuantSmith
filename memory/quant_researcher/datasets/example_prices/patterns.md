# Patterns Memory: quant_researcher × example_prices

> Recipes that worked for this workflow on this dataset. Reference example.

- **Momentum construction:** original-vintage `close_adj` → convert to common
  currency → reindex to trading calendar → 12-1 month return → cross-sectional
  z-score within the liquid universe.
- **Universe:** top 80% by 20-day median dollar volume, halted days excluded.
- **Return calc:** compute on reindexed prices so holidays do not create fake jumps.
