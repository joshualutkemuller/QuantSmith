# Evening Quant Content Workflow Handoff

## Status

- **Status:** in-progress
- **Priority:** P1
- **Spec path:** `specs/0003-evening-quant-content-workflow/`
- **Primary workflow map:** `docs/workflows.md`
- **Related backlog:** `docs/handoffs/future_features.md`

## Problem

A quant content workflow should turn market context, current events, data-backed
angles, visual concepts, and meme ideas into a nightly draft pack that is useful
without becoming an autoposter. The current SDK has the right building blocks
for research, data ingestion, reporting, alerts, monitoring, memory, and workflow
orchestration, but it needs a configurable content workflow that composes those
pieces into an evening publishing pipeline.

The target user is a quant or Head of Quantitative Research who wants 10-15
high-signal X/Twitter post ideas, longer-form thread drafts, visual concepts, and
meme/pop-culture angles every evening at 10:30 PM Eastern.

## Guiding Principle

Build this as a **content research pipeline**, not a posting bot.

The core product is a ranked nightly draft pack. Actual posting should remain a
manual approval step unless a future spec adds explicit approval gates, identity
controls, and platform write permissions.

## Goals

- Generate 10-15 content ideas per run across quant research, markets, macro,
  securities finance, AI infrastructure, volatility, microstructure, financing,
  collateral, liquidity, and model risk.
- Produce a smaller set of finished draft posts and longer thread outlines.
- Include meme concepts and pop-culture framing where it strengthens the idea.
- Produce visual specs for charts, screenshots, diagrams, or meme images.
- Separate sourced facts, model/data inferences, opinion, jokes, and speculative
  takes.
- Support free-account X/Twitter constraints through configuration rather than
  hard-coded platform assumptions.
- Make topic weights, tone, schedule, channels, deliverables, and review strictness
  configurable.
- Use memory to avoid repeating the same hooks, themes, formats, and jokes.

## Non-Goals

- Do not automatically post to X/Twitter in the first version.
- Do not optimize for engagement at the expense of factual discipline.
- Do not embed proprietary desk data, confidential client information, MNPI, or
  non-public trade context.
- Do not create separate agents for each delivery channel. Email, Slack, Teams,
  webhooks, and ticketing systems should be adapters behind a shared delivery
  contract.
- Do not hard-code platform limits that can change. Keep account-mode and format
  constraints in config.

## Proposed Workflow

```text
schedule trigger
  -> content_orchestrator
  -> market_context_researcher
  -> quant_angle_generator
  -> x_post_packager
  -> visual_spec_agent
  -> meme_culture_agent
  -> claim_review_agent
  -> content_memory_agent
  -> delivery adapter
```

## Agent Responsibilities

| Agent | Responsibility | Reuses |
| --- | --- | --- |
| `agents/content/content_orchestrator/` | Own the run config, topic budget, ranking logic, deliverable assembly, and handoff to delivery adapters. | `workflow_orchestrator`, `reporting-agent` |
| `agents/content/market_context_researcher/` | Gather current market/news context and classify facts, reactions, and speculation. | `research_analyst`, `data_ingestion/*`, `knowledge/*` |
| `agents/content/quant_angle_generator/` | Convert context into contrarian, quantitative, research-grade angles with clear mechanisms and second-order implications. | `research_analyst`, `modeling`, `risk` |
| `agents/content/x_post_packager/` | Format concise posts, quote-tweet replies, hooks, and thread drafts under configurable platform constraints. | `reporting-agent` |
| `agents/content/visual_spec_agent/` | Define chart, meme, screenshot, or diagram concepts, including data needed, chart type, source notes, and caption direction. | `tooling/*`, `reporting-agent` |
| `agents/content/meme_culture_agent/` | Generate market-aware meme concepts without compromising factual claims or professional tone. | `reporting-agent` |
| `agents/content/claim_review_agent/` | Review factual claims, source support, uncertainty language, compliance hazards, and confidential-information risk. | `quality-guard-agent`, `risk`, `knowledge/*` |
| `agents/content/content_memory_agent/` | Track prior themes, formats, hooks, visual ideas, and rejected tropes to reduce repetition. | `memory/`, `knowledge/*` |

The content group should be a pipeline-shaped group with a co-located
`agents/content/README.md` mini-map once implementation begins.

## Config Contract

Initial config file:

`configs/evening_quant_content.yml`

```yaml
workflow_name: evening_quant_content

schedule:
  frequency: daily
  time: "22:30"
  timezone: America/New_York

platform:
  primary: x
  account_mode: free
  max_post_chars: 280
  max_thread_posts: 8
  require_manual_approval: true

content:
  ideas_per_run: 15
  finished_posts: 5
  thread_drafts: 3
  meme_concepts: 5
  visual_specs: 5
  tone:
    - quant-native
    - contrarian
    - market-aware
    - lightly funny
  avoid:
    - investment_advice
    - unsupported_performance_claims
    - confidential_desk_context
    - client_or_counterparty_details

topics:
  include:
    - AI infrastructure
    - equity concentration
    - macro liquidity
    - volatility
    - market microstructure
    - securities finance
    - collateral optimization
    - repo
    - quant research
    - model risk
  priority_bias:
    securities_finance: 1.4
    AI_infrastructure: 1.2
    macro_liquidity: 1.2
    market_microstructure: 1.1

sources:
  freshness_window_hours: 24
  allow_web_research: true
  allow_user_supplied_images: true
  require_source_notes_for_facts: true

review:
  fact_inference_joke_labels: true
  claim_review_required: true
  confidential_info_check: true
  compliance_language_check: true

delivery:
  draft_channel: email
  include:
    - ranked_ideas
    - finished_posts
    - thread_drafts
    - meme_concepts
    - visual_specs
    - source_notes
    - rejected_or_deferred_ideas
```

