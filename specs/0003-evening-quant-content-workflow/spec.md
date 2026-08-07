# Spec: Evening Quant Content Workflow

- **ID:** 0003-evening-quant-content-workflow
- **Status:** Draft
- **Author:** QuantSmith
- **Approver:** TBD
- **Last updated:** 2026-08-07

> WHAT and WHY only. Implementation lives in `plan.md`.

## Problem & Context

Quant content work often starts from the same nightly loop: scan markets and
current events, find a non-obvious quantitative angle, draft X/Twitter posts or
threads, design a visual, and reject claims that are under-sourced or too close to
advice. Without a workflow, the process is ad hoc and memoryless: good hooks are
forgotten, weak claims slip through, and the same themes repeat.

This spec defines a non-posting evening workflow that produces a ranked draft pack
for a quant-finance audience. The workflow is a content research pipeline, not an
autoposter.

## Goals

- Produce 10-15 ranked quant content ideas per run.
- Draft finished short posts, longer thread outlines, meme concepts, visual specs,
  source notes, review findings, and deferred ideas.
- Separate sourced facts, inferences, jokes, and speculation.
- Keep platform limits, schedule, topic weights, tone, and delivery configurable.
- Use workflow memory to reduce repeated hooks, formats, and stale jokes.
- Keep posting manual unless a future spec adds explicit approval and platform
  write controls.

## Non-Goals

- Automatically posting to X/Twitter or any social platform.
- Producing investment advice, performance promises, or unsupported causal claims.
- Using confidential desk data, client/counterparty details, MNPI, or private
  position/inventory context.
- Implementing live provider integrations in this spec.
- Optimizing purely for engagement without factual discipline.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The workflow shall load a versioned config defining schedule, platform constraints, deliverable counts, topic weights, source policy, review rules, memory policy, and delivery target. | must |
| REQ-002 | The workflow shall generate 10-15 ranked ideas with topic, format, score, claim classification, risk labels, and next step. | must |
| REQ-003 | The workflow shall produce finished posts, thread drafts, meme concepts, visual specs, source notes, review findings, and deferred ideas according to config. | must |
| REQ-004 | Every factual claim shall reference a source note or be rejected/deferred. | must |
| REQ-005 | Inferences, jokes, and speculative framing shall be labeled separately from sourced facts. | must |
| REQ-006 | The workflow shall validate configured character limits and thread limits before delivery. | must |
| REQ-007 | The workflow shall use `memory/evening_quant_content/` to track prior themes, hooks, formats, visual ideas, rejected framing, and style preferences. | should |
| REQ-008 | Delivery shall emit a draft pack through artifact/delivery adapters without implying automatic posting. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Confidentiality | zero secrets, MNPI, client details, credentials, or private desk data in configs, memory, or draft packs |
| NFR-002 | Reproducibility | every draft pack records run ID, config ref, generated time, source notes, and memory version |
| NFR-003 | Reviewability | every postable item has claim classification and review status before delivery |
| NFR-004 | Configurability | platform/account constraints and deliverable counts are not hard-coded in agent prompts |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given `configs/evening_quant_content.yml`, when the workflow is initialized, then schedule, platform, content, source, review, memory, and delivery sections are present. | REQ-001 |
| AC-002 | Given a run, when ranked ideas are emitted, then 10-15 ideas include score, classification, risks, and next step fields. | REQ-002 |
| AC-003 | Given configured deliverable counts, when the draft pack is assembled, then it includes posts, threads, memes, visual specs, source notes, review findings, and deferred ideas. | REQ-003 |
| AC-004 | Given any factual claim, when claim review runs, then it has a source note ID or is marked deferred/rejected. | REQ-004 |
| AC-005 | Given an inference, joke, or speculative claim, when review runs, then it is not labeled as a sourced fact. | REQ-005 |
| AC-006 | Given a free-account platform config, when finished posts are packaged, then post and thread limits are validated before delivery. | REQ-006 |
| AC-007 | Given prior memory records, when a new run is planned, then repeated hooks, stale meme formats, and rejected framing are surfaced as avoid rules. | REQ-007 |
| AC-008 | Given a completed draft pack, when delivery runs, then it is delivered as an artifact and never posted automatically. | REQ-008 |

## Data & Dependencies

- `configs/evening_quant_content.yml` defines run behavior.
- `agents/content/*` define the workflow roles.
- `templates/docs/evening_quant_draft_pack.md` defines the human-readable
  delivery shape.
- `examples/evening_quant_content/sample_draft_pack.yml` gives a deterministic
  no-live-data fixture.
- `memory/evening_quant_content/` stores metadata-only style and repetition memory.
- Data access uses `adapters/data_access/api.md` and provider profiles when live
  sources are enabled.
- Delivery uses artifact and alert delivery adapters; platform posting is out of
  scope.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Under-sourced current-events claims are packaged as facts. | Credibility/compliance risk. | Claim review requires source notes or deferral. |
| RISK-002 | Content drifts into investment advice. | Regulatory/reputational risk. | Review labels advice-like language and moves it to deferred ideas. |
| RISK-003 | Private desk or client context leaks into content. | Confidentiality breach. | Confidential-info check and memory secret/PII rules. |
| RISK-004 | Repetitive hooks degrade quality. | Audience fatigue. | Memory tracks prior themes, hooks, memes, and rejected framing. |
| RISK-005 | Platform constraints change. | Drafts become unusable. | Limits live in config, not prompts. |

## Assumptions & Open Questions

- Assumption: first delivery targets local Markdown/YAML and optional email draft
  handoff, not platform posting.
- Assumption: live current-events research may be disabled for deterministic runs.
- Open question: should scoring weights remain fixed or be adjusted from memory?
- Open question: which sources are mandatory for current-events market claims?

## Exceptions

None.