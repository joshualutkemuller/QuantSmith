# Tasks: Experiment (A/B test) analysis

- **Spec:** 0009-experimentation (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test. Routing agents are noted per task.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Statistical consistency holds: one shared standard error for p-value and CI.
- No winner is declared without adequate power and valid allocation.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Agent | Notes |
| --- | --- | --- | --- | --- | --- |
| T-001 | Implement `required_sample_size` (two-proportion power analysis). | REQ-001 | done | `experimentation` | Per-arm, equal allocation; matches standard references. |
| T-002 | Implement `analyze_proportions` (Wald test + matching CI, one shared SE). | REQ-002, NFR-001, NFR-002 | done | `experimentation` | CI excludes 0 iff p < alpha. |
| T-003 | Implement `sample_ratio_mismatch` (allocation guard). | REQ-003 | done | `quality-guard-agent` | Strict alpha; True invalidates the experiment. |
| T-004 | Implement `analyze_experiment` verdict gated on power and SRM. | REQ-004, NFR-003 | done | `experimentation` / `reporting-agent` | "inconclusive" unless powered and valid. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

The runtime is a standard-library-only reference in
`src/quantsmith/pipelines/experimentation.py` (normal CDF via `math.erf`, inverse
normal via Acklam's approximation). Production may swap in a stats library; the
contract — sized, allocation-checked, power-gated, CI-consistent — is unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_experimentation.py::test_sample_size_monotonic_in_mde_AC_001` | done |
| AC-002 | `tests/test_experimentation.py::test_significance_detection_AC_002` | done |
| AC-003 | `tests/test_experimentation.py::test_sample_ratio_mismatch_AC_003` | done |
| AC-004 | `tests/test_experimentation.py::test_verdict_guards_underpowered_and_srm_AC_004` | done |
| AC-005 | `tests/test_experimentation.py::test_pvalue_ci_agree_AC_005` | done |
| AC-006 | `tests/test_experimentation.py::test_deterministic_AC_006` | done |

## Follow-ups

- Add continuous-metric (t-test) experiments and multi-arm correction.
- Add sequential/Bayesian designs and variance reduction (CUPED).
- Connect the governed conversion measure from `0008-metrics-semantic-layer` as the
  experiment metric source.