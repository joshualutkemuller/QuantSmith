# Plan: Remaining BI dashboard profiles

- **Spec:** 0018-remaining-dashboard-profiles (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Four more renderers on the `0016` pattern, sharing one payload type and one mapping
helper (they differ only by chart-type dictionary), plus a Streamlit executable
scaffolder parallel to the React one. Governance holds by construction — the shared
`DashboardSpec` rejects ungoverned/unknown before any renderer runs. Pure Python.

## Agent Routing

```text
analytics/dashboard_design (DashboardSpec)
  -> render_streamlit -> tooling/streamlit_dash  -> scaffold_streamlit (app.py)
  -> render_looker    -> tooling/looker
  -> render_superset  -> tooling/superset
  -> render_qlik      -> tooling/qlik
```

Seven render targets now share one design: Power BI, Excel, React (`0015`/`0016`) and
Streamlit, Looker, Superset, Qlik (this spec).

## Architecture & Components

- `pipelines/bi_profiles.py` — `BiDashboardPayload` / `BiElement`, per-tool
  `_CHART_MAPS`, a private `_render(spec, tool)`, and the four `render_*` entry points.
- `adapters/dashboard_render/streamlit_scaffold.py` — `scaffold_streamlit(payload,
  destination, dry_run)`: deterministic `app.py` + `requirements.txt`, data loaded from
  `$DATA_ENDPOINT`, a secret guard, dry-run planning.
- Agents: `tooling/streamlit_dash`, `tooling/looker`, `tooling/qlik`,
  `tooling/superset` (four-file contracts).

## Interfaces & Data Contracts

- Input: a `DashboardSpec` (`0014`/`0015`).
- Output: a `BiDashboardPayload(tool, title, dataset, page, elements, filters)` with
  `measures()`/`object_types()`; and, for Streamlit, a `RenderResult` from the
  scaffolder.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Shared spec rejects ungoverned/unknown; deterministic mappings and scaffold. |
| P5 Reversibility | yes | Payloads/apps are regenerable from the spec. |
| P6 Observability | yes | Scaffolder emits a checksum manifest; payloads expose measures/object types. |
| P9 Security & data | yes | Streamlit data via endpoint; secret guard; no credentials embedded. |
| P10 Honest reporting | yes | Governed metrics only; documented chart mappings per tool. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `render_streamlit/looker/superset/qlik` + `_CHART_MAPS` | T-001 |
| REQ-002 | `scaffold_streamlit` | T-002 |
| REQ-003 | four `tooling/` agents | T-003 |
| REQ-004 | shared `DashboardSpec` guards | T-001 |
| NFR-001 | deterministic render + scaffold | T-001, T-002 |
| NFR-002 | one payload + mapping helper; reuse render result | T-001, T-002 |
| NFR-003 | governed metrics + secret guard | T-001, T-002 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Payload | One `BiDashboardPayload` with a `tool` field | Four tool-specific payloads | DRY; the tool object type is captured per element. |
| Streamlit | Executable scaffolder | Payload only | Python-native — cheap to generate a runnable app, like React. |
| Looker/Superset/Qlik | Payload only | Executable emitters | Those tools import their own spec formats; emitters are a follow-up. |
| Agents | One per tool | Profiles under one agent | Each tool has distinct review rules (LookML, associative model, SQL/Jinja, caching). |

## Validation Strategy

- AC-001/002/003: render each tool; assert object-type mapping, carry-through, and
  determinism.
- AC-004: assert ungoverned/empty specs are refused.
- AC-005/006: scaffold Streamlit; assert runnable files, no secrets, endpoint load,
  non-Streamlit rejection, dry-run planning, and manifest determinism.

## Rollout, Observability & Rollback

Renderers imported by the BI-tool agents; the Streamlit scaffolder by
`tooling/streamlit_dash`. Rollout adds them; rollback removes them. The `DashboardSpec`
remains the tool-agnostic source of truth.

## Open Questions

- Executable emitters for Looker (LookML), Superset (import JSON), and Qlik (load
  script), and live publish/host behind the scheduler/CI adapters.
