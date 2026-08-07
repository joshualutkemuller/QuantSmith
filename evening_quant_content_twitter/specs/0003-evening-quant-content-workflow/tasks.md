# Tasks: Evening Quant Content Workflow

- **Spec:** 0003-evening-quant-content-workflow (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-07

## Definition of Done

- Matches the plan; deviations noted in `plan.md`.
- No automatic posting capability is introduced.
- No secrets, credentials, MNPI, PII, client details, or private desk context.
- Docs/configs/contracts update together.
- Validation checks pass deterministically.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Add `evening_quant_content_twitter/configs/evening_quant_content.yml`. | REQ-001, REQ-006, NFR-004 | done | Config-driven schedule, limits, topics, review, memory, delivery. |
| T-002 | Promote the handoff into this spec package. | REQ-001, REQ-002 | done | `spec.md`, `plan.md`, `tasks.md`. |
| T-003 | Add `evening_quant_content_twitter/agents/content/README.md` group workflow. | REQ-001, REQ-008 | done | Content group mini-map. |
| T-004 | Add content generation agent contracts. | REQ-002, REQ-005 | done | Orchestrator, context, angle, package, visual, meme, review, memory. |
| T-005 | Add draft-pack template. | REQ-003, NFR-002 | done | `evening_quant_content_twitter/templates/docs/evening_quant_draft_pack.md`. |
| T-006 | Add deterministic sample draft pack. | REQ-002, REQ-003, NFR-002 | done | No live data required. |
| T-007 | Add claim-review contract and review requirements. | REQ-004, REQ-005, NFR-001, NFR-003 | done | Facts require source notes or deferral. |
| T-008 | Add advisory content draft-pack check. | REQ-006, NFR-003 | done | Structural shell gate. |
| T-009 | Add workflow memory scaffold. | REQ-007, NFR-001, NFR-002 | done | Metadata-only memory files. |
| T-010 | Wire docs/catalog/backlog references. | REQ-008 | done | Workflow map and agent catalog updated. |
| T-011 | Add runnable workflow executor. | REQ-002, REQ-003, REQ-008 | done | `evening_quant_content_twitter/runtime/evening_quant_pipeline.py` emits local YAML/Markdown draft packs. |
| T-012 | Add scheduler deployment profile. | REQ-008 | done | `evening_quant_content_twitter/scheduler/` documents cron deployment. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `content-draft-pack-check` required config sections | done |
| AC-002 | sample draft pack ranked idea structure | done |
| AC-003 | sample draft pack deliverable groups | done |
| AC-004 | claim review source-note rule | done |
| AC-005 | classification labels in sample fixture | done |
| AC-006 | platform limits present in config | done |
| AC-007 | memory scaffold present | done |
| AC-008 | manual approval and artifact delivery present | done |

## Follow-ups

- Add source-provider profiles used by the nightly market context stage.
- Add optional artifact delivery beyond local files when a real delivery target is
  selected.
