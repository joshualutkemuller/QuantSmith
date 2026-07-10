# Planning & Requirements Analysis Instructions

## Operating Rules

- Restate the request in one sentence before decomposing it.
- Separate the research question from the engineering requirement.
- Write every requirement so it can be verified or tested.
- Mark each requirement as must-have, should-have, or nice-to-have.
- State what is explicitly out of scope; silence is not a boundary.
- Capture data, latency, cost, capacity, and compliance constraints early.
- Never invent facts to fill gaps; record them as open questions.

## Checks

- Is the problem statement specific and tied to a decision or use case?
- Does each requirement have a clear acceptance test?
- Are non-functional requirements captured, not just functional ones?
- Are dependencies and upstream owners identified?
- Are assumptions and open questions listed with owners where possible?
- Is there a defined, measurable definition of done?

## Output Contract

Use clear Markdown sections. Always include a final `Open Questions` section and
a final `Acceptance Criteria` section. When the work affects trading, data, or
compliance, include a `Constraints & Risks` section.
