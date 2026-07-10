# Coding & Implementation Instructions

## Operating Rules

- Match the existing code's naming, structure, and comment density.
- Keep changes scoped to the design; flag scope creep instead of absorbing it.
- Make outputs reproducible: pin inputs, seed randomness, avoid hidden state.
- In data and feature code, guard against look-ahead and leakage explicitly.
- Prefer small, composable functions over large notebook cells for shared logic.
- Update configs, docstrings, and inline docs alongside the code.
- State how the change was checked; never assert it works untested.

## Checks

- Does the implementation match the approved design, or is the deviation noted?
- Does it follow the repository's conventions and style?
- Are inputs, seeds, and configs explicit enough to reproduce the result?
- Is there any look-ahead, leakage, or non-determinism in the data path?
- Are secrets, credentials, and private data paths kept out of the code?
- Is it clear what still needs tests?

## Output Contract

Use clear Markdown sections around any code. Always include a `Reproducibility
Notes` section and a `Needs Tests` section. When behavior changed, include a
`Self-Review` section listing the top risks.
