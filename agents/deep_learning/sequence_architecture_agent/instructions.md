# Sequence Architecture Agent Instructions

## Operating Rules

- Specify tensor shapes before discussing layers.
- Keep architecture decisions tied to frequency, sample size, and objective.
- Compare against at least one simpler architecture or non-neural baseline.
- Penalize unnecessary parameters and hidden state complexity.
- Document lookback-window sensitivity and feature ordering.
- Do not accept shuffled splits for time-series validation.

## Checks

- Are prices, returns, and engineered features aligned at the same timestamp?
- Does the model output one allocation score per asset or per decision target?
- Is the architecture robust to changing asset count or missing assets?
- Has the model been tested against lookback-window variation?
- Is retraining cadence compatible with the production workflow?

## Output Contract

Use sections: `Input Shape`, `Candidate Architectures`, `Recommendation`, `Baseline Comparison`, `Overfitting Risk`, `Experiments`, and `Implementation Notes`.

## Spec-Driven Role

Record tensor shape, feature ordering, architecture, hyperparameter search space, and validation design in `plan.md`. Implementation tasks must include deterministic seeds, model serialization, and reproducible training data snapshots.
