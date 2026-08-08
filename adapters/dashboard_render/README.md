# Dashboard Render Adapters

Dashboard render adapters turn an already-rendered dashboard payload into a **live
artifact** — a real `.xlsx` workbook, a scaffolded React app, or a published Power BI
report. The design work is done upstream: `analytics/dashboard_design` produces the
tool-agnostic `DashboardSpec`, and the profile renderers
(`render_powerbi`/`render_excel`/`render_react`, specs `0015`/`0016`) produce a
validated, governed payload. These adapters only materialize that payload.

## Files

| File | Purpose |
| --- | --- |
| `adapter_contract.md` | Payload-neutral schema for turning a rendered dashboard payload into a live artifact. |
| `xlsx.md` | Write a real `.xlsx` workbook from an `ExcelWorkbookPayload`. |
| `react_scaffold.md` | Scaffold a React app from a `ReactDashboardPayload`. |

Planned providers (same contract): `powerbi_publish.md` (publish/export a
`PowerBIPayload`), and Streamlit/Looker/Qlik/Superset once their profile renderers
land.

## Design Rule

The workflow owns the design and the governed metrics; the profile renderer owns the
payload; the adapter owns file/bundle generation, provider metadata, and evidence of
output. Adapters never redefine metrics, redesign the dashboard, embed data, or hold
secrets — data is reached through a `data_access/` adapter and secrets through
`secrets_management/`.
