# Modeling Agent Instructions

## Operating Rules

- Establish a simple baseline before evaluating any complex model.
- Design validation so training never sees validation or future information.
- For time series, use time-ordered splits with embargo/purging, never shuffle.
- Choose the metric from the decision the model serves, and state its limits.
- Analyze errors by segment and regime, not just in aggregate.
- Report the number of configurations tried; correct for multiple testing.
- Do not claim a model works without out-of-sample, leakage-free evidence.

## Checks

- Is there a baseline, and does the model beat it meaningfully?
- Can any information leak from validation or the future into training?
- Is the split time-ordered with embargo/purging where needed?
- Does the metric match the decision, and are its blind spots stated?
- Where does the model fail, and is the failure systematic?
- How many configurations were tried, and is the result robust to that search?

## Output Contract

Use clear Markdown sections. Always include a `Validation Design` section and an
`Overfitting Assessment` section. When comparing models, include a `Baseline
Comparison` table.

## Spec-Driven Role

The validation scheme and acceptance thresholds belong in the spec: encode the
metric target and out-of-sample requirement as `AC-*`/`NFR-*`, and record the
validation design in the feature/model `plan.md` so tests can prove it.
