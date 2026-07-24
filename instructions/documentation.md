# Documentation Instructions

## Purpose

Use this instruction set when creating or reviewing durable quant workflow artifacts: research memos, dataset cards, model cards, experiment summaries, backtest reports, risk reviews, and handoff memos.

## Required Inputs

- Artifact purpose and audience.
- Source materials, code paths, data references, and experiment identifiers.
- Known assumptions, decisions, results, and limitations.
- Owner and next reviewer.

## Expected Output

- Clear artifact with enough context for review or continuation.
- Explicit assumptions and limitations.
- Source references.
- Validation status.
- Open questions and next actions.

## Standards

- Write for the next qualified person who must continue the work.
- Link claims to evidence, code, data, or owner-provided context.
- Separate facts, interpretations, decisions, and recommendations.
- Include dates, versions, windows, and identifiers where they affect reproducibility.
- Make blockers and risks visible.
- Avoid hiding uncertainty behind polished prose.

## Checks

- Can a reviewer tell what changed, why, and what evidence supports it?
- Are assumptions and limitations explicit?
- Are data sources and code paths referenced?
- Are validation steps and results summarized?
- Are open questions and next actions clear?
- Is the artifact scoped to the intended audience?

## Common Failure Modes

- Narrative summaries without enough reproducibility detail.
- Missing data windows, code versions, or configuration references.
- Treating open questions as resolved.
- Omitting negative results.
- Failing to identify who owns the next action.

## Spec-Driven Alignment

Documentation is where traceability becomes visible. Reference the spec IDs a
document supports (`REQ-*`/`AC-*`/`RISK-*`) so claims trace to requirements
(constitution P2); capture reproducibility detail via `templates/docs/run_card.md`
(P4); and report status honestly — unmet criteria are not "done" and open
questions are not resolved (P10). Every reusable artifact template lives under
`templates/`; keep generated documents consistent with the spec they describe.
