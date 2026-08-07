# Plan: Evening Quant Content Workflow

- **Spec:** 0003-evening-quant-content-workflow (`spec.md`)
- **Status:** Draft
- **Author:** QuantSmith
- **Last updated:** 2026-08-07

> HOW. Requires the approved `spec.md`.

## Approach

Build the workflow as a reviewable draft-pack generator. The content agents form a
pipeline from config and context through idea generation, packaging, visual/meme
specification, claim review, memory updates, and delivery. Provider-specific data
access and delivery remain behind adapters so the workflow can run deterministically
with supplied context or live sources without changing agent behavior.

The first implementation is non-posting by construction. It emits Markdown/YAML
artifacts and can hand them to a delivery adapter, but social-platform writes are
out of scope.

## Architecture & Components

```text
config + memory
  -> content_orchestrator
  -> market_context_researcher
  -> quant_angle_generator
  -> x_post_packager
  -> visual_spec_agent
  -> meme_culture_agent
  -> claim_review_agent
  -> content_memory_agent
  -> artifact/delivery adapter
```

| Component | Responsibility |
| --- | --- |
| `configs/evening_quant_content.yml` | Run schedule, platform limits, topic weights, deliverable counts, sources, review, memory, and delivery. |
| `agents/content/*` | Agent contracts for each content workflow stage. |
| `templates/docs/evening_quant_draft_pack.md` | Human-readable draft-pack shape. |
| `examples/evening_quant_content/sample_draft_pack.yml` | Deterministic fixture for validation and documentation. |
| `memory/evening_quant_content/` | Metadata-only memory for style, repetition, prior outputs, and rejected framing. |
| `hooks/stages/content-draft-pack-check.sh` | Advisory structural check for the config, template, and sample fixture. |

## Interfaces & Data Contracts

The workflow input is a config plus optional user-supplied context. Live source
pulls use the data-access API adapters and must emit source notes. The output is a
versioned draft pack with:

- `run_id`, `generated_at`, `config_ref`, `memory_version`, and `status`;
- ranked ideas with scores, classifications, risks, and next steps;
- finished posts and thread drafts validated against platform constraints;
- meme concepts and visual specs with factual risk labels;
- source notes, review findings, deferred ideas, and memory updates.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Facts require source notes; platform constraints live in config and are validated. |
| P5 Reversibility | yes | Output is a draft artifact; posting is manual and out of scope. |
| P6 Observability | yes | Draft packs include run IDs, source notes, review findings, and memory updates. |
| P9 Security & data | yes | Secrets, MNPI, client details, and private desk context are forbidden. |
| P10 Honest reporting | yes | Facts, inferences, jokes, and speculation are explicitly separated. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | Config template and content orchestrator | T-001, T-003 |
| REQ-002 | Ranked idea schema and angle generator | T-002, T-004 |
| REQ-003 | Draft-pack template and sample fixture | T-005, T-006 |
| REQ-004 | Claim review agent and source-note contract | T-007 |
| REQ-005 | Classification schema in every draft item | T-004, T-007 |
| REQ-006 | Platform constraints in config and hook | T-001, T-008 |
| REQ-007 | Workflow memory scaffold and content memory agent | T-009 |
| REQ-008 | Delivery contract through adapters | T-010 |
| NFR-001 | Confidential-info checks and memory rules | T-007, T-009 |
| NFR-002 | Run metadata and memory version | T-005, T-006 |
| NFR-003 | Review status on postable items | T-007, T-008 |
| NFR-004 | Config-driven platform/content settings | T-001 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Publishing | Manual approval only | Automatic X/Twitter posting | Avoids identity, compliance, and platform-permission risk. |
| Sources | Adapter-backed or user-supplied | Hard-coded source scraping | Keeps source policy configurable and testable. |
| Agents | Pipeline-shaped content group | One monolithic content agent | Makes review, memory, visuals, and claims independently inspectable. |
| Validation | Advisory shell hook first | Full runtime validator first | Gives immediate guardrails without overbuilding runtime code. |

## Validation Strategy

- AC-001/006: `content-draft-pack-check` verifies required config sections and
  platform constraints.
- AC-002/003: sample fixture includes ranked ideas and all deliverable groups.
- AC-004/005: claim review requires source note references for facts and separate
  labels for inferences/jokes/speculation.
- AC-007: memory scaffold records prior themes, style preferences, rejected
  framing, and visual playbook.
- AC-008: delivery config uses draft artifact delivery and `require_manual_approval`.

## Rollout, Observability & Rollback

Ship as documentation, contracts, config, sample artifacts, and an advisory hook.
Runtime execution can be added later behind the same contracts. Rollback is simply
reverting the additive files; no external state or posting side effects are created.

## Open Questions

- Should the first runnable implementation be a pure Markdown/YAML generator or a
  small Python package entrypoint?
- Should scoring weights be explicit in config or derived from memory?
- Which delivery adapter should be the default after local-file output?