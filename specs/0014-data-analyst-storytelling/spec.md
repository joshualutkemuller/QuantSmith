# Spec: Data Analyst storytelling & dashboard expansion

- **ID:** 0014-data-analyst-storytelling
- **Status:** Approved
- **Author:** QuantSmith
- **Approver:** QuantSmith
- **Last updated:** 2026-08-08

> Reference example. WHAT and WHY only. Implementation lives in `plan.md`.
> Agent-expansion spec (like `0004`): adds the *communication layer* of the Data
> Analyst role on top of the existing governed-analysis runtimes, reusing them
> rather than duplicating.

## Problem & Context

The Data Analyst role can now produce trustworthy numbers — governed metrics
(`0008`), disciplined experiments (`0009`), and an end-to-end pipeline that emits a
provenance-carrying `Report` (`0010`). What it lacks are the specialists who turn
that governed analysis into *communication*: a narrative a stakeholder acts on, and a
dashboard designed for comprehension. Today reporting is a single `reporting-agent`
(artifacts) and dashboards are tool-specific payload agents (`tableau`/`powerbi`).
There is no storytelling role and no tool-agnostic dashboard-design role, so framing
and layout are ad hoc and inconsistent. This spec adds those specialists — the
efficient way, by consuming existing outputs and handing off to existing renderers.

## Goals

- A data-storytelling agent that turns a governed `Report` into an audience-tailored
  narrative (situation → insight → recommended action) that never claims beyond the
  governed evidence.
- A tool-agnostic dashboard-design agent that produces a dashboard *spec* (layout,
  chart selection, hierarchy, drill paths, accessibility) which existing BI-tool
  agents render.
- Maximum reuse: consume `0010` `Report`, `0008` metric definitions, and `0009`
  readouts; hand off to `reporting-agent` and the tool-specific dashboard agents.
- A defined tooling-expansion track for specific BI tools (Looker, Qlik, Superset,
  Streamlit) as thin profiles that render the shared dashboard spec.

## Non-Goals

- Reimplementing metrics, experiments, reporting artifacts, or tool-specific payloads
  (owned by existing agents/runtimes — this spec composes them).
- A new charting/rendering engine; visualization standards reuse the `dataviz` skill.
- Building every BI-tool profile now; those are a defined, prioritized track.

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | Add a `data_storytelling` agent that turns a governed `Report` (`0010`) into an audience-tailored narrative (situation → insight → action), carrying provenance and making no claim beyond the governed evidence. | must |
| REQ-002 | Add a `dashboard_design` agent that produces a tool-agnostic dashboard spec (layout, chart selection, information hierarchy, drill paths, accessibility) for existing BI-tool agents to render. | must |
| REQ-003 | The new agents shall consume existing outputs (`0010` Report, `0008` definitions, `0009` readouts) and hand off to `reporting-agent` and the tool-specific dashboard agents — not duplicate them. | must |
| REQ-004 | Define a tooling-expansion track (Looker, Qlik, Superset, Streamlit) as profiles that render the shared dashboard spec. | should |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Contract consistency | Every new agent has `README.md`, `prompt.md`, `instructions.md`, `tasks.md` and a Spec-Driven Role. |
| NFR-002 | No duplication | New agents reference existing agents/runtimes; they do not reimplement metrics, reporting, or tool payloads. |
| NFR-003 | Honest communication | Narratives and dashboards carry provenance and never assert beyond the governed numbers or an experiment's significance. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given the agents directory, when the catalog check runs, then `analytics/data_storytelling` and `analytics/dashboard_design` are listed in `agents/README.md`. | REQ-001, REQ-002, NFR-001 |
| AC-002 | Given the workflow map, when the Data Analyst route is read, then it names the path from a governed `Report` to a narrative / dashboard spec to the reporting and tool-specific dashboard agents. | REQ-003 |
| AC-003 | Given the new agents, when their instructions are read, then each declares the existing inputs it consumes (`0010`/`0008`/`0009`) and the existing agents it hands to — no reimplementation. | REQ-003, NFR-002 |
| AC-004 | Given the documentation set, when the spec, spec-index, docs-link, and agent-catalog checks run, then the new spec, index entry, and docs pass. | NFR-001 |

## Data & Dependencies

- Inputs (reused, not rebuilt): `0010` `Report` (value + provenance), `0008` metric
  definitions, `0009` experiment readouts.
- Handoffs (reused): `reporting-agent`, `tableau-dashboard-agent`,
  `powerbi-dashboard-agent`, `tooling/tableau`, `tooling/power_bi`.
- Standards: new `instructions/data_storytelling.md`; existing
  `instructions/documentation.md`, `instructions/metrics_semantic_layer.md`; the
  `dataviz` skill for chart standards.
- No private data or credentials are written to this repository.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | Narrative overclaims beyond the evidence. | Misleading decisions. | Narratives cite the governed `Report` and its provenance; no claim beyond it (NFR-003). |
| RISK-002 | New agents duplicate reporting/tool payloads. | Divergent, redundant outputs. | Reuse-only design; agents hand off to existing renderers (REQ-003 / NFR-002). |
| RISK-003 | Agent sprawl dilutes the catalog. | Hard to route. | Narrow roles; two agents now, the rest a prioritized track (REQ-004). |
| RISK-004 | Dashboards tied to one BI tool. | Rework per tool. | A tool-agnostic dashboard spec rendered by tool profiles (REQ-002, REQ-004). |

## Assumptions & Open Questions

- Assumption: the governed `Report` from `0010` is the canonical input for all
  communication agents; storytelling never recomputes numbers.
- Assumption: tool-specific rendering stays in the existing tool agents.
- Open question: which BI-tool profile to build first (Looker vs Streamlit) — decided
  when a downstream consumer picks a tool (tracked, not silently deferred).

## Exceptions

None.
