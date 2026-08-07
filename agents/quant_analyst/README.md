# Quant Analyst Agent

The Quant Analyst Agent turns a quant research, portfolio construction,
securities financing, or model-monitoring request into an executable,
reviewable workflow plan.

This directory is the **agent contract**. Runtime code belongs in the package:

- `src/quantsmith/quant/agentic_quant/` — blackboard pipeline, quant agents,
  securities lending workflow, ML workflow, and CLI modules.
- `src/quantsmith/quant/mean_variance.py` — mean-variance optimizer.
- `src/quantsmith/quant/agentic_quant/README.md` — runtime usage notes.

Legacy wrappers remain here for now so older commands still work:

- `python agents/quant_analyst/run_sec_lending.py`
- `python agents/quant_analyst/run_rebalancer.py`
- `python agents/quant_analyst/run_sp500.py`

Prefer the packaged entry points in new work:

```bash
python -m quantsmith.quant.agentic_quant
quantsmith-sec-lending
quantsmith-rebalancer
quantsmith-sp500
```

## Role

Use this agent when a request needs quantitative workflow judgment rather than a
single narrow review. It composes research, data ingestion, feature engineering,
modeling, trading strategy, securities financing, backtest review, and risk
agents into a coherent plan or executable prototype.

## Inputs

- Research question, production request, or workflow goal.
- Universe, horizon, data sources, constraints, and intended decision.
- Existing specs, notebooks, code paths, run cards, model cards, or reports.
- Risk limits, financing assumptions, operational constraints, and review gates.

## Outputs

- Workflow decomposition and agent routing.
- Data, feature, model, backtest, financing, and risk assumptions.
- Runnable package entry point or implementation handoff when code exists.
- Acceptance criteria and validation gates.
- Explicit open questions, stop conditions, and next actions.

## Boundaries

- Do not store executable runtime modules directly in this agent directory.
- Do not bypass `specs/` for implementation-grade work.
- Do not claim performance, alpha, or production readiness without evidence.
- Do not embed secrets, MNPI, client identifiers, or proprietary desk context.

## Runtime Handoff

When implementation is required, hand off to the packaged runtime under `src/`
or create a numbered spec under `specs/NNNN-slug/`. The agent directory should
stay a catalog and contract surface, not the long-term home for Python modules.
