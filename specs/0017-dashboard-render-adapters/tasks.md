# Tasks: Dashboard render adapters (executable providers)

- **Spec:** 0017-dashboard-render-adapters (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; deviations noted in `plan.md`.
- Tests exist and pass deterministically.
- The core `pipelines/` stay dependency-free; optional deps are lazy in the adapter.
- No secrets, credentials, or private data in generated artifacts.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Implement `scaffold_react` (pure stdlib React app generation) with a secret guard. | REQ-001, REQ-003, REQ-004, NFR-002, NFR-003 | done | Deterministic file map; data via `/api/data`. |
| T-002 | Implement `write_xlsx` (openpyxl, lazy import) with dry-run. | REQ-002, REQ-003, REQ-004, NFR-002 | done | Data sheet + dashboard sheet with charts. |
| T-003 | Implement `RenderResult` / `FileRecord` / `manifest` and the `contains_secret` guard. | REQ-003, NFR-001, NFR-003 | done | Path-sorted sha256 evidence manifest. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtimes: `src/quantsmith/adapters/dashboard_render/{result,react_scaffold,xlsx}.py`.
The React provider is standard-library only; the XLSX provider needs `openpyxl` (added
to the `dev` extra) for a real write, and its dry-run works without it.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_dashboard_render_adapters.py::test_react_scaffold_writes_files_AC_001` | done |
| AC-002 | `tests/test_dashboard_render_adapters.py::test_react_dry_run_plans_only_AC_002` | done |
| AC-003 | `tests/test_dashboard_render_adapters.py::test_react_no_secrets_AC_003` | done |
| AC-004 | `tests/test_dashboard_render_adapters.py::test_xlsx_dry_run_AC_004`, `::test_xlsx_real_write_AC_004` | done |
| AC-005 | `tests/test_dashboard_render_adapters.py::test_deterministic_AC_005` | done |
| AC-006 | `tests/test_dashboard_render_adapters.py::test_renders_only_payload_AC_006` | done |

## Follow-ups

- Add a `powerbi_publish` provider and a hosted-deploy step behind the scheduler/CI
  adapters.
- Populate the workbook data sheet and the React fetch from a real `data_access/`
  adapter in an end-to-end example.