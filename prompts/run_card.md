# Prompt: Run Card (record a reproducible run)

Produce a run card so an experiment or job can be reproduced.

## Inputs

- What was run (hypothesis, model, or job).
- Commit SHA and whether the tree was clean.
- Data snapshot identifier/hash, range, and frequency.
- Config/parameters and random seeds.
- Environment lockfile and runtime version.
- Result metrics and output artifact location.

## Instructions

Fill `templates/docs/run_card.md`. Capture only the parameters that affect the
result. State every source of non-determinism. Provide the exact command(s) to
reproduce. If the working tree was dirty at run time, say so and why — an
unreproducible run is not a candidate result (constitution P4).

## Output

A completed run card, plus a note on any reproducibility gaps that must be closed
before the result is treated as a candidate.
