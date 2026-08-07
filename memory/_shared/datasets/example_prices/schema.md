# Schema Memory: example_prices

> Learned schema for the `example_prices` daily equity price source. Reference
> example — metadata only, no credentials or data rows. Records are catalogued in
> `provenance.yaml`.

## Grain & Keys

- **Grain:** one row per (date, security_id).
- **Primary key:** (date, security_id) — unique per grain.

## Fields

| Field | Type | Notes |
| --- | --- | --- |
| date | date | Trading date (exchange calendar). |
| security_id | string | Point-in-time identifier; not the ticker (tickers are reused). |
| close_adj | float | Split/dividend-adjusted close. |
| volume | int | Shares; zero on halted days, not null. |
| currency | string | Some names quote in non-USD; convert before cross-sectional use. |

## Known Availability

- Prices land ~T+0 after close; use with a one-day lag for point-in-time signals.
