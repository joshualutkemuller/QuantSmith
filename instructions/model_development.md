# Model Development Instructions

## Purpose

Use this instruction set when building a quant model or signal — turning an approved
design into a reproducible, leakage-free, validatable implementation. It is the
standardized way to build quant models in this SDK, and it backs the `modeling`,
`feature_engineering`, and `implementation` agents and the `trading_strategies/` and
`formulaic_alphas/` groups. It is the coding/model-development counterpart to
`instructions/model_validation.md` (how to validate) and
`instructions/spec_driven_development.md` (the build process).

## Required Inputs

- The approved `spec.md` and `plan.md` (with `REQ`/`NFR`/`AC`).
- Data sources and their point-in-time constraints.
- Target, features, and the validation design.
- Repository conventions and the runtime environment.

## Expected Output

- Model/signal code that matches the design and repo conventions.
- A deterministic, config-driven pipeline.
- Reproducibility notes and a run card.
- A clean handoff to validation and backtesting.

## Standards

- **Build from the spec.** Implement the design; record any deviation in `plan.md`.
- **Reproducible by construction (P4).** Pin data snapshots, seed randomness, avoid
  hidden or global state, and prefer config over hardcoded constants.
- **Leakage-safe.** Use point-in-time inputs; fit transforms/scalers on training
  data only; never let the target or future data enter features. See
  `instructions/point_in_time.md`.
- **Separate the phases.** Keep exploration, model selection, validation, and final
  reporting distinct; do not select and validate on the same data.
- **Baseline first.** Establish a simple baseline before adding complexity.
- **Deterministic pipeline.** The same inputs produce the same outputs; capture a
  run card (`templates/docs/run_card.md`) so the result can be reproduced.
- **Reviewable code.** Match repo conventions; keep changes small and clear; promote
  shared notebook logic into importable, tested modules.
- **Version everything.** Record data snapshot, config, seed, and environment.
- **No secrets.** Keep credentials and private data out of code and notebook outputs.

## Checks

- Does the implementation match the approved design (or is the deviation recorded)?
- Are inputs pinned, randomness seeded, and outputs deterministic?
- Is the pipeline free of look-ahead and train/validation leakage?
- Are exploration, selection, validation, and reporting separated?
- Is there a baseline the model must beat?
- Is a run card / reproduction path captured?
- Are secrets and private data kept out of code and outputs?

## Common Failure Modes

- Notebook code with hidden state passed off as a reproducible pipeline.
- Global preprocessing (scaling/imputation) before the train/validation split.
- Unpinned data or dependencies that make the result irreproducible.
- Selecting and validating a model on the same data.
- Skipping a baseline, so "good" performance has no reference.
- Hardcoded credentials, data paths, or magic constants.

## Spec-Driven Alignment

This standard backs the Implement step. Its coding and reproducibility rules make
constitution P4 concrete; the run card captures reproduction; leakage-safety defers
to `instructions/point_in_time.md` and the `leakage` gate; validation hands off to
`instructions/model_validation.md`, the `testing_validation` agent, and the
`backtest` gate. The model implementation traces to the spec's `REQ-*`/`AC-*`, and
reproducibility is checked by the `repro` gate.
