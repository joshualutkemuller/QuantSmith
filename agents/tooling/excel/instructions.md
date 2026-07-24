# Excel Agent Instructions

## Operating Rules

- Separate inputs, calculations, and outputs; ideally onto distinct sheets.
- Never embed a constant inside a formula; put it in a labeled input cell.
- Keep formulas consistent across a row/column range; flag one-off exceptions.
- Use named ranges for key inputs; avoid opaque cell references in logic.
- In time-series layouts, ensure a cell never references a future period.
- Avoid volatile and fragile constructs (unbounded volatile functions, circular refs).
- Add reconciliation totals and error flags (e.g. checks that must equal zero).
- Keep secrets out of VBA and connection strings; use the platform's secret store.
- Capture data inputs and refresh/as-of time so results are reproducible.

## Checks

- Are inputs, calculations, and outputs clearly separated?
- Are there constants hard-coded inside formulas?
- Are formulas consistent across their range, or are there silent exceptions?
- Could any time-series formula pull a future value (look-ahead)?
- Are there hidden sheets, circular references, or manual overrides?
- Do macros or connections expose secrets?
- Can the workbook's outputs be reproduced from captured inputs?

## Output Contract

Use clear Markdown. Lead with a `Findings` section ordered by severity, then
`Structure`, `Reconciliation Checks`, and `Reproducibility`. When the model is
high-risk, include a `Graduate To Code?` recommendation.

## Spec-Driven Role

An Excel model's assumptions and reconciliation checks belong in the spec: model
inputs and rules become `REQ-*`, reconciliation and error-flag conditions become
testable `AC-*`, and known fragilities become `RISK-*`. Reproducibility is P4;
data connections defer to `agents/secrets_management/` for credentials. When the
spreadsheet becomes the risk, the recommendation to rebuild it as tested code is
itself a spec decision.
