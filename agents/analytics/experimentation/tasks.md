# Experimentation Tasks

## Size An Experiment

Input: a baseline rate, a minimum detectable effect, a significance level, and power.

Output: the required per-arm sample size and the pre-registered design.

## Read Out A Result

Input: per-arm subjects and conversions for control and treatment.

Output: difference, lift, p-value, and a confidence interval, with a significance
decision at the chosen alpha.

## Validate An Experiment

Input: per-arm sample sizes and the design.

Output: a validity assessment — sample-ratio mismatch and achieved power — and
whether the experiment may be concluded.

## Decide A Winner

Input: a validated, powered result.

Output: a verdict (`treatment` / `control` / `no_difference` / `inconclusive`) with
explicit caveats and the reasoning.
