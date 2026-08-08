# Experimentation Instructions

## Operating Rules

- Size the experiment before it runs: choose the minimum detectable effect,
  significance level, and power, and compute the required per-arm sample size.
- Do not conclude before the pre-registered sample size is reached; no peeking or
  early stopping without a sequential correction.
- Check sample-ratio mismatch first; a broken allocation invalidates the readout.
- Report a confidence interval computed from the same standard error as the p-value,
  so they always agree.
- Treat an underpowered test as "inconclusive", not "no difference".
- Declare a winner only when the experiment is powered, valid, and significant.
- State the causal caveats; hand observational or heterogeneous-effect questions to
  `machine_learning/causal_uplift`.

## Checks

- Is there a pre-registered design (MDE, alpha, power, expected split)?
- Has the achieved per-arm sample reached the required size?
- Does the sample-ratio check pass?
- Does the confidence interval exclude 0 exactly when p < alpha?
- Is the verdict gated on power and allocation validity?
- Are the caveats explicit in the readout?

## Output Contract

Use clear Markdown. Report the design and required sample size, then the readout
(difference, lift, p-value, CI), then a `Validity` section (SRM, power), then a
`Verdict` with caveats. Name the runtime symbols (`required_sample_size`,
`analyze_experiment`) when handing off to code.

## Spec-Driven Role

The experiment design becomes `REQ-*`; power/sample-size, SRM validity, p-value/CI
consistency, and the power-gated verdict become testable `AC-*`; peeking,
sample-ratio mismatch, and underpowered conclusions become `RISK-*`. The runtime is
`src/quantsmith/pipelines/experimentation.py`; the worked spec is
`specs/0009-experimentation/`; validation discipline is in
`instructions/model_validation.md`. Hands off to `quality-guard-agent` and
`reporting-agent`.
