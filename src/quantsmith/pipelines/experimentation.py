"""Reference pipeline for spec 0009 — experiment (A/B test) analysis.

This module makes the ``0009-experimentation`` spec *executable*. It is a
deterministic, standard-library-only reference for planning and analyzing two-arm
proportion experiments the way an analyst should: size the experiment before running
it, test the result with a confidence interval that agrees with the p-value, guard
against sample-ratio mismatch, and refuse to declare a winner when the experiment is
underpowered or invalid.

Guarantees held by construction:

* REQ-001 / AC-001 — required sample size grows as the minimum detectable effect
  shrinks.
* REQ-002 / NFR-002 / AC-002, AC-005 — a single Wald standard error drives both the
  two-sided p-value and the confidence interval, so the CI excludes 0 exactly when
  ``p < alpha``.
* REQ-003 / AC-003 — sample-ratio mismatch is detected and invalidates the readout.
* REQ-004 / NFR-003 / AC-004 — the verdict is "inconclusive" unless the
  pre-registered sample size is reached and allocation is valid (a peeking guard).
* NFR-001 / AC-006 — every computation is deterministic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# Normal distribution helpers (stdlib only)
# ---------------------------------------------------------------------------


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _norm_ppf(p: float) -> float:
    """Inverse standard-normal CDF via Acklam's rational approximation.

    Accurate to ~1e-9 over (0, 1); deterministic.
    """
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")

    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00]

    plow, phigh = 0.02425, 1.0 - 0.02425
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    if p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1.0)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1.0)


# ---------------------------------------------------------------------------
# Power analysis — REQ-001
# ---------------------------------------------------------------------------


def required_sample_size(
    baseline_rate: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    """Per-arm sample size for a two-proportion test with equal allocation.

    ``mde`` is the absolute minimum detectable effect (e.g. 0.02 = +2pp). Returns the
    number of subjects *per arm*, rounded up.
    """
    if not 0.0 < baseline_rate < 1.0:
        raise ValueError("baseline_rate must be in (0, 1)")
    if mde <= 0.0:
        raise ValueError("mde must be positive")
    p1 = baseline_rate
    p2 = baseline_rate + mde
    if not 0.0 < p2 < 1.0:
        raise ValueError("baseline_rate + mde must be in (0, 1)")

    z_alpha = _norm_ppf(1.0 - alpha / 2.0)
    z_beta = _norm_ppf(power)
    pbar = (p1 + p2) / 2.0
    term = z_alpha * math.sqrt(2.0 * pbar * (1.0 - pbar)) + \
        z_beta * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    n = (term * term) / (mde * mde)
    return int(math.ceil(n))


# ---------------------------------------------------------------------------
# Sample-ratio-mismatch guard — REQ-003
# ---------------------------------------------------------------------------


def sample_ratio_mismatch(
    control_n: int,
    treatment_n: int,
    expected_share: float = 0.5,
    alpha: float = 0.001,
) -> bool:
    """Return True when the arm allocation deviates from the expected split.

    A two-sided proportion test on the observed control share against
    ``expected_share``. Uses a strict alpha (1e-3 by default) as is conventional for
    SRM checks. True means "mismatch — invalidate the experiment".
    """
    total = control_n + treatment_n
    if total == 0:
        return False
    observed = control_n / total
    se = math.sqrt(expected_share * (1.0 - expected_share) / total)
    if se == 0.0:
        return False
    z = (observed - expected_share) / se
    p = 2.0 * (1.0 - _norm_cdf(abs(z)))
    return p < alpha


# ---------------------------------------------------------------------------
# Result analysis — REQ-002
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ProportionTest:
    diff: float
    lift: float
    p_value: float
    ci_low: float
    ci_high: float
    significant: bool


def analyze_proportions(
    control_n: int,
    control_x: int,
    treatment_n: int,
    treatment_x: int,
    alpha: float = 0.05,
) -> ProportionTest:
    """Two-proportion Wald test with a matching confidence interval.

    A single unpooled standard error drives both the p-value and the CI, so the CI
    excludes 0 exactly when ``p < alpha`` (NFR-002 / AC-005).
    """
    if control_n <= 0 or treatment_n <= 0:
        raise ValueError("arm sizes must be positive")
    p1 = control_x / control_n
    p2 = treatment_x / treatment_n
    diff = p2 - p1
    se = math.sqrt(p1 * (1.0 - p1) / control_n + p2 * (1.0 - p2) / treatment_n)
    z_crit = _norm_ppf(1.0 - alpha / 2.0)

    if se == 0.0:
        p_value = 0.0 if diff != 0.0 else 1.0
        margin = 0.0
    else:
        z = diff / se
        p_value = 2.0 * (1.0 - _norm_cdf(abs(z)))
        margin = z_crit * se

    ci_low, ci_high = diff - margin, diff + margin
    significant = (ci_low > 0.0) or (ci_high < 0.0)
    lift = diff / p1 if p1 != 0.0 else float("nan")
    return ProportionTest(diff, lift, p_value, ci_low, ci_high, significant)


# ---------------------------------------------------------------------------
# End-to-end experiment readout — REQ-004 / NFR-003
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExperimentReadout:
    test: ProportionTest
    srm_ok: bool
    powered: bool
    required_n: int
    verdict: str  # "treatment" | "control" | "no_difference" | "inconclusive"
    caveats: List[str] = field(default_factory=list)


def analyze_experiment(
    control_n: int,
    control_x: int,
    treatment_n: int,
    treatment_x: int,
    baseline_rate: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
    expected_share: float = 0.5,
) -> ExperimentReadout:
    """Plan-aware readout: size, validate allocation, test, and decide honestly.

    The verdict is "inconclusive" whenever the experiment fails its sample-ratio
    check or has not reached the pre-registered per-arm sample size — even if the
    raw test is significant. This is the peeking / underpowered guard (REQ-004).
    """
    required_n = required_sample_size(baseline_rate, mde, alpha=alpha, power=power)
    srm = sample_ratio_mismatch(control_n, treatment_n, expected_share=expected_share)
    powered = min(control_n, treatment_n) >= required_n
    test = analyze_proportions(control_n, control_x, treatment_n, treatment_x, alpha=alpha)

    caveats: List[str] = []
    if srm:
        caveats.append("sample-ratio mismatch: arm allocation is invalid; do not conclude")
    if not powered:
        caveats.append(
            f"underpowered: {min(control_n, treatment_n)} per arm < required {required_n}"
        )

    if srm or not powered:
        verdict = "inconclusive"
    elif not test.significant:
        verdict = "no_difference"
    elif test.diff > 0.0:
        verdict = "treatment"
    else:
        verdict = "control"

    return ExperimentReadout(
        test=test,
        srm_ok=not srm,
        powered=powered,
        required_n=required_n,
        verdict=verdict,
        caveats=caveats,
    )
