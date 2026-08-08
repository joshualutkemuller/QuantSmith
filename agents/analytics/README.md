# Analytics Agents (`analytics/`)

The Analytics group holds the specialist roles that make **Data Analyst** work
consistent and trustworthy — starting with the metrics semantic layer, the single
place a KPI is defined.

## Group Workflow

These agents sit in the middle of the Data Analyst chain (see `docs/workflows.md` →
*Data Analyst*):

```text
planning_requirements -> sql-integration-agent -> data-prep-agent
  -> eda-specialist-agent -> metrics_semantic_layer
  -> tooling/tableau | tooling/power_bi -> quality-guard-agent -> reporting-agent

# experiment branch:
planning_requirements -> experimentation (design) -> (run) -> experimentation (readout)
  -> quality-guard-agent -> reporting-agent

# communication layer (from a governed Report):
metrics_semantic_layer / experimentation / analytics_pipeline (Report)
  -> data_storytelling (narrative) | dashboard_design (dashboard spec)
  -> reporting-agent | tableau-dashboard-agent | powerbi-dashboard-agent
```

## Agents

| Agent | Handles |
| --- | --- |
| `metrics_semantic_layer/` | Canonical KPI/metric definitions — one source of truth per metric, consistent point-in-time computation, declared dimensions, and derived (ratio) metrics. |
| `experimentation/` | A/B test design and readout — power/sample-size, sample-ratio-mismatch validity, p-value/CI consistency, and a power-gated verdict. |
| `data_storytelling/` | Turns a governed `Report` into an audience-tailored narrative (situation → insight → action); reuses `0008`/`0009`/`0010`, hands off to `reporting-agent`; never claims beyond the evidence. |
| `dashboard_design/` | Produces a tool-agnostic dashboard spec (hierarchy, chart selection, drill paths, accessibility) rendered by the tool-specific dashboard agents. |

The last two are the **communication layer** (spec `0014-data-analyst-storytelling`):
they compose existing governed outputs and hand off to existing renderers rather than
duplicating them.

## Rules

- Keep each specialist narrow and inspectable.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.
- A metric is defined once; consumers (dashboards, reports) read the definition, they
  do not redefine it.
- Runtime Python belongs under `src/quantsmith/` (the semantic-layer evaluator lives
  at `src/quantsmith/pipelines/metrics_semantic_layer.py`); agent directories describe
  roles, prompts, instructions, and tasks.

Planned (spec `0014`): a `data_visualization/` agent (single-chart encoding) and
BI-tool profiles under `tooling/` (Looker, Qlik, Superset, Streamlit) that render the
shared dashboard spec.

## Standards

- `instructions/metrics_semantic_layer.md` — how to define and govern metrics.
- `instructions/model_validation.md` — validation discipline behind experiment readouts.
- `instructions/data_storytelling.md` — narrative and dashboard communication standard.

## Worked Examples

- `specs/0008-metrics-semantic-layer/` — the metrics layer as a spec-driven,
  test-backed runtime workflow.
- `specs/0009-experimentation/` — disciplined A/B test design and readout
  (`src/quantsmith/pipelines/experimentation.py`).
