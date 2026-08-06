# Orchestrator Agent Tasks

## Plan A Request

Input: a natural-language analytics request.

Output: parsed objectives and a dependency-ordered plan across specialist agents.

## Delegate Subtasks

Input: the plan and the specialist agents' contracts.

Output: typed subtask delegations with tracked status.

## Handle Failures

Input: a failed or retried subtask.

Output: the failure cause and a retry or fallback decision.

## Assemble Summary

Input: completed subtask artifacts.

Output: a terminal-ready summary of deliverables and next actions.
