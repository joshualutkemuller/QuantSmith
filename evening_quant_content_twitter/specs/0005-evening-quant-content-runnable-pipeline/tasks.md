# Tasks: Evening Quant Content Runnable Pipeline

- **Spec:** 0005-evening-quant-content-runnable-pipeline (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

## Definition of Done

- Runtime can be invoked from the repository root.
- Runtime writes local YAML and Markdown draft-pack artifacts.
- Scheduler profile documents the same runnable command.
- No automatic posting capability is introduced.
- Validation checks pass deterministically.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Add standard-library CLI executor. | REQ-001, REQ-002, NFR-001, NFR-002 | done | `runtime/evening_quant_pipeline.py`. |
| T-002 | Load config and optional context notes. | REQ-002, REQ-003 | done | Supports checked-in YAML shape plus Markdown/plain text or JSON context. |
| T-003 | Build ranked ideas and deliverable groups. | REQ-003, REQ-004 | done | Emits ideas, posts, threads, memes, visuals, source notes, review findings, deferred ideas, memory updates. |
| T-004 | Validate platform and safety controls. | REQ-005, REQ-006, NFR-003 | done | Checks character limits, source-note references, manual approval, and disabled autopost. |
| T-005 | Write local YAML and Markdown artifacts. | REQ-007, NFR-004 | done | Outputs `draft_pack.yml` and `draft_pack.md`. |
| T-006 | Add cron scheduler deployment profile. | REQ-008, NFR-003 | done | `scheduler/cron.md` and crontab example. |
| T-007 | Extend content gate with runtime smoke test. | REQ-005, REQ-007, REQ-008, NFR-001 | done | Uses sample context and `/tmp` output. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | CLI smoke test in `content-draft-pack-check` | done |
| AC-002 | Runtime validation and fixture output shape | done |
| AC-003 | Source-note IDs in generated post classifications | done |
| AC-004 | Runtime character-count validator | done |
| AC-005 | Runtime manual-approval/autopost validator | done |
| AC-006 | Scheduler profile file presence and command text in content gate | done |

## Follow-ups

- Add live source adapters as a separate spec.
- Add LLM-backed generation as a separate spec.
- Add optional delivery adapters after artifact quality is stable.
