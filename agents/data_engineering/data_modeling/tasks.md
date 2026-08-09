# Data Modeling Tasks

## Design

Input: the sources, targets, and grain in scope.

Output: a reviewed design with explicit data contracts, keys, ownership, and trade-offs.

## Review

Input: an existing design or pipeline artifact.

Output: a review against contracts, grain, point-in-time correctness, and ownership,
with concrete fixes.

## Promote To A Spec

Input: an approved design.

Output: spec-ready requirements, risks, and acceptance criteria for `specs/NNNN-slug/`.

## Hand Off

Input: a completed design.

Output: a handoff to `pipeline_orchestration`, `data_quality`, and `analytics/metrics_semantic_layer` with the contracts and open questions.
