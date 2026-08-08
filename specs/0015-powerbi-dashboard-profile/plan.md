# Plan: Power BI dashboard profile

- **Spec:** 0015-powerbi-dashboard-profile (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Two small, deterministic pieces: a tool-agnostic `DashboardSpec` contract, and a
Power BI renderer that maps it onto the existing `PowerBIPayload` and validates with
the existing `PowerBIPayloadValidator`. Governance holds *by construction* — the spec
rejects metric-less panels and unknown chart types at construction, so only a governed
design can be rendered. Pure Python; reuses existing Power BI code (repaired here).

## Agent Routing

```text
analytics/dashboard_design (DashboardSpec)
  -> [render_powerbi]                 # map spec -> Power BI payload
  -> powerbi-dashboard-agent / tooling/power_bi   # review, governance, publish
```

Upstream metrics come from `metrics_semantic_layer` (`0008`); the design comes from
`analytics/dashboard_design` (`0014`).

## Architecture & Components

- `DashboardSpec` / `Panel` (`pipelines/dashboard_spec.py`) — the tool-agnostic
  contract: ordered panels (title, chart type from `CHART_TYPES`, governed metric,
  dimensions), dataset, page, filters. Validates itself on construction.
- `render_powerbi(spec)` (`pipelines/powerbi_profile.py`) — maps chart types to Power
  BI visuals via `_CHART_TO_VISUAL`, metrics to measures (de-duplicated, ordered),
  carries dataset/page/filters, and validates with `PowerBIPayloadValidator`.
- Repair: add the missing `PowerBIPayload` dataclass to
  `agentic_code_tools/contracts.py` so `agentic_code_tools/powerbi.py` imports.

## Interfaces & Data Contracts

- Input: a `DashboardSpec` whose panels reference governed metric names (`0008`).
- Output: a validated `PowerBIPayload` (title, dataset, report_page, visuals,
  measures, filters).
- Chart vocabulary: `bar, line, area, scatter, table, kpi, gauge, map` →
  `clustered_column, line, area, scatter, matrix, card, gauge, map`.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Spec rejects ungoverned panels / unknown charts at construction; render is deterministic. |
| P5 Reversibility | yes | A payload is a build artifact; re-render from the spec. |
| P6 Observability | yes | The payload validates against an explicit schema. |
| P9 Security & data | yes | No private data, secrets, or credentials; no live publish. |
| P10 Honest reporting | yes | Governed metrics only; restricted chart vocabulary avoids misleading visuals. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `DashboardSpec` / `Panel` + `CHART_TYPES` | T-001 |
| REQ-002 | `render_powerbi` mapping | T-002 |
| REQ-003 | spec construction guards + validator call | T-001, T-002 |
| REQ-004 | `PowerBIPayload` added to contracts | T-003 |
| NFR-001 | reuse `PowerBIPayload`/validator | T-002, T-003 |
| NFR-002 | deterministic mapping | T-002 |
| NFR-003 | governed metrics + chart vocabulary | T-001, T-002 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Payload | Reuse `PowerBIPayload` + validator | New Power BI payload type | Reuse avoids divergent contracts; repairs existing dead code (NFR-001). |
| Spec contract | Shared tool-agnostic `DashboardSpec` | Per-tool spec | One design contract, many renderers — no rework per tool. |
| Chart types | Fixed vocabulary, rejected if unknown | Free-form strings | A vocabulary prevents misleading/unsupported visuals (NFR-003). |
| Publish | Produce a validated payload | Live workspace publish | Publishing is a deployment concern, out of this slice. |

## Validation Strategy

- AC-001/002: render a spec; assert visuals/measures mapping and carry-through; assert
  chart-type mapping and rejection of unknown types.
- AC-003/005: assert metric-less panels and empty specs raise; assert the payload
  passes the validator.
- AC-004: render twice; assert identical payloads and preserved filters/dataset.

## Rollout, Observability & Rollback

A renderer imported by the Power BI agents. Rollout adds it; rollback removes it. The
`DashboardSpec` remains the tool-agnostic source of truth, so a design can be
re-rendered to Power BI or any future profile at any time.

## Open Questions

- Which profile is next (Looker vs Streamlit), and whether to add a live-publish
  deployment step behind the adapter contract.
