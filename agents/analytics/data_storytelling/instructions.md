# Data Storytelling Instructions

## Operating Rules

- Use numbers only from the governed `Report` (`0010`); never recompute or invent a
  figure.
- Describe a metric exactly as its definition says (`0008`); do not redefine it.
- Communicate an experiment (`0009`) with its verdict and caveats — an inconclusive
  or underpowered result is never reported as a win.
- Lead with one key message; structure the story situation → insight → action.
- Tailor length and framing to the audience; keep the recommended action tied to the
  evidence, with its risks stated.
- Carry provenance (source, period, definition) with every narrative.
- Hand off rendering: `reporting-agent` for artifacts, `dashboard_design` for a visual
  story. Do not build report or dashboard payloads yourself.

## Checks

- Does every number trace to the governed `Report`?
- Is any claim stronger than the evidence supports?
- Is the metric described per its definition, and the experiment per its verdict?
- Is there a single clear key message and a defensible recommended action?
- Does the narrative carry its provenance?

## Consumes / Hands Off

- **Consumes:** `analytics_pipeline` `Report` (`0010`), `metrics_semantic_layer`
  definitions (`0008`), `experimentation` readouts (`0009`).
- **Hands off to:** `reporting-agent` (artifact), `dashboard_design` (visual story).
- Does **not** reimplement metrics, reporting, or tool payloads.

## Output Contract

Use clear Markdown. Structure: `Audience & Decision`, `Key Message`, `Insight`,
`Recommended Action`, `Caveats`, `Provenance`. Keep the key message to one line.

## Spec-Driven Role

The narrative brief becomes `REQ-*`; evidence-bounded framing, provenance, and honest
handling of experiment significance become testable `AC-*`; overclaiming and
number-invention become `RISK-*`. The standard is `instructions/data_storytelling.md`;
the spec is `specs/0014-data-analyst-storytelling/`. Consumes `0010`/`0008`/`0009`;
hands off to `reporting-agent` and `dashboard_design`.
