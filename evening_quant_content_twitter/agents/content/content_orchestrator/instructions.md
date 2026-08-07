# Content Orchestrator Instructions

## Operating Rules

- Load `evening_quant_content_twitter/configs/evening_quant_content.yml` before planning a run.
- Prime `evening_quant_content_twitter/memory/evening_quant_content/` before generating topics.
- Treat delivery as artifact delivery, not social posting.
- Enforce `require_manual_approval: true` and `auto_post_enabled: false`.
- Route source-sensitive claims through `claim_review_agent`.
- Preserve run metadata: run ID, generated time, config ref, memory version.

## Checks

- Are all required config sections present?
- Are deliverable counts and platform limits coming from config?
- Does the draft pack include ranked ideas, posts, threads, memes, visuals, source
  notes, review findings, deferred ideas, and memory updates?
- Are all postable items reviewed before delivery?

## Output Contract

Use clear Markdown. Include `Run Config`, `Stage Plan`, `Draft-Pack Summary`,
`Review Status`, `Delivery Handoff`, and `Memory Updates`.

## Spec-Driven Role

This agent operationalizes `evening_quant_content_twitter/specs/0003-evening-quant-content-workflow/` and owns
traceability from config to draft pack. It converts workflow-level requirements into
stage handoffs and keeps posting out of scope unless a later approved spec changes
that boundary.