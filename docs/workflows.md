# Workflow Map

The single place to see how the SDK's agents, gates, and instructions compose into
end-to-end workflows. It does not replace the flow definitions it links to — it
unifies them and adds role-based and scenario workflows.

## The Backbone: Spec-Driven Development

Every workflow runs on top of the SDD lifecycle (the canonical map lives in
`instructions/spec_driven_development.md`):

```
Constitution → Specify → Plan → Tasks → Implement → Verify → Operate
```

Each step has an owning stage agent and a companion gate:

| Step | Stage agent | Gate |
| --- | --- | --- |
| Specify | `planning_requirements` | `planning`, `spec` |
| Plan | `design_architecture` | `design`, `spec` |
| Tasks + Implement | `implementation` | `implementation`, `leakage`, `secret-scan` |
| Verify | `testing_validation` | `testing`, `backtest` |
| Operate (release) | `deployment_release` | `deployment` |
| Operate (run) | `maintenance_monitoring` | `maintenance` |

The `workflow_orchestrator` agent drives this flow and enforces the gate between
stages. Agents marked **(planned)** below are on the roadmap — see
`docs/handoffs/future_features.md`.

## Role & Scenario Workflows

Each workflow is an ordered chain of agents plus the gates that check the work. They
all sit on the SDD backbone above.

### Quant Researcher

Idea → reviewed, reproducible, risk-checked signal or model.

```
research_analyst → data_quality → feature_engineering → modeling
  → backtest_review → risk → git_release
```

- Standard: `instructions/quant_research.md`, `instructions/model_development.md`.
- Gates: `leakage`, `backtest`, `repro`, `spec`.
- Strategy/alpha variants slot in `trading_strategies/*` or `formulaic_alphas/*`
  between `research_analyst` and `modeling`.

### Quant Model Build

Approved design → reproducible, validatable model implementation.

```
design_architecture (plan) → implementation (build) → testing_validation (verify)
```

- Standard: `instructions/model_development.md` (how to build) +
  `instructions/model_validation.md` (how to validate).
- Gates: `implementation`, `leakage`, `repro`, `testing`, `backtest`.
- Reproducibility is captured in a run card (`templates/docs/run_card.md`).

### Data Analyst

Business question → validated, communicated answer.

```
planning_requirements → sql-integration-agent → eda-specialist-agent
  → metrics_semantic_layer (planned) → tooling/tableau | tooling/power_bi
  → quality-guard-agent → reporting-agent
```

- Experimentation/A-B work uses `experimentation` (planned).
- Gates: `data-contract`, `secret-scan`.

### Data Engineer

Source → modeled, orchestrated, monitored, contract-backed data.

```
data_ingestion/* (or sql-integration-agent) → data_modeling (planned)
  → data-prep-agent → pipeline_orchestration (planned)
  → data_quality + quality-guard-agent → pipeline_observability (planned)
```

- Standard: `instructions/data_quality.md`, `templates/data/data_contract.md`.
- Gates: `data-contract`, `repro`, `secret-scan`.
- Secrets/access via `secrets_management/*`.

### Analytics Pipeline (runtime)

The consolidated multi-agent analytics copilot (full blueprint in
`agents/agentic_workflow_blueprint.md`):

```
orchestrator-agent → sql-integration-agent → data-prep-agent
  → eda-specialist-agent → tableau-dashboard-agent | powerbi-dashboard-agent
  → quality-guard-agent → reporting-agent
```

### Persistent Workflow Memory (cross-cutting)

Each workflow primes from and writes back to `memory/` so it arrives already knowing
a dataset's kinks. Facts about a source live in `memory/_shared/`; workflow-specific
usage in `memory/<workflow>/`.

- Standard: `instructions/workflow_memory.md`; design: `specs/0002-workflow-memory/`.
- Served by the `knowledge/` agents; gate: `memory`. Research runs use only
  point-in-time-scoped records (leakage firewall).

### Knowledge & Institutional Memory (cross-cutting)

```
knowledge/knowledge_ingestion → knowledge/knowledge_curation
  → knowledge/knowledge_retrieval ; knowledge/institutional_memory (persist)
```

- Standard: `instructions/knowledge_base.md`; sources in `knowledge_sources.yml`.
- Gate: `knowledge`.

## Related Maps

- `instructions/spec_driven_development.md` — the SDD lifecycle (the backbone).
- `agents/README.md` — the agent catalog and "How They Fit Together".
- `agents/agentic_workflow_blueprint.md` — the analytics-pipeline blueprint.
- `README.md` — the "Suggested Quant Workflow" narrative.

## Composing A Role Agent

To build (or "convert") an agent that performs a role, compose the chain above from
the listed agents, apply their backing instructions, and run the named gates as the
definition of done. Where a step names a **(planned)** agent, that capability is
tracked in `docs/handoffs/future_features.md`.
