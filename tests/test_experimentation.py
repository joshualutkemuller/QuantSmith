"""Acceptance tests for spec 0009 — experiment (A/B test) analysis.

Each test is named for the acceptance criterion it covers (see
``specs/0009-experimentation/tasks.md``). Standard-library only.
"""

from __future__ import annotations

from quantsmith.pipelines.experimentation import (
    analyze_experiment,
    analyze_proportions,
    required_sample_size,
    sample_ratio_mismatch,
)


# --- AC-001: required sample size grows as the MDE shrinks ---


def test_sample_size_monotonic_in_mde_AC_001():
    n_big_effect = required_sample_size(0.10, mde=0.05)
    n_small_effect = required_sample_size(0.10, mde=0.01)
    assert n_big_effect > 0
    assert n_small_effect > n_big_effect
    # Tighter power also needs more samples.
    assert required_sample_size(0.10, 0.02, power=0.9) > required_sample_size(0.10, 0.02, power=0.8)


# --- AC-002: significant vs null differences classified correctly ---


def test_significance_detection_AC_002():
    # Large, clear treatment effect over big samples -> significant.
    clear = analyze_proportions(control_n=10000, control_x=1000, treatment_n=10000, treatment_x=1300)
    assert clear.significant is True
    assert clear.p_value < 0.05
    assert clear.ci_low > 0.0  # CI excludes 0

    # Identical rates -> not significant.
    null = analyze_proportions(control_n=10000, control_x=1000, treatment_n=10000, treatment_x=1000)
    assert null.significant is False
    assert null.p_value > 0.05


# --- AC-003: sample-ratio mismatch detection ---


def test_sample_ratio_mismatch_AC_003():
    assert sample_ratio_mismatch(5000, 5000) is False          # balanced -> ok
    assert sample_ratio_mismatch(5000, 5050) is False          # small drift -> ok
    assert sample_ratio_mismatch(5000, 6000) is True           # gross imbalance -> mismatch


# --- AC-004: verdict guards against underpowered / invalid experiments ---


def test_verdict_guards_underpowered_and_srm_AC_004():
    # Significant raw effect but far below the required sample size -> inconclusive.
    small = analyze_experiment(
        control_n=50, control_x=5, treatment_n=50, treatment_x=13,
        baseline_rate=0.10, mde=0.02,
    )
    assert small.test.significant is True
    assert small.powered is False
    assert small.verdict == "inconclusive"
    assert any("underpowered" in c for c in small.caveats)

    # Well-powered, valid, clearly positive -> treatment wins.
    n = required_sample_size(0.10, 0.02) + 100
    good = analyze_experiment(
        control_n=n, control_x=int(0.10 * n), treatment_n=n, treatment_x=int(0.13 * n),
        baseline_rate=0.10, mde=0.02,
    )
    assert good.srm_ok is True
    assert good.powered is True
    assert good.verdict == "treatment"

    # A sample-ratio mismatch invalidates even a powered, significant result.
    srm = analyze_experiment(
        control_n=n, control_x=int(0.10 * n), treatment_n=n * 2, treatment_x=int(0.13 * n * 2),
        baseline_rate=0.10, mde=0.02,
    )
    assert srm.srm_ok is False
    assert srm.verdict == "inconclusive"


# --- AC-005: p-value and confidence interval agree at alpha ---


def test_pvalue_ci_agree_AC_005():
    cases = [
        (10000, 1000, 10000, 1300),   # clearly significant
        (10000, 1000, 10000, 1000),   # null
        (2000, 200, 2000, 230),       # borderline-ish
        (500, 50, 500, 40),           # small, likely n.s.
    ]
    for cn, cx, tn, tx in cases:
        r = analyze_proportions(cn, cx, tn, tx, alpha=0.05)
        ci_excludes_zero = (r.ci_low > 0.0) or (r.ci_high < 0.0)
        assert ci_excludes_zero == (r.p_value < 0.05)
        assert r.significant == ci_excludes_zero


# --- AC-006: deterministic ---


def test_deterministic_AC_006():
    args = dict(
        control_n=8000, control_x=800, treatment_n=8000, treatment_x=910,
        baseline_rate=0.10, mde=0.02,
    )
    a = analyze_experiment(**args)
    b = analyze_experiment(**args)
    assert a == b
    assert required_sample_size(0.10, 0.02) == required_sample_size(0.10, 0.02)
