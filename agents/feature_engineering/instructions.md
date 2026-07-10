# Feature Engineering Agent Instructions

## Operating Rules

- For every input, state when it is actually known (point-in-time availability).
- Reject any transform that uses future information relative to the label.
- Fit normalization and scaling on training data only; never on the full sample.
- Prefer transforms that are stationary or explicitly stationarized.
- Assess feature drift and stability across regimes, not just in-sample.
- Keep feature computation reproducible: pinned inputs, seeds, no hidden state.
- Document each feature so another researcher can recompute it exactly.

## Checks

- When is each input known, and does the feature respect that timing?
- Does any transform peek at the future or leak the target?
- Is normalization fit only on training data?
- Is the feature stationary and stable, or does it drift?
- Can the feature be recomputed deterministically from documented inputs?
- Is there a data dictionary entry for each feature?

## Output Contract

Use clear Markdown sections. Always include a `Point-in-Time & Leakage` section
and a `Data Dictionary` section. When normalization is involved, state exactly
what data it is fit on.

## Spec-Driven Role

Point-in-time and leakage requirements are acceptance criteria, not comments:
encode "no look-ahead" and "normalization fit on train only" as `AC-*` in the
spec so the testing stage must prove them. See `instructions/point_in_time.md`.
