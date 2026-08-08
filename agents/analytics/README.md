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
```

## Agents

| Agent | Handles |
| --- | --- |
| `metrics_semantic_layer/` | Canonical KPI/metric definitions — one source of truth per metric, consistent point-in-time computation, declared dimensions, and derived (ratio) metrics. |
| `experimentation/` | A/B test design and readout — power/sample-size, sample-ratio-mismatch validity, p-value/CI consistency, and a power-gated verdict. |

## Rules

- Keep each specialist narrow and inspectable.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.
- A metric is defined once; consumers (dashboards, reports) read the definition, they
  do not redefine it.
- Runtime Python belongs under `src/quantsmith/` (the semantic-layer evaluator lives
  at `src/quantsmith/pipelines/metrics_semantic_layer.py`); agent directories describe
  roles, prompts, instructions, and tasks.

## Standards

- `instructions/metrics_semantic_layer.md` — how to define and govern metrics.
- `instructions/model_validation.md` — validation discipline behind experiment readouts.

## Worked Examples

- `specs/0008-metrics-semantic-layer/` — the metrics layer as a spec-driven,
  test-backed runtime workflow.
- `specs/0009-experimentation/` — disciplined A/B test design and readout
  (`src/quantsmith/pipelines/experimentation.py`).
