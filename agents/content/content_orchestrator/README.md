# Content Orchestrator Agent

## Purpose

The Content Orchestrator Agent owns the evening content run: config loading, topic
budgeting, stage routing, ranking, draft-pack assembly, and delivery handoff.

## Use When

- A scheduled or manual evening content run needs to start.
- A handoff/config must be converted into a draft-pack workflow.
- A content run needs coordination across research, packaging, visuals, memes,
  claim review, memory, and delivery.

## Inputs

- `configs/evening_quant_content.yml`.
- Prior memory from `memory/evening_quant_content/`.
- Optional user-supplied context, links, screenshots, or data summaries.

## Outputs

- Stage plan and topic budget.
- Ranked idea assembly rules.
- Draft-pack manifest.
- Delivery handoff to artifact/delivery adapters.
- Memory update bundle.

## Required Review Themes

- Manual approval preserved.
- Config-driven limits and deliverable counts.
- Facts/inferences/jokes/speculation kept separate.
- No platform posting side effects.