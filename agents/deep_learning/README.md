# Deep Learning Agents

The Deep Learning group covers neural architectures, training systems, transformers, GNNs, RL, generative models, embeddings, and production serving.

## Group Workflow

```text
dl_orchestrator -> training_systems -> specialist DL agent -> compression_serving -> model_selection_validation/mlops_monitoring
```

For neural portfolio work, route through the general DL workflow first, then add the portfolio-specific review loop:

```text
dl_orchestrator -> deep_portfolio_optimization -> portfolio_volatility_costs -> portfolio_stress_explainability -> backtest_review/risk
```

## Agents

| Agent | Handles |
| --- | --- |
| `dl_orchestrator/` | Routes deep-learning work across architecture, data, training, evaluation, compression, serving, and monitoring. |
| `training_systems/` | Owns data loaders, distributed training, mixed precision, checkpointing, determinism, accelerators, and cost controls. |
| `neural_tabular/` | Covers tabular neural nets, embeddings, categorical features, calibration, baselines, and tabular-vs-tree trade-offs. |
| `sequence_transformers/` | Designs temporal, transformer, attention, and sequence models for markets, logs, language, and operational streams. |
| `graph_neural_networks/` | Handles GNNs for networks, collateral chains, counterparties, supply graphs, ownership graphs, and message passing. |
| `reinforcement_learning/` | Covers MDP framing, reward design, simulators, offline RL, policy constraints, safety, and evaluation before live use. |
| `computer_vision/` | Handles image/document/screenshot models, OCR-adjacent workflows, augmentation, labeling, and visual quality checks. |
| `nlp_llm/` | Covers text classification, retrieval, embeddings, reranking, prompt/eval design, RAG boundaries, and LLM risk controls. |
| `representation_metric_learning/` | Designs embeddings, contrastive learning, similarity search, clustering, and representation evaluation. |
| `generative_models/` | Covers diffusion, VAEs, GANs, synthetic data, scenario generation, augmentation, and privacy/risk limits. |
| `deep_time_series/` | Handles deep forecasting, temporal fusion, sequence-to-sequence models, regime conditioning, and probabilistic forecasts. |
| `compression_serving/` | Owns distillation, quantization, pruning, batching, latency, memory, GPU utilization, and serving contracts. |
| `deep_portfolio_optimization/` | Designs direct neural allocation systems that optimize portfolio-level objectives instead of proxy prediction losses. |
| `portfolio_volatility_costs/` | Reviews volatility targeting, turnover, scaled positions, and transaction-cost robustness for neural portfolio strategies. |
| `portfolio_stress_explainability/` | Explains neural allocation behavior across stress windows using weights, scaled exposure, returns, and feature attribution. |

## Inputs

- Current `spec.md`, `plan.md`, `tasks.md`, or handoff memo when available.
- Business decision, objective, constraints, and risk limits.
- Data contracts, source provenance, point-in-time assumptions, and refresh cadence.
- Runtime expectations for `src/quantsmith/`, notebooks, adapters, or downstream systems.

## Outputs

- Specialist routing plan.
- Spec-ready requirements, risks, acceptance criteria, and task suggestions.
- Method, baseline, validation, monitoring, and deployment recommendations.
- Handoffs to lifecycle agents, data agents, risk, testing, reporting, and adapters.

## Rules

- Keep each specialist narrow and inspectable.
- Promote broad or risky work into `specs/NNNN-slug/` before implementation.
- Use adapters for provider/runtime boundaries and `src/quantsmith/` for executable code.
- Treat this group as decision support and workflow design unless a spec authorizes implementation.
