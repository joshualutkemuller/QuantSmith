# Deep Learning Instructions

## Purpose

Use this standard when designing, reviewing, or operating neural-network systems, including transformers, graph neural networks, reinforcement learning, generative models, computer vision, NLP/LLM systems, and deep time-series models.

## Required Inputs

- Model purpose, data modality, labels/rewards, deployment action, and baseline.
- Dataset scale, sampling plan, train/validation/test split, and leakage controls.
- Architecture candidates, training budget, hardware, reproducibility constraints, and serving limits.
- Evaluation metrics, stress tests, safety constraints, and monitoring plan.

## Standards

- Justify deep learning against simpler baselines; complexity must buy measurable value.
- Make training reproducible enough to review: data snapshot, seed strategy, code version, checkpoint, config, hardware, and environment.
- Track loss curves, validation curves, calibration, failure slices, and robustness tests.
- For RL, validate in simulation/offline settings before any live action and constrain policy behavior.
- For LLM/NLP and generative models, separate retrieval, generation, evaluation, safety review, and provenance.
- For production, define latency, memory, batching, fallback, rollback, and drift/quality monitoring.

## Common Failure Modes

- A large model beating no serious baseline.
- Training instability hidden by cherry-picked checkpoints.
- Data leakage through windowing, augmentation, document overlap, or benchmark contamination.
- Reward hacking or simulator overfit in reinforcement learning.
- Serving costs, memory, and latency discovered only after the model is selected.

## Spec-Driven Alignment

Deep learning work maps architecture purpose, modality, and action space to `REQ-*`; training cost, latency, hardware, reproducibility, and safety constraints to `NFR-*`; benchmark lift, robustness, calibration, and serving evidence to `AC-*`; and instability, data contamination, reward hacking, hallucination, privacy, and cost overrun to `RISK-*`.
