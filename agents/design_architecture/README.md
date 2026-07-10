# Design & Architecture Agent

## Purpose

The Design & Architecture Agent covers the second stage of the development
lifecycle. It turns approved requirements into a design: interfaces, data flow,
component boundaries, validation strategy, and the trade-offs behind each choice.

For quant work this includes experiment and pipeline design, feature and label
definitions, model validation scheme, and how the deliverable will be tested,
deployed, and monitored later.

## Use When

- Requirements are agreed and the team needs a design before coding.
- A change spans multiple components, datasets, or services.
- There are competing approaches and the trade-offs need to be written down.
- Reviewers need to see interfaces and failure modes before implementation.

## Inputs

- Approved requirements and acceptance criteria.
- Existing architecture, datasets, and interfaces the change touches.
- Constraints: latency, cost, capacity, compliance, reproducibility.
- Known risks, prior incidents, or fragile areas.

## Outputs

- Design overview and component diagram (described in text).
- Interfaces, data contracts, and data flow.
- Validation and testing strategy.
- Trade-off analysis with rejected alternatives.
- Rollout, observability, and rollback considerations.

## Example Requests

- "Design the pipeline for this feature set and name the data contracts."
- "Compare two model-serving approaches and recommend one with trade-offs."
- "Propose the validation scheme and how we detect drift after launch."

## Required Review Themes

- Fit between design and stated requirements.
- Interface and data-contract clarity.
- Time alignment, leakage, and reproducibility by construction.
- Failure modes, rollback, and observability.
- Trade-offs and explicitly rejected alternatives.
