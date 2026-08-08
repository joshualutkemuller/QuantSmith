# Plan: Data Analyst storytelling & dashboard expansion

- **Spec:** 0014-data-analyst-storytelling (`spec.md`)
- **Status:** Approved
- **Author:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. HOW. Requires the approved `spec.md`.

## Approach

Add the communication layer as **thin specialist agents that compose existing
runtimes**, not new engines. The governed `Report` from `0010` (value +
provenance) is the single input contract; storytelling and dashboard design read it
and hand off to the existing reporting and tool-specific dashboard agents. This is
the most efficient expansion: no metric, experiment, reporting, or tool-payload code
is rewritten.

## What We Reuse (the efficiency of this plan)

| Need | Reused, not rebuilt |
| --- | --- |
| Governed numbers | `analytics/metrics_semantic_layer` (`0008`) + the `Report` from `0010` |
| Experiment results | `analytics/experimentation` (`0009`) readouts |
| End-to-end data → answer | `analytics_pipeline` runtime (`0010`) `Report` with provenance |
| Report artifacts | `reporting-agent` |
| Tool rendering | `tableau-dashboard-agent`, `powerbi-dashboard-agent`, `tooling/tableau`, `tooling/power_bi` |
| Chart standards | the `dataviz` skill |

## New Agents (analytics group)

```text
0010 Report / 0008 defs / 0009 readouts
  -> analytics/data_storytelling     # narrative: situation -> insight -> action
  -> analytics/dashboard_design      # tool-agnostic dashboard spec
  -> reporting-agent | tableau-dashboard-agent | powerbi-dashboard-agent  (render)
```

- `analytics/data_storytelling` — turns a governed `Report` into an audience-tailored
  narrative arc; frames the "so what" and the recommended action; carries provenance;
  never claims beyond the evidence. Hands the narrative to `reporting-agent`.
- `analytics/dashboard_design` — produces a tool-agnostic **dashboard spec**
  (information hierarchy, chart-type selection, layout, drill paths, filters,
  accessibility) that the tool-specific dashboard agents render. Uses the `dataviz`
  skill for chart/color/accessibility standards.

## Tooling-Expansion Track (planned)

Thin BI-tool profiles that render the shared dashboard spec, prioritized as consumers
appear (already in `docs/handoffs/future_features.md`):

- `tooling/looker`, `tooling/qlik`, `tooling/superset`, `tooling/streamlit_dash`.

An optional `analytics/data_visualization` agent (single-chart encoding/accessibility)
may be split out later if `dashboard_design` grows too broad.

## Interfaces & Data Contracts

- Input: a `Report` (metric, value, provenance) from `0010`; optionally a metric
  definition (`0008`) and an experiment readout (`0009`).
- `data_storytelling` output: a narrative (audience, key message, insight, action,
  caveats) plus the source provenance.
- `dashboard_design` output: a dashboard spec (panels with chart type, encodings,
  metric refs, hierarchy, drill paths, filters, accessibility notes) for a renderer.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P4 Correct by construction | yes | Numbers come only from the governed `Report`; agents never recompute. |
| P6 Observability | yes | Narrative and dashboard spec carry the source provenance. |
| P9 Security & data | yes | No private data, secrets, or credentials in the repo. |
| P10 Honest reporting | yes | No claim beyond the governed evidence or an experiment's significance. |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `analytics/data_storytelling` agent | T-001 |
| REQ-002 | `analytics/dashboard_design` agent | T-002 |
| REQ-003 | reuse-only routing + instructions declaring inputs/handoffs | T-001, T-002, T-004 |
| REQ-004 | tooling-expansion track in backlog + plan | T-005 |
| NFR-001 | four-file contract + Spec-Driven Role | T-001, T-002 |
| NFR-002 | no new metric/reporting/tool code | T-001, T-002 |
| NFR-003 | provenance + evidence-bounded framing | T-001, T-002 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Layer | Thin agents over `0010` Report | New reporting/dashboard runtime | Reuse is faster and avoids divergence (NFR-002). |
| Dashboard design | Tool-agnostic spec + existing renderers | Per-tool design agents | One design contract, many renderers; no rework per tool. |
| Visualization | Fold into `dashboard_design` for now | Separate agent immediately | Avoid sprawl; split out only if it grows too broad. |
| Storytelling vs reporting | Storytelling above `reporting-agent` | Extend `reporting-agent` | Keep `reporting-agent` as the renderer; narrative is a distinct concern. |

## Validation Strategy

- AC-001: `hooks/stages/run-stage.sh agent-catalog` lists both new agents.
- AC-002: inspect `docs/workflows.md` Data Analyst route.
- AC-003: inspect each agent's `instructions.md` for declared inputs/handoffs.
- AC-004: `hooks/stages/run-stage.sh spec spec-index docs-link agent-catalog`.

## Rollout, Observability & Rollback

Documentation-only expansion (agents + a standard). Rollout adds the agents and
routing; rollback removes them. No runtime state; the governed `Report` remains the
source of truth for every number communicated.

## Open Questions

- Which BI-tool profile first (Looker vs Streamlit), and whether to split out a
  dedicated `data_visualization` agent.
