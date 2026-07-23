# Quant Research Instructions

## Purpose

Use this instruction set when planning, reviewing, or documenting a quant research workflow. The goal is to move from idea to evidence without hiding assumptions, data risk, or validation gaps.

## Required Inputs

- Research question or hypothesis.
- Target universe or population.
- Intended decision, forecast, signal, or model output.
- Candidate data sources.
- Time horizon and evaluation window.
- Constraints such as turnover, capacity, latency, explainability, or operational limits.

## Expected Output

- Testable hypothesis.
- Research plan.
- Assumption log.
- Data requirements.
- Experiment design.
- Metrics and benchmarks.
- Validation and robustness plan.
- Handoff notes.

## Standards

- State the economic, behavioral, structural, or domain rationale.
- Define the unit of observation and decision time.
- Identify all data sources and their point-in-time availability.
- Include a simple baseline before complex methods.
- Match metrics to the intended decision.
- Define acceptance criteria before inspecting final results when possible.
- Separate exploration, model selection, validation, and final reporting.
- Record negative or inconclusive results when they affect future research.

## Checks

- Is the hypothesis falsifiable?
- Is the target universe documented?
- Are data sources, date ranges, frequency, and refresh cadence documented?
- Are labels and features defined at the correct decision time?
- Is there a benchmark or baseline?
- Are leakage, survivorship, and overfitting risks surfaced?
- Can another researcher reproduce the experiment from documented code, data versions, and configuration?

## Common Failure Modes

- Choosing metrics after seeing results.
- Treating exploratory notebook output as final evidence.
- Ignoring data availability time.
- Comparing against a weak or mismatched benchmark.
- Reusing validation results across many undocumented parameter searches.
- Failing to document why an idea was stopped.

## Spec-Driven Alignment

This standard backs the Specify and Plan steps (see
`instructions/spec_driven_development.md`). The hypothesis and rationale become
`REQ-*`; the evaluation metrics, baselines, and pre-registered success thresholds
become testable `AC-*`/`NFR-*`; leakage, survivorship, and overfitting risks
become `RISK-*`. Defining acceptance criteria before inspecting results is
constitution P3 (Definition of Done is explicit and testable); reproducibility is
P4. Point-in-time rules live in `instructions/point_in_time.md`.
