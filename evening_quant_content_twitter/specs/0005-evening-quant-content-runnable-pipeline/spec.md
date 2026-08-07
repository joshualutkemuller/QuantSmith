# Spec: Evening Quant Content Runnable Pipeline

- **ID:** 0005-evening-quant-content-runnable-pipeline
- **Status:** Implemented
- **Author:** QuantSmith
- **Approver:** TBD
- **Last updated:** 2026-08-07

> WHAT and WHY only. Implementation lives in `plan.md`.

## Problem & Context

The `0003` evening quant content workflow defined a strong draft-pack contract, but
it stopped at documentation, agent contracts, a config, a fixture, and an advisory
gate. The missing slice is an executable pipeline that a human or scheduler can run
without adding posting permissions or live-source dependencies.

This spec turns the evening X/Twitter content workflow into a runnable, local,
non-posting draft-pack generator. It is deliberately deterministic so the workflow
can be validated before live research, LLM generation, or platform delivery is
introduced.

## Goals

- Provide a command-line executor that loads the evening content config.
- Accept optional user-supplied context notes in Markdown/plain text or JSON.
- Prime from metadata-only workflow memory.
- Emit both YAML and Markdown draft-pack artifacts.
- Validate ranked ideas, output sections, platform limits, source-note references,
  and manual approval controls before writing output.
- Provide a cron scheduler deployment profile for local runs.
- Keep X/Twitter posting out of scope.

## Non-Goals

- Live web/news retrieval.
- LLM orchestration or model-provider calls.
- Automatic X/Twitter posting.
- Email, Slack, Teams, or other external delivery writes.
- Storing credentials, MNPI, client/counterparty details, or private desk context.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The runtime shall expose a CLI executable from the repo root with config, optional context, output directory, and deterministic timestamp arguments. | must |
| REQ-002 | The runtime shall load `evening_quant_content_twitter/configs/evening_quant_content.yml` and preserve configured deliverable counts, platform limits, schedule metadata, memory path, and manual approval controls. | must |
| REQ-003 | The runtime shall accept optional Markdown/plain-text or JSON context notes and turn them into source notes. | must |
| REQ-004 | The runtime shall emit 10-15 ranked ideas plus finished posts, thread drafts, meme concepts, visual specs, source notes, review findings, deferred ideas, and memory updates. | must |
| REQ-005 | The runtime shall validate post character counts and source-note references before delivery. | must |
| REQ-006 | The runtime shall block or fail if automatic posting is enabled or manual approval is disabled. | must |
| REQ-007 | The runtime shall write local YAML and Markdown artifacts without mutating external platforms. | must |
| REQ-008 | The scheduler profile shall document a cron trigger that runs the same CLI command at 10:30 PM Eastern-equivalent local time. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Determinism | fixed timestamp and context inputs reproduce the same draft-pack content |
| NFR-002 | Portability | runtime uses Python standard library only |
| NFR-003 | Safety | no social-platform writes, secrets, MNPI, client details, or private desk data |
| NFR-004 | Reviewability | every generated artifact is local and human-readable |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given the default config and sample context, when the CLI runs, then it writes `draft_pack.yml` and `draft_pack.md`. | REQ-001, REQ-007 |
| AC-002 | Given configured counts, when output is produced, then ranked ideas are between 10 and 15 and configured deliverable groups are present. | REQ-002, REQ-004 |
| AC-003 | Given context notes, when source notes are built, then factual draft references use source-note IDs. | REQ-003, REQ-005 |
| AC-004 | Given a generated post, when validation runs, then character counts are at or below the configured platform limit. | REQ-005 |
| AC-005 | Given `auto_post_enabled: true` or `require_manual_approval: false`, when validation runs, then the runtime exits non-zero. | REQ-006 |
| AC-006 | Given the scheduler folder, when a human reviews deployment, then a cron profile and example entry show the exact local run command. | REQ-008 |

## Data & Dependencies

- Config: `evening_quant_content_twitter/configs/evening_quant_content.yml`.
- Runtime: `evening_quant_content_twitter/runtime/evening_quant_pipeline.py`.
- Scheduler: `evening_quant_content_twitter/scheduler/`.
- Sample context: `evening_quant_content_twitter/examples/evening_quant_content/context_sample.md`.
- Output template: `evening_quant_content_twitter/templates/docs/evening_quant_draft_pack.md`.
- Memory scaffold: `evening_quant_content_twitter/memory/evening_quant_content/`.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Users mistake deterministic scaffold output for fully sourced current-market commentary. | Credibility risk. | Runtime labels source refresh and human approval requirements. |
| RISK-002 | A future scheduler profile mutates a social account without approval. | Platform/reputation risk. | This spec limits scheduler output to local artifacts and keeps autopost disabled. |
| RISK-003 | YAML parsing is too narrow for arbitrary config rewrites. | Runtime drift risk. | Parser is intentionally scoped to the checked-in config; future richer config can add a declared dependency. |

## Assumptions & Open Questions

- Assumption: the first runnable pipeline should be deterministic and local.
- Assumption: live source retrieval and LLM generation should arrive in later
  specs behind explicit adapters.
- Open question: should the next runtime spec add a provider-backed research stage
  or a local LLM drafting stage first?

## Exceptions

None.
