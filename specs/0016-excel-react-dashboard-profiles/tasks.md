# Tasks: Excel and React dashboard profiles

- **Spec:** 0016-excel-react-dashboard-profiles (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- Both renderers reuse the shared `DashboardSpec`; only governed metrics appear.
- No secrets, credentials, or private data introduced; runtime code lives under
  `src/quantsmith/`.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Implement `render_excel` + `ExcelWorkbookPayload`/`ExcelChart`. | REQ-001, REQ-003, NFR-001, NFR-003 | done | Data sheet + dashboard sheet; chart-type mapping. |
| T-002 | Implement `render_react` + `ReactDashboardPayload`/`ReactComponent`/`GridItem`. | REQ-002, REQ-003, NFR-001, NFR-003 | done | Component per panel; deterministic grid. |
| T-003 | Add the `tooling/react` agent (four-file contract + Spec-Driven Role). | REQ-004 | done | Web-dashboard review; Excel uses existing `tooling/excel`. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtimes: `src/quantsmith/pipelines/excel_profile.py` and
`src/quantsmith/pipelines/react_profile.py`. A production build may add an `.xlsx`
writer and a React scaffold behind the adapter contract; the shared spec and payloads
are unchanged.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_excel_react_profiles.py::test_excel_render_AC_001` | done |
| AC-002 | `tests/test_excel_react_profiles.py::test_react_render_AC_002` | done |
| AC-003 | `tests/test_excel_react_profiles.py::test_carry_through_and_governed_AC_003` | done |
| AC-004 | `tests/test_excel_react_profiles.py::test_deterministic_AC_004` | done |
| AC-005 | `tests/test_excel_react_profiles.py::test_ungoverned_spec_refused_AC_005` | done |

## Follow-ups

- Add a live `.xlsx` writer and a React scaffold behind the adapter contract.
- Add the remaining BI-tool profiles (Looker, Qlik, Superset, Streamlit) on the same
  shared spec.