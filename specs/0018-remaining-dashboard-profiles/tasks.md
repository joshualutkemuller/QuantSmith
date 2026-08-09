# Tasks: Remaining BI dashboard profiles

- **Spec:** 0018-remaining-dashboard-profiles (`spec.md`, `plan.md`)
- **Last updated:** 2026-08-08

> Reference example. Every task cites a requirement; every acceptance criterion is
> named by a test.

## Definition of Done (applies to every task)

- Code matches the plan; tests exist and pass deterministically.
- All renderers reuse the shared `DashboardSpec`; only governed metrics appear.
- No secrets in generated apps; runtime code lives under `src/quantsmith/`.
- New agents follow the four-file contract with a Spec-Driven Role.
- Docs updated alongside the change.

## Task List

| ID | Task | Covers | Status | Notes |
| --- | --- | --- | --- | --- |
| T-001 | Implement `render_streamlit/looker/superset/qlik` (shared `BiDashboardPayload` + `_CHART_MAPS`). | REQ-001, REQ-004, NFR-001, NFR-002, NFR-003 | done | One helper; four entry points. |
| T-002 | Implement `scaffold_streamlit` (executable, pure stdlib) with dry-run + secret guard. | REQ-002, NFR-001, NFR-003 | done | `app.py` + `requirements.txt`; data via `$DATA_ENDPOINT`. |
| T-003 | Add `tooling/streamlit_dash`, `tooling/looker`, `tooling/qlik`, `tooling/superset` agents. | REQ-003 | done | Four-file contracts + Spec-Driven Role. |

Status values: `todo` | `in-progress` | `blocked` | `done`.

Runtimes: `src/quantsmith/pipelines/bi_profiles.py` and
`src/quantsmith/adapters/dashboard_render/streamlit_scaffold.py`. Looker/Superset/Qlik
are payload-only; executable emitters are a follow-up.

## Test Coverage Map

| Acceptance criterion | Test(s) | Status |
| --- | --- | --- |
| AC-001 | `tests/test_bi_profiles.py::test_tool_mappings_AC_001` | done |
| AC-002 | `tests/test_bi_profiles.py::test_measures_and_carry_through_AC_002` | done |
| AC-003 | `tests/test_bi_profiles.py::test_deterministic_AC_003` | done |
| AC-004 | `tests/test_bi_profiles.py::test_ungoverned_refused_AC_004` | done |
| AC-005 | `tests/test_bi_profiles.py::test_streamlit_scaffold_AC_005` | done |
| AC-006 | `tests/test_bi_profiles.py::test_streamlit_dry_run_and_determinism_AC_006` | done |

## Follow-ups

- Executable emitters for Looker (LookML), Superset (import JSON), and Qlik (load
  script) behind the `adapters/dashboard_render/` contract.
- A `powerbi_publish` provider and live publish/host behind the scheduler/CI adapters.
