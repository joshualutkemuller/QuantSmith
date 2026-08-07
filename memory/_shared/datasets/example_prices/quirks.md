# Quirks Memory: example_prices

> The "need-to-knows" learned about this source. Reference example.

- **Tickers are reused.** Join on `security_id`, never the ticker — a delisted
  ticker can be reassigned to a different company.
- **`volume = 0` means halted, not missing.** Do not impute; filter or flag.
- **Mixed currencies.** `currency` is not always USD; convert before any
  cross-sectional ranking or the ranks are meaningless.
- **Adjusted prices are restated.** `close_adj` changes retroactively after splits/
  dividends — use the original vintage for point-in-time work (leakage risk).
- **Exchange-holiday rows are absent, not zero.** Reindex to the trading calendar
  before computing returns.
