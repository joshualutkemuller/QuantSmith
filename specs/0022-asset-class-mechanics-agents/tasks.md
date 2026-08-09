# Tasks: Asset Class Mechanics Agent Expansion

- **Spec:** 0022-asset-class-mechanics-agents (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-09

## Definition of Done (applies to every task)

- Agent contracts follow the four-file convention with a `Spec-Driven Role`
  section in each `instructions.md`.
- Each agent states its mechanics-only scope and names its downstream handoff.
- Docs and catalogs are updated alongside the new public agents.
- No secrets, credentials, private data, or fabricated live-data capability
  claims are introduced.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Add `agents/asset_classes/` group and five specialist agents. | REQ-001, REQ-002, NFR-001, NFR-003 | done | `equities/`, `fixed_income_rates/`, `fx/`, `commodities/`, `digital_assets/`, plus group `README.md`. |
| T-002 | Add backing instruction standard. | REQ-003 | done | `instructions/asset_class_mechanics.md`. |
| T-003 | Update catalogs and top-level README. | REQ-004, NFR-002 | done | `agents/README.md`, `specs/README.md`, root `README.md`. |
| T-004 | Run validation gates. | NFR-001, NFR-002 | done | `spec`, `agent-catalog`, `docs-link`, `spec-index`, contract-presence, and `git diff --check`. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `hooks/stages/run-stage.sh agent-catalog` | done |
| AC-002 | Inspect each `agents/asset_classes/*/instructions.md` `Spec-Driven Role` section | done |
| AC-003 | `hooks/stages/run-stage.sh spec-index` | done |
| AC-004 | `hooks/stages/run-stage.sh spec docs-link`; `git diff --check` | done |

## Follow-ups

- Add a runtime mechanics helper under `src/quantsmith/` (e.g. a corporate-action
  price adjuster, a point-in-time curve builder, or a perpetual-funding-rate
  series builder) once a concrete workflow needs one, promoted through a new
  numbered spec following the `0006`/`0007` pattern.
- Revisit taxonomy breadth (credit derivatives, private markets, structured
  products) only if a concrete workflow needs mechanics coverage the five
  existing agents do not provide.