## Output Contract

Each run should emit a versioned draft pack:

```yaml
run_id: "2026-08-07-evening-quant-content"
generated_at: "2026-08-07T22:30:00-04:00"
config_ref: "configs/evening_quant_content.yml"
status: draft

ranked_ideas:
  - id: idea-001
    title: "AI capex as a duration trade"
    topic: AI infrastructure
    format: post
    score:
      novelty: 4
      timeliness: 5
      quant_depth: 4
      visual_potential: 5
      meme_potential: 3
    classification:
      facts: []
      inferences: []
      jokes: []
    risks:
      - unsupported_causal_claim
    next_step: draft_post

finished_posts: []
thread_drafts: []
meme_concepts: []
visual_specs: []
source_notes: []
review_findings: []
memory_updates: []
```

## Suggested Deliverable Format

Every evening delivery should include:

1. Top 10-15 ideas ranked by timeliness, quant depth, novelty, visual potential,
   meme potential, and claim risk.
2. Three to five finished posts under the configured character limit.
3. One to three longer thread drafts with per-post structure.
4. Three to five meme concepts with setup, caption, image direction, and risk.
5. Visual specs for the strongest ideas, including chart type, data needed,
   source candidates, and intended takeaway.
6. Source notes for factual claims.
7. A short "do not post yet" section for ideas that are promising but under-sourced
   or too close to investment advice.

## Review Standards

- **Facts:** Must have source notes or be removed.
- **Inferences:** Must use uncertainty language and avoid overclaiming causality.
- **Jokes/memes:** Must not carry factual claims unless separately sourced.
- **Markets:** Avoid individualized investment advice and performance promises.
- **Desk context:** Treat internal models, client details, inventory, financing
  levels, and counterparty information as restricted unless explicitly public.
- **Visuals:** Chart specs must state data source, grain, window, transformation,
  and caveats before rendering.

## Memory Design

Use persistent workflow memory to track:

- Repeated themes and hooks.
- Prior finished posts and thread formats.
- Visual concepts already used.
- Meme templates that became stale or overused.
- Personal style preferences.
- Topic weights that performed well or poorly.
- Rejected claims or risky framing to avoid resurfacing.

Suggested memory path:

```text
memory/evening_quant_content/
  README.md
  index.yaml
  themes.md
  style_preferences.md
  rejected_framing.md
  visual_playbook.md
```

## Implementation Phases

| Phase | Scope | Done When |
| --- | --- | --- |
| 1 | Add handoff, workflow-map entry, and backlog row. | **Done.** The workflow is discoverable and spec-ready. |
| 2 | Promote to `specs/0003-evening-quant-content-workflow/` and add the config template. | **Done.** `spec.md`, `plan.md`, `tasks.md`, and `configs/evening_quant_content.yml` define build scope and acceptance criteria. |
| 3 | Add `agents/content/*` contracts and group README. | **Done.** Each content agent has README, prompt, instructions, and tasks files. |
| 4 | Add sample run fixture and draft-pack template. | **Done.** A deterministic example run produces the output contract without live posting. |
| 5 | Add validation hooks. | **Done.** `content-draft-pack-check.sh` validates the config/template/sample scaffold. |
| 6 | Add scheduler and delivery adapter. | **Partial.** Config references scheduler and local artifact adapters; executable scheduler deployment is deferred. |

## Acceptance Criteria For The Future Spec

- A human can run the workflow manually with a config file and receive a draft pack.
- A scheduler can trigger the same workflow at 10:30 PM Eastern.
- Topic weights, deliverable counts, tone, account mode, and delivery channel are
  configurable.
- The system produces 10-15 ranked ideas per run.
- The system produces finished posts, thread drafts, meme concepts, visual specs,
  source notes, and review findings.
- Every factual claim is labeled and tied to a source note.
- Every inference is labeled separately from sourced fact.
- Every meme concept is reviewed for factual leakage, confidential context, and
  reputational risk.
- Free-account character constraints are validated from config.
- Delivery does not imply automatic posting.

## Open Questions

- Should the first implementation support only email delivery, or also local
  Markdown/JSON output?
- Should web/news research be required every run, or can the workflow accept
  user-supplied links and screenshots as the only input?
- Should scoring use fixed weights, configurable weights, or a learned preference
  file in memory?
- Should visual generation be separate from visual specification in the first
  version?
- What is the minimum acceptable source set for current-events claims?

## Build Recommendation

Start with a non-posting MVP:

```text
config -> research/context notes -> ranked content ideas -> draft pack -> review
```

Do not build platform posting until the draft-pack quality, claim-review gate, and
memory loop are reliable. The value is not that it can post unattended; the value
is that it can hand a quant a publishable, sourced, visually interesting content
queue every night.