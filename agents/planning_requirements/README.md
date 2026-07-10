# Planning & Requirements Analysis Agent

## Purpose

The Planning & Requirements Analysis Agent covers the first stage of the
development lifecycle. It turns a request, hypothesis, or business problem into
clear, testable requirements, scope boundaries, and success criteria before any
design or code work begins.

For quant work this means separating the research question from the engineering
requirement, identifying the data and constraints the work depends on, and
capturing the decisions the deliverable must support.

## Use When

- A stakeholder request is vague, verbal, or captured only in a ticket title.
- A research idea needs to become a scoped, reviewable requirement.
- The team disagrees on what "done" means for a signal, model, or pipeline.
- Non-functional needs (latency, capacity, cost, compliance) are unstated.

## Inputs

- Problem statement, hypothesis, or stakeholder request.
- Intended decision or use case the deliverable supports.
- Known constraints: data availability, latency, cost, capacity, compliance.
- Existing systems, datasets, or prior work the change touches.

## Outputs

- Requirements list (functional and non-functional).
- Scope and explicit out-of-scope statement.
- Assumptions and open questions.
- Acceptance criteria and success metrics.
- Stakeholders, dependencies, and risks.

## Example Requests

- "Turn this Slack thread into a scoped requirements doc with acceptance criteria."
- "List the functional and non-functional requirements for this forecast service."
- "Identify the open questions and dependencies before we start designing."

## Required Review Themes

- Problem clarity and measurable success criteria.
- In-scope vs out-of-scope boundaries.
- Data, latency, cost, and compliance constraints.
- Dependencies, stakeholders, and sign-off owners.
- Assumptions and unresolved questions.
