# Tasks: Data Analyst storytelling & dashboard expansion

- **Spec:** 0014-data-analyst-storytelling (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a check. Agent-expansion spec — the "tests" are the catalog/docs gates.

## Definition of Done (applies to every task)

- New agents follow the four-file contract with a Spec-Driven Role.
- Agents reuse existing runtimes/agents; no metric, reporting, or tool-payload code is
  duplicated.
- Numbers come only from the governed `Report` (`0010`); no claim beyond the evidence.
- No secrets, credentials, or private data introduced.
- Catalog, workflow map, spec index, and handoff updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Add `analytics/data_storytelling` agent (narrative from a governed Report). | REQ-001, REQ-003, NFR-001, NFR-002, NFR-003 | done | Hands narrative to `reporting-agent`. |
| T-002 | Add `analytics/dashboard_design` agent (tool-agnostic dashboard spec). | REQ-002, REQ-003, NFR-001, NFR-002 | done | Rendered by the tool-specific dashboard agents. |
| T-003 | Add `instructions/data_storytelling.md` backing standard. | REQ-001, REQ-002, NFR-003 | done | Shared by storytelling, dashboard, and reporting agents. |
| T-004 | Update catalog, workflow map, spec index, and handoff; run gates. | REQ-003, NFR-001 | done | agent-catalog, docs-link, spec, spec-index pass. |
| T-005 | Tooling-expansion track: `tooling/looker`, `qlik`, `superset`, `streamlit_dash` profiles. | REQ-004 | todo (planned) | Render the shared dashboard spec; build as consumers appear. |
| T-006 | Optional `analytics/data_visualization` agent (single-chart encoding/accessibility). | REQ-002 | todo (planned) | Split from `dashboard_design` only if it grows too broad. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

This is an agent/documentation expansion; it adds no Python runtime because it reuses
the `0010` analytics-pipeline `Report` as its input. Validation is via the catalog and
docs gates, not a pytest module.

## Test Coverage Map

| Acceptance criterion | Check | Status |
| --- | --- | --- |
| AC-001 | `hooks/stages/run-stage.sh agent-catalog` | done |
| AC-002 | inspect `docs/workflows.md` (Data Analyst route) | done |
| AC-003 | inspect `agents/analytics/*/instructions.md` (declared inputs/handoffs) | done |
| AC-004 | `hooks/stages/run-stage.sh spec spec-index docs-link agent-catalog` | done |

## Follow-ups

- Build the BI-tool profiles (T-005) and, if needed, split out `data_visualization`
  (T-006).
- Consider a lightweight `narrative-provenance` check that a published narrative cites
  a governed `Report`.