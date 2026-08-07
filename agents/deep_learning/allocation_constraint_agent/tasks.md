# Allocation Constraint Agent Tasks

## Standard Tasks

1. Define allowed positions and portfolio-total constraint.
2. Select softmax, projection, optimizer, or control-layer enforcement.
3. Map every business constraint to an enforcement point.
4. Test feasibility under normal and edge-case universes.
5. Measure how constraint handling changes objective and turnover.
6. Produce tests for executable weight outputs.

## Evidence to Collect

- Constraint table.
- Example raw outputs and transformed weights.
- Feasibility tests.
- Objective-drift analysis after constraints.
- Edge-case handling notes.

## Red Flags

- Softmax used as a substitute for all risk controls.
- Ineligible assets receive nonzero weights.
- Projection step silently changes model intent.
- Constraints described verbally but not tested.
