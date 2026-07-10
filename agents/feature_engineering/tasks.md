# Feature Engineering Agent Tasks

## Document Feature Set

Input: feature definitions or code and source data timing.

Output: feature definitions with point-in-time semantics and a data dictionary.

## Leakage Review

Input: feature transforms and the label definition.

Output: per-transform review of look-ahead, target leakage, and normalization leakage.

## Stability Assessment

Input: feature history over time.

Output: stationarity and drift assessment with regime-by-regime behavior.

## Normalization Plan

Input: feature set and intended model.

Output: scaling/normalization plan that fits on training data only, with the
fit/apply boundary made explicit.
