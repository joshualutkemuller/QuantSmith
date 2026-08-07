# Content Agents

The Content group turns market context and quant ideas into reviewed, non-posting
draft packs. It is a pipeline-shaped group for scheduled content research, not a
social-platform automation surface.

## Group Workflow

```text
content_orchestrator -> market_context_researcher -> quant_angle_generator
  -> x_post_packager -> visual_spec_agent -> meme_culture_agent
  -> claim_review_agent -> content_memory_agent -> delivery adapter
```

## Agents

| Agent | Handles |
| --- | --- |
| `content_orchestrator/` | Run config, topic budget, stage routing, ranking, assembly, and delivery handoff. |
| `market_context_researcher/` | Current market context, source notes, and fact/reaction/speculation separation. |
| `quant_angle_generator/` | Contrarian, quantitative angles with mechanisms, second-order effects, and risks. |
| `x_post_packager/` | Short posts, quote-tweet replies, and thread drafts under platform constraints. |
| `visual_spec_agent/` | Chart, diagram, screenshot, and meme-image specs with data and caveat requirements. |
| `meme_culture_agent/` | Market-aware meme concepts that do not smuggle unsupported claims. |
| `claim_review_agent/` | Source support, claim labels, compliance language, and confidential-info review. |
| `content_memory_agent/` | Prior themes, hooks, rejected framing, visual playbook, and style memory updates. |

## Inputs

- `evening_quant_content_twitter/configs/evening_quant_content.yml`.
- Optional user-supplied links, screenshots, charts, or current-events context.
- Source notes from web, API, market data, or user-provided material.
- Prior workflow memory from `evening_quant_content_twitter/memory/evening_quant_content/`.

## Outputs

- Ranked ideas.
- Finished posts and thread drafts.
- Meme concepts.
- Visual specs.
- Source notes and review findings.
- Deferred/rejected ideas.
- Memory updates.

## Rules

- Draft packs require manual approval.
- Delivery adapters can send artifacts; they must not post to a social platform.
- Facts require source notes.
- Inferences, jokes, and speculation are labeled separately.
- No confidential desk context, client details, MNPI, private positions, or
  credentials.