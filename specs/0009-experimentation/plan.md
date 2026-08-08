# Plan: Experiment (A/B test) analysis

- **Spec:** 0009-experimentation (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Implement the standard two-proportion toolkit with the discipline built in.
Statistical consistency holds *by construction* because a single Wald standard error
drives both the p-value and the confidence interval, and honesty holds by
construction because the end-to-end readout computes power and sample-ratio validity
*before* it is allowed to name a winner. Pure Python (normal CDF via `math.erf`,
inverse normal via Acklam's approximation) so the reference runs anywhere.

## Agent Routing

The workflow is the Data Analyst chain's experimentation branch (see
`docs/workflows.md` → *Data Analyst*):

```text
planning_requirements -> analytics/experimentation   # design: MDE, alpha, power, sample size
  -> (run experiment; assignment/logging are upstream)
  -> analytics/experimentation                        # readout: SRM, test, verdict
  -> quality-guard-agent -> reporting-agent
```

Adjacent: `analytics/metrics_semantic_layer` supplies the governed conversion
measure; `machine_learning/causal_uplift` handles observational/heterogeneous-effect
questions this node deliberately does not.

## Architecture & Components

- `required_sample_size(baseline, mde, alpha, power)` → per-arm n (power analysis).
- `sample_ratio_mismatch(control_n, treatment_n, expected_share, alpha)` → bool guard.
- `analyze_proportions(cn, cx, tn, tx, alpha)` → `ProportionTest` (diff, lift,
  p-value, CI, significant) from one shared Wald SE.
- `analyze_experiment(...)` → `ExperimentReadout` composing power, SRM, and the test
  into a verdict with explicit caveats.
- `_norm_cdf` / `_norm_ppf` — stdlib normal helpers.

## Interfaces & Data Contracts

- Input: per-arm subject and conversion counts, plus the pre-registered design
  (baseline, MDE, alpha, power, expected share).
- Output: a `ProportionTest` or an `ExperimentReadout` with a verdict in
  {`treatment`, `control`, `no_difference`, `inconclusive`} and caveats.
- No look-ahead concerns; the guard is against *peeking* (early stopping), handled by
  requiring the pre-registered sample size before concluding.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Shared SE makes p-value and CI consistent; verdict gated on power and SRM. |
| P5 Reversibility | yes | Pure analysis; no state to roll back. |
| P6 Observability | yes | Caveats enumerate SRM and underpowered conditions explicitly. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | No winner without adequate power and valid allocation; div-by-zero lift is NaN. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `required_sample_size` | T-001 |
| REQ-002 | `analyze_proportions` (shared SE) | T-002 |
| REQ-003 | `sample_ratio_mismatch` | T-003 |
| REQ-004 | `analyze_experiment` verdict guard | T-004 |
| NFR-001 | deterministic math | T-002, T-004 |
| NFR-002 | one SE for p-value and CI | T-002 |
| NFR-003 | verdict gated on power + SRM | T-004 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Test SE | Unpooled (Wald), shared by p-value and CI | Pooled SE for the test, unpooled for the CI | Sharing one SE guarantees the CI and p-value never disagree (NFR-002). |
| Stopping | Fixed pre-registered sample size | Peek-and-stop | Early stopping without correction inflates false positives (RISK-001). |
| Metric | Proportions | Continuous (t-test) | Proportions cover the most common A/B case first; t-test is a follow-up. |
| Div-by-zero lift | NaN | 0.0 | 0.0 is a misleading lift; NaN is honest (P10). |

## Validation Strategy

- AC-001: assert required n increases as MDE shrinks (and as power rises).
- AC-002: assert a clear effect is significant with a CI excluding 0; a null is not.
- AC-003: assert balanced allocation passes and a gross imbalance flags SRM.
- AC-004: assert underpowered/SRM cases return "inconclusive"; a valid powered effect
  names the winner.
- AC-005: across several cases, assert the CI excludes 0 iff p < alpha.
- AC-006: assert identical inputs give identical results.

## Rollout, Observability & Rollback

A library consumed by the reporting and quality-guard agents. There is nothing to
roll back; a changed design (alpha, power, MDE) simply changes the required sample
size and the verdict. Caveats travel with every readout so a reviewer sees why a
result is or is not conclusive.

## Open Questions

- Add continuous-metric (t-test), multi-arm correction, sequential testing, and
  variance reduction (CUPED) as follow-up slices.
