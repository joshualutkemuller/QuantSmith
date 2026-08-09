# Spec: Remaining BI dashboard profiles

- **ID:** 0018-remaining-dashboard-profiles
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Finishes the dashboard track: renders the shared `DashboardSpec` to the remaining
> common BI tools, and makes Streamlit executable like React and Excel.

## Problem & Context

Specs `0015`/`0016` render the shared `DashboardSpec` to Power BI, Excel, and React,
and `0017` ships executable providers for React and `.xlsx`. Four common BI targets
remained on the backlog — **Streamlit, Looker, Superset, Qlik** — leaving the dashboard
track incomplete. This spec adds a renderer for each (one design, seven render
targets), adds an executable **Streamlit scaffolder** so a Python-native app can be
generated like the React one, and adds the four `tooling/` agents so every target has a
review contract.

## Goals

- A renderer for Streamlit, Looker, Superset, and Qlik that maps the shared
  `DashboardSpec` to a tool-specific payload, governed metrics only.
- An executable Streamlit scaffolder (pure standard library) that writes a runnable
  app from the Streamlit payload.
- A `tooling/` agent per new tool (`streamlit_dash`, `looker`, `qlik`, `superset`).
- Complete parity across BI targets: the same governed design renders everywhere.

## Non-Goals

- Live publishing/hosting to any BI service (a deployment concern; the payloads and the
  Streamlit scaffold are the deliverables).
- New dashboard design or metric semantics (owned by `0014`/`0008`).
- Executable scaffolders for Looker/Superset/Qlik (payload-only; those tools import
  their own spec formats).

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Provide `render_streamlit`, `render_looker`, `render_superset`, and `render_qlik` that map a `DashboardSpec` to a tool-specific payload (one element per panel, chart types mapped to each tool's object types), carrying dataset, page, filters, and governed metrics. | must |
| REQ-002 | Provide an executable `scaffold_streamlit` that writes a runnable Streamlit app (`app.py`, pinned `requirements.txt`) from the Streamlit payload, with data loaded from a governed endpoint and no secrets in the app. | must |
| REQ-003 | Add a `tooling/` agent for each new tool (`streamlit_dash`, `looker`, `qlik`, `superset`), each on the four-file contract with a Spec-Driven Role. | should |
| REQ-004 | All renderers shall reuse the shared `DashboardSpec` and render only governed metrics; ungoverned/empty specs are refused upstream. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Reproducibility | The same `DashboardSpec` renders to identical payloads, and the same Streamlit payload scaffolds identical files. |
| NFR-002 | Reuse | All four renderers share one payload type and one mapping helper; the Streamlit scaffolder reuses the `dashboard_render` result/manifest. |
| NFR-003 | Honesty & governance | Only governed metrics are rendered; each tool's chart mapping preserves the intended encoding; no secrets in generated apps. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given a `DashboardSpec`, when rendered to each tool, then each panel maps to that tool's object type. | REQ-001 |
| AC-002 | Given a spec, when rendered to any of the four tools, then the governed measures, dataset, page, and filters are carried through. | REQ-001, REQ-004, NFR-003 |
| AC-003 | Given a spec, when rendered twice to any tool, then the payloads are identical. | NFR-001 |
| AC-004 | Given an ungoverned or empty spec, when rendering is attempted, then it is refused (by the shared `DashboardSpec`). | REQ-004, NFR-002 |
| AC-005 | Given a Streamlit payload, when scaffolded, then a runnable app is written with governed metrics and an endpoint-based data load, and no secrets; a non-Streamlit payload is rejected. | REQ-002, NFR-003 |
| AC-006 | Given a Streamlit payload, when scaffolded with `dry_run`, then files are planned without writing; two scaffolds produce identical manifests. | REQ-002, NFR-001 |

## Data & Dependencies

- Input: a `DashboardSpec` from `analytics/dashboard_design` (`0014`/`0015`), governed
  metrics from `0008`.
- Runtime: `src/quantsmith/pipelines/bi_profiles.py` (renderers) and
  `src/quantsmith/adapters/dashboard_render/streamlit_scaffold.py` (scaffolder).
- Agents: new `tooling/streamlit_dash`, `tooling/looker`, `tooling/qlik`,
  `tooling/superset`.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Ungoverned or misleading visuals reach a BI tool. | Untrustworthy dashboards. | Governed metrics only; the shared spec's chart vocabulary restricts types (NFR-003). |
| RISK-002 | Divergent design contracts per tool. | Rework, inconsistency. | One shared `DashboardSpec` and one payload/mapping helper (NFR-002). |
| RISK-003 | Secrets leak into a generated Streamlit app. | Credential exposure. | Data via an endpoint; a secret guard rejects credential-shaped content. |
| RISK-004 | Agent sprawl across BI tools. | Hard to route. | Narrow, template-consistent agents; payload-only for Looker/Qlik/Superset. |

## Assumptions & Open Questions

- Assumption: a validated payload (and, for Streamlit, a scaffolded app) is the
  deliverable; publishing/hosting is separate.
- Open question: whether Looker/Superset/Qlik warrant executable emitters (LookML,
  Superset import JSON, Qlik script) behind the adapter contract (tracked, not deferred
  silently).

## Exceptions

None.
