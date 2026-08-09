# Plan: Dashboard render adapters (executable providers)

- **Spec:** 0017-dashboard-render-adapters (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Two providers under `src/quantsmith/adapters/dashboard_render/`, deliberately outside
`src/quantsmith/pipelines/` (which stays dependency-free). The React provider is pure
standard library; the XLSX provider imports openpyxl *lazily* inside the write path, so
the module imports everywhere and dry-run needs no dependency. Both are deterministic
and return the contract's `RenderResult` with an evidence manifest.

## Agent Routing

```text
render_excel / render_react (0016)  -> governed payload
  -> adapters/dashboard_render (this spec)
       write_xlsx     -> .xlsx workbook        (tooling/excel)
       scaffold_react -> React app source      (tooling/react)
  -> artifact_delivery / scheduler adapters (publish/host — separate)
```

## Architecture & Components

- `result.py` — `RenderResult`, `FileRecord`, `manifest()` (path-sorted sha256), and a
  `contains_secret()` guard for credential-shaped content.
- `react_scaffold.py` — `scaffold_react(payload, destination, dry_run)`: builds a
  deterministic file map (`package.json`, `src/main.jsx`, `src/Dashboard.jsx`,
  `src/useData.js`, `src/components/registry.jsx`, README, `.gitignore`), rejects
  secrets, then plans (dry-run) or writes.
- `xlsx.py` — `write_xlsx(payload, destination, dry_run)`: data sheet (header row from
  measures + dimensions) and dashboard sheet (a native chart per supported type, a
  titled cell otherwise); openpyxl imported lazily; dry-run plans without writing.

## Interfaces & Data Contracts

- Input: `ReactDashboardPayload` / `ExcelWorkbookPayload` (`0016`).
- Output: `RenderResult(status, artifact_uri, files, dry_run)` per the adapter
  contract; `status` in {generated, planned, skipped, failed}.
- The React app fetches data from `/api/data?dataset=…`; the workbook data sheet holds
  headers only — data is populated by a `data_access/` adapter downstream.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Deterministic generation; renders strictly from the payload. |
| P5 Reversibility | yes | Artifacts are regenerable from the payload; delete and re-run. |
| P6 Observability | yes | Evidence manifest with per-file checksums and sizes. |
| P9 Security & data | yes | No embedded data/credentials; secret check; data via endpoint. |
| P10 Honest reporting | yes | Only governed metrics/components; dry-run reports the true plan. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `scaffold_react` file map | T-001 |
| REQ-002 | `write_xlsx` workbook build | T-002 |
| REQ-003 | dry-run + `RenderResult`/`manifest` | T-001, T-002, T-003 |
| REQ-004 | payload-only render + `contains_secret` + endpoint fetch | T-001, T-002 |
| NFR-001 | deterministic content + sorted checksums | T-003 |
| NFR-002 | stdlib React; lazy openpyxl | T-001, T-002 |
| NFR-003 | secret guard | T-001, T-003 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Location | `src/quantsmith/adapters/` | Inside `pipelines/` | Keeps the renderers dependency-free; adapters carry optional deps. |
| XLSX dependency | openpyxl, imported lazily | Hand-rolled OOXML zip | openpyxl is correct and maintained; lazy import preserves portability. |
| React output | Source scaffold + registry | Emit a bundled build | Source is inspectable, reviewable, and framework-version-agnostic. |
| Data | Fetch via endpoint | Embed rows | Keeps data and credentials out of the artifact (P9). |

## Validation Strategy

- AC-001/006: scaffold to a temp dir; assert files and that only used components appear.
- AC-002: dry-run; assert nothing written and a manifest returned.
- AC-003: assert no secrets and the `/api/data` fetch; governed metric in props.
- AC-004: xlsx dry-run plans; a real write (openpyxl) loads with the right sheets and
  header measures.
- AC-005: scaffold twice; assert identical manifests.

## Rollout, Observability & Rollback

Providers imported by the Excel/React agents. Rollout adds them; rollback removes them.
The manifest is the evidence surface. Publishing/hosting is a later step behind the
artifact-delivery and scheduler adapters.

## Open Questions

- Add a `powerbi_publish` provider and a hosted-deploy step behind the scheduler/CI
  adapters.
