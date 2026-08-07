# Content Orchestrator Tasks

## Plan Evening Run

Input: workflow config, memory records, optional user context.

Output: stage plan with topic budget, source policy, deliverable counts, review
rules, and delivery target.

## Assemble Draft Pack

Input: outputs from context, angle, post, visual, meme, review, and memory stages.

Output: versioned draft-pack manifest matching
`evening_quant_content_twitter/templates/docs/evening_quant_draft_pack.md`.

## Route Review Findings

Input: claim-review findings and draft-pack items.

Output: publish-ready, needs-refresh, deferred, and rejected queues.

## Handoff Delivery

Input: reviewed draft pack and delivery config.

Output: artifact delivery payload with manual approval status preserved.