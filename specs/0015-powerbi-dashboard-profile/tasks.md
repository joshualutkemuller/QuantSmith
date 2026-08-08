# Tasks: Power BI dashboard profile

- **Spec:** 0015-powerbi-dashboard-profile (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Reuses the existing Power BI payload and validator; governance holds by construction.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Implement the tool-agnostic `DashboardSpec`/`Panel` contract with construction-time governance. | REQ-001, REQ-003, NFR-003 | done | Governed metric + chart vocabulary enforced. |
| T-002 | Implement `render_powerbi` (spec → validated Power BI payload). | REQ-002, REQ-003, NFR-001, NFR-002, NFR-003 | done | De-duplicated, ordered mapping; validated. |
| T-003 | Repair the `PowerBIPayload` contract so the Power BI runtime imports. | REQ-004, NFR-001 | done | Added to `agentic_code_tools/contracts.py`. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtimes: `src/quantsmith/pipelines/dashboard_spec.py` (shared contract) and
`src/quantsmith/pipelines/powerbi_profile.py` (renderer). A production build may add a
live-publish step behind the adapter contract; the spec and payload are unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_powerbi_profile.py::test_render_maps_panels_AC_001` | done |
| AC-002 | `tests/test_powerbi_profile.py::test_chart_type_mapping_AC_002` | done |
| AC-003 | `tests/test_powerbi_profile.py::test_governance_and_validation_AC_003` | done |
| AC-004 | `tests/test_powerbi_profile.py::test_carry_through_and_deterministic_AC_004` | done |
| AC-005 | `tests/test_powerbi_profile.py::test_empty_spec_rejected_AC_005` | done |

## Follow-ups

- Add the next BI-tool profiles that render the same `DashboardSpec`: Looker, Qlik,
  Superset, Streamlit.
- Optionally add a live-publish deployment step behind the adapter contract.