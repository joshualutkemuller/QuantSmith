# Market Data Access Adapter

## Use For

- Prices, fundamentals, estimates, corporate actions, borrow data, rates, curves,
  reference data, and vendor feeds.
- Data with entitlements, latency tiers, and point-in-time requirements.

## Delivery Rules

- Preserve vendor, dataset, entitlement context, release time, and as-of time.
- Capture corporate-action adjustment policy.
- Record calendar, timezone, stale/missing-data handling, and symbology mapping.
- Respect vendor redistribution restrictions in artifact delivery.
- Emit a snapshot or checksum when the workflow depends on reproducibility.

## Risks

- Revisions and late vendor corrections can create look-ahead bias.
- Symbology drift can silently corrupt joins.
- Redistribution restrictions can block broad report sharing.
