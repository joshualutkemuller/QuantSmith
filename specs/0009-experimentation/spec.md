# Spec: Experiment (A/B test) analysis

- **ID:** 0009-experimentation
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Second Data Analyst node (after `0008-metrics-semantic-layer`): plan and read out
> two-arm experiments honestly.

## Problem & Context

The Data Analyst workflow includes an experimentation node that did not exist.
Without it, A/B tests are analyzed ad hoc: teams peek at results and stop early,
declare winners on underpowered samples, ignore sample-ratio mismatch, and report
p-values without a matching confidence interval. Each of these turns noise into a
"result". This spec defines disciplined experiment analysis: size the test before
running it, validate the allocation, test the result with a CI that agrees with the
p-value, and refuse to call a winner when the experiment is underpowered or invalid.

## Goals

- Compute the required per-arm sample size for a target effect, significance, and
  power, so experiments are sized before they run.
- Analyze a two-arm proportion experiment into lift, p-value, and a confidence
  interval that is consistent with the significance decision.
- Detect sample-ratio mismatch and invalidate experiments whose allocation is wrong.
- Produce a verdict that is "inconclusive" unless the pre-registered sample size is
  reached and the allocation is valid — a guard against peeking and underpowered
  conclusions.

## Non-Goals

- Multi-arm / multi-variate testing, sequential/Bayesian designs, and variance
  reduction (CUPED) — documented follow-ups.
- Continuous-metric (t-test) experiments in this slice; proportions first.
- Experiment assignment, logging, or a feature-flag system (upstream of this node).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall compute the required per-arm sample size for a baseline rate, minimum detectable effect, significance level, and power. | must |
| REQ-002 | The system shall analyze a two-arm proportion experiment into difference, lift, p-value, and a confidence interval at the chosen significance level. | must |
| REQ-003 | The system shall detect sample-ratio mismatch and invalidate an experiment whose arm allocation deviates from the expected split. | must |
| REQ-004 | The system shall return a verdict of "inconclusive" unless the pre-registered sample size is reached and no sample-ratio mismatch is present. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same inputs yield identical results on every run. |
| NFR-002 | Statistical consistency | The two-sided p-value and the (1−alpha) confidence interval agree — the CI excludes 0 exactly when p < alpha. |
| NFR-003 | Honest reporting | No "winner" is declared without adequate power and valid allocation; caveats are explicit. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a baseline rate and power, when the minimum detectable effect shrinks, then the required per-arm sample size increases. | REQ-001 |
| AC-002 | Given a clearly different treatment over large samples, then the test is significant with p < alpha and a CI excluding 0; given identical rates, then it is not significant. | REQ-002 |
| AC-003 | Given a balanced allocation, then the sample-ratio check passes; given a gross imbalance, then it flags a mismatch. | REQ-003 |
| AC-004 | Given a significant but underpowered result, then the verdict is "inconclusive"; given a well-powered, valid, significant result, then the verdict names the winning arm; a sample-ratio mismatch forces "inconclusive". | REQ-004, NFR-003 |
| AC-005 | Given any two-arm result, when analyzed, then the CI excludes 0 exactly when p < alpha. | NFR-002 |
| AC-006 | Given the same inputs, when analyzed twice, then the results are identical. | NFR-001 |

## Data & Dependencies

- Per-arm counts: subjects and conversions for control and treatment (from
  `sql-integration-agent` via the `0008` metrics layer where applicable).
- The pre-registered design: baseline rate, minimum detectable effect, significance
  level, power, and expected allocation.
- Standard: `instructions/model_validation.md` (validation discipline) and the
  causal caveats in `agents/machine_learning/causal_uplift/`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Peeking / early stopping inflates false positives. | Ship changes that do not work. | Verdict requires the pre-registered sample size before concluding (AC-004). |
| RISK-002 | Sample-ratio mismatch signals a broken experiment. | Biased, invalid readout. | SRM check invalidates the experiment (AC-003 / AC-004). |
| RISK-003 | p-value and CI disagree at the boundary. | Contradictory conclusions. | One shared standard error drives both (NFR-002 / AC-005). |
| RISK-004 | Underpowered test reported as "no difference". | False negatives; real effects missed. | Power is computed and surfaced; underpowered → "inconclusive", not "no difference". |

## Assumptions & Open Questions

- Assumption: a binary/conversion metric with independent subjects and a fixed-horizon
  (non-sequential) design for v1.
- Assumption: equal allocation by default; the expected share is configurable.
- Open question: add continuous-metric (t-test) and sequential designs next
  (tracked, not silently deferred).

## Exceptions

None.
