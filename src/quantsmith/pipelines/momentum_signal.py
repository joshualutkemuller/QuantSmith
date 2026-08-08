"""Reference pipeline for spec 0001 — daily cross-sectional momentum signal.

This module makes the original ``0001-daily-momentum-signal`` reference *executable*,
so the whole quant chain — signal (`0001`) → forecast (`0006`) → portfolio (`0007`)
→ execution (`0012`) — is runnable end to end. It is deterministic and
standard-library only.

The signal is a pure transform from a point-in-time price panel to a per-name daily
score:

    load -> raw_momentum (12-1 window) -> liquidity_filter -> normalize (z-score)

Guarantees held by construction:

* REQ-001 / AC-001 — momentum for day D uses only prices on or before D minus the
  skip window; a later price never changes an earlier score (no look-ahead).
* REQ-002 / AC-002 — each day's included cross-section is z-scored (mean ~0, std ~1).
* REQ-003 — names failing the liquidity filter are excluded from that day.
* NFR-001 / AC-003 — the same input panel yields identical output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Tuple

Sample = Tuple[int, str]  # (date_index, name)


@dataclass(frozen=True)
class PriceBar:
    """One adjusted-close observation for a name on a trading-day index."""

    t: int
    name: str
    close: float


def _closes_by_name(panel: Sequence[PriceBar]) -> Dict[str, Dict[int, float]]:
    out: Dict[str, Dict[int, float]] = {}
    for bar in panel:
        out.setdefault(bar.name, {})[bar.t] = bar.close
    return out


def raw_momentum(
    panel: Sequence[PriceBar],
    lookback: int = 252,
    skip: int = 21,
) -> Dict[Sample, float]:
    """Trailing ``lookback``-day return skipping the most recent ``skip`` days.

    Momentum for (t, name) is ``close[t-skip] / close[t-lookback] - 1``. The most
    recent price used is at ``t - skip``, so no data after that enters the score —
    no look-ahead relative to the decision day ``t`` (AC-001).
    """
    if skip < 0 or lookback <= skip:
        raise ValueError("require 0 <= skip < lookback")
    by_name = _closes_by_name(panel)
    out: Dict[Sample, float] = {}
    for name, closes in by_name.items():
        for t in closes:
            a = t - lookback
            b = t - skip
            if a in closes and b in closes and closes[a] > 0:
                out[(t, name)] = closes[b] / closes[a] - 1.0
    return out


def liquidity_filter(
    raw: Dict[Sample, float],
    liquidity: Dict[Sample, float],
    min_percentile: float,
) -> Dict[Sample, float]:
    """Drop names below the per-date liquidity percentile.

    ``min_percentile`` is in [0, 1]; on each date, names whose liquidity ranks below
    that percentile of the day's cross-section are excluded (REQ-003).
    """
    if not 0.0 <= min_percentile <= 1.0:
        raise ValueError("min_percentile must be in [0, 1]")
    by_date: Dict[int, list] = {}
    for (t, name) in raw:
        by_date.setdefault(t, []).append(name)

    kept: Dict[Sample, float] = {}
    for t, names in by_date.items():
        vals = sorted(liquidity.get((t, n), 0.0) for n in names)
        if not vals:
            continue
        idx = int(min_percentile * (len(vals) - 1))
        threshold = vals[idx]
        for n in names:
            if liquidity.get((t, n), 0.0) >= threshold:
                kept[(t, n)] = raw[(t, n)]
    return kept


def normalize(raw: Dict[Sample, float]) -> Dict[Sample, float]:
    """Per-date cross-sectional z-score (mean ~0, std ~1) over included names."""
    by_date: Dict[int, list] = {}
    for key in raw:
        by_date.setdefault(key[0], []).append(key)

    out: Dict[Sample, float] = {}
    for _t, keys in by_date.items():
        vals = [raw[k] for k in keys]
        n = len(vals)
        mean = sum(vals) / n
        if n < 2:
            for k in keys:
                out[k] = 0.0
            continue
        var = sum((v - mean) ** 2 for v in vals) / (n - 1)
        std = var ** 0.5
        for k in keys:
            out[k] = 0.0 if std == 0 else (raw[k] - mean) / std
    return out


def build_signal(
    panel: Sequence[PriceBar],
    lookback: int = 252,
    skip: int = 21,
    liquidity: Optional[Dict[Sample, float]] = None,
    min_liquidity_percentile: Optional[float] = None,
) -> Dict[Sample, float]:
    """Compose the daily cross-sectional momentum signal.

    Returns a score per (date, name): raw 12-1 momentum, optionally liquidity-filtered,
    then per-date cross-sectionally z-scored. Deterministic (NFR-001 / AC-003).
    """
    raw = raw_momentum(panel, lookback=lookback, skip=skip)
    if liquidity is not None and min_liquidity_percentile is not None:
        raw = liquidity_filter(raw, liquidity, min_liquidity_percentile)
    return normalize(raw)
