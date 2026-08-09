# Spec: Dashboard render adapters (executable providers)

- **ID:** 0017-dashboard-render-adapters
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Executable providers behind the `adapters/dashboard_render/` contract: turn a
> rendered dashboard payload (`0015`/`0016`) into a live artifact.

## Problem & Context

Specs `0015`/`0016` render the shared `DashboardSpec` into validated payloads, and
`adapters/dashboard_render/` documents the contract for turning a payload into a live
artifact — but the providers were documentation only. This spec ships the first two
executable providers: a **React scaffolder** (pure standard library) that writes a
runnable React app, and an **XLSX writer** (openpyxl) that writes a real workbook. They
keep the core pipelines dependency-free — the optional dependency is imported lazily in
the adapter layer, not the renderers.

## Goals

- Generate a runnable React project from a `ReactDashboardPayload`, deterministically,
  with data fetched from a governed endpoint and no secrets in the bundle.
- Write a real `.xlsx` workbook from an `ExcelWorkbookPayload` (data sheet + dashboard
  sheet with charts), using openpyxl imported lazily.
- Support dry-run (plan the outputs without writing) and emit an evidence manifest with
  checksums, per the adapter contract.
- Render only the payload — no invented metrics, panels, or embedded data/credentials.

## Non-Goals

- Publishing/hosting the built app or workbook (a scheduler/CI/deployment concern).
- New chart design or metric semantics (owned by `0014`/`0008`).
- Live data population (data is fetched at runtime via a `data_access/` endpoint; the
  workbook data sheet carries headers, not embedded rows).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Generate a runnable React project (package manifest, dashboard component, component registry, data hook) from a `ReactDashboardPayload`, one component per panel at its grid position. | must |
| REQ-002 | Write a real `.xlsx` from an `ExcelWorkbookPayload`: a data sheet with header row from the governed measures/dimensions and a dashboard sheet with one chart per panel; openpyxl imported lazily. | must |
| REQ-003 | Both providers shall support `dry_run` (plan without writing) and return a `RenderResult` with status, artifact URI, and an evidence manifest (files + checksums). | must |
| REQ-004 | Both providers shall render only the payload — no invented metrics/panels — and embed no data or credentials; the React data hook fetches from a governed endpoint. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same payload yields the same files and manifest checksums on every run. |
| NFR-002 | Dependency isolation | The React provider is standard-library only; the XLSX provider imports openpyxl lazily so the module imports without it and dry-run needs no dependency. |
| NFR-003 | No secrets | Generated artifacts contain no embedded credentials; the check rejects credential-shaped content. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a `ReactDashboardPayload`, when scaffolded, then the expected React files are written and the manifest lists them. | REQ-001 |
| AC-002 | Given a payload, when scaffolded with `dry_run`, then the files are planned (manifest computed) and nothing is written. | REQ-003 |
| AC-003 | Given a scaffold, when the output is inspected, then it contains no secrets and the data hook fetches from `/api/data`; governed metrics appear in props. | REQ-004, NFR-003 |
| AC-004 | Given an `ExcelWorkbookPayload`, when `dry_run`, then the plan is returned without writing; when written (openpyxl present), then a loadable workbook with the data and dashboard sheets and the governed measures in the header is produced. | REQ-002, REQ-003 |
| AC-005 | Given the same payload, when scaffolded twice, then the manifests (paths + checksums) are identical. | NFR-001 |
| AC-006 | Given a payload, when scaffolded, then only the payload's used components are generated (no extras). | REQ-004 |

## Data & Dependencies

- Input: `ReactDashboardPayload` / `ExcelWorkbookPayload` from `render_react` /
  `render_excel` (`0016`).
- Contract: `adapters/dashboard_render/adapter_contract.md`, `react_scaffold.md`,
  `xlsx.md`.
- Optional dependency: `openpyxl` (in the `dev` extra), imported lazily.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | The optional dependency leaks into the dependency-free core. | Breaks portability. | openpyxl imported lazily inside the XLSX provider only (NFR-002). |
| RISK-002 | Generated artifacts embed secrets or data. | Credential/data exposure. | Data via a governed endpoint; a secret check rejects credential-shaped content (NFR-003). |
| RISK-003 | Non-deterministic output. | Noisy diffs, unverifiable evidence. | Deterministic content and path-sorted checksum manifest (NFR-001). |
| RISK-004 | Providers drift from the payload. | Ungoverned artifacts. | Render strictly from the payload; tests assert only used components/measures appear. |

## Assumptions & Open Questions

- Assumption: a validated, governed payload is the input; the design and metrics are
  fixed upstream.
- Open question: add a `powerbi_publish` provider and a live host/deploy step behind
  the scheduler/CI adapters (tracked, not silently deferred).

## Exceptions

None.
