# Workflow Orchestrator Tasks

## Locate & Route

Input: a request or an in-progress change and its spec state.

Output: current lifecycle position, the next gate, and which stage agent to
invoke next with what inputs.

## Gate Assessment

Input: the current stage and its artifacts.

Output: whether the exit gate is satisfied, with evidence; if not, the single
missing item and its owner.

## Coordinate Handoff

Input: a completed stage and the next stage.

Output: a handoff package giving the next agent exactly the inputs it needs, plus
the spec chain status.

## Unblock A Stuck Change

Input: a change that is not progressing.

Output: the specific gate that is blocking, the owner, and the minimal path to
clear it.

## Lifecycle Status Report

Input: one or more active changes.

Output: for each, its lifecycle position, gate status, and next action — a
single-glance view of where everything stands.
