"""Acceptance tests for spec 0001 — daily cross-sectional momentum signal.

Each test is named for the acceptance criterion it covers (see
``specs/0001-daily-momentum-signal/tasks.md``). Standard-library only.
"""

from __future__ import annotations

import random

from quantsmith.pipelines.momentum_signal import (
    PriceBar,
    build_signal,
    liquidity_filter,
    raw_momentum,
)

LOOKBACK = 20
SKIP = 2
NAMES = ["AAA", "BBB", "CCC", "DDD", "EEE"]


def make_panel(n_days: int = 40, seed: int = 3):
    rng = random.Random(seed)
    bars = []
    for name in NAMES:
        price = 100.0
        for t in range(n_days):
            price *= 1.0 + rng.uniform(-0.02, 0.02)
            bars.append(PriceBar(t=t, name=name, close=round(price, 6)))
    return bars


# --- AC-001: momentum uses only data on or before D minus the skip window ---


def test_no_lookahead_AC_001():
    panel = make_panel()
    raw = raw_momentum(panel, lookback=LOOKBACK, skip=SKIP)
    t, name = 25, "AAA"
    assert (t, name) in raw
    baseline = raw[(t, name)]

    # Perturb the price AT the decision day t (inside the skipped window) and after.
    perturbed = [
        PriceBar(b.t, b.name, b.close * (10.0 if (b.name == name and b.t >= t - SKIP + 1) else 1.0))
        for b in panel
    ]
    raw2 = raw_momentum(perturbed, lookback=LOOKBACK, skip=SKIP)
    assert raw2[(t, name)] == baseline  # nothing at or after t-skip+1 affects it


# --- AC-002: each date's included cross-section is z-scored ---


def test_cross_section_normalized_AC_002():
    panel = make_panel()
    scores = build_signal(panel, lookback=LOOKBACK, skip=SKIP)
    by_date = {}
    for (t, _n), v in scores.items():
        by_date.setdefault(t, []).append(v)
    for t, vals in by_date.items():
        if len(vals) < 2:
            continue
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
        assert abs(mean) < 1e-9
        assert abs(var ** 0.5 - 1.0) < 1e-9


# --- AC-003: reproducible ---


def test_reproducible_output_AC_003():
    panel = make_panel()
    assert build_signal(panel, lookback=LOOKBACK, skip=SKIP) == build_signal(
        panel, lookback=LOOKBACK, skip=SKIP
    )


# --- REQ-003: liquidity filter excludes illiquid names ---


def test_liquidity_filter_excludes():
    panel = make_panel()
    raw = raw_momentum(panel, lookback=LOOKBACK, skip=SKIP)
    # Make CCC the least liquid on every date; everyone else liquid.
    liquidity = {(t, n): (1.0 if n == "CCC" else 100.0) for (t, n) in raw}
    kept = liquidity_filter(raw, liquidity, min_percentile=0.5)
    assert all(n != "CCC" for (_t, n) in kept)
    assert any(n == "AAA" for (_t, n) in kept)
