# Engineering Principles (Constitution)

These are the non-negotiable engineering rules for work done with the QF Workflow
SDK. They are the constitution: every specification, plan, task, and review is
checked against them. A change that violates a principle must either be brought
into compliance or carry an explicit, approved, time-bound exception recorded in
the relevant `spec.md`.

The principles are deliberately few and strict. Add project-specific rules in a
downstream copy; do not weaken these.

## P1. The spec is the source of truth

Behavior is defined by the specification, not by the code. Code, tests, and docs
serve the spec. When code and spec disagree, one of them is a defect — decide
which and fix it. No feature work begins without an approved `spec.md`.

## P2. Everything traces to a requirement

Every design decision, task, test, and line of production behavior traces to a
requirement (`REQ-*`) or acceptance criterion (`AC-*`). Orphan work (code with no
requirement) and orphan requirements (a requirement with no task or test) are
both defects. Traceability is enforced, not aspirational.

## P3. Definition of Done is explicit and testable

"Done" means every acceptance criterion has passing, deterministic evidence and
every non-functional requirement (`NFR-*`) has been checked. A criterion that
cannot be tested is not an acceptance criterion — it is an open question.

## P4. Correct by construction

Prefer designs that make defects impossible over checks that detect them later.
For quant and data work this specifically means: no look-ahead, no leakage, and
reproducible-by-default data and feature paths. Reproducibility (pinned inputs,
seeded randomness, no hidden state) is a requirement, not a nicety.

## P5. Reversibility and blast-radius control

Anything that ships must be reversible. Every release has a rollback path and,
where it trades or serves, a kill switch. Match rollout caution to blast radius.
Irreversible actions require explicit sign-off recorded in the spec.

## P6. Observability is part of the feature

A feature is not done until you can tell whether it is working in production.
Monitoring, alert thresholds, and an owner are defined before launch, not after.

## P7. Small, reviewable changes

Prefer narrow changes that a reviewer can fully understand. Large or
architecturally significant changes are split, or their risk is documented in the
plan and approved before implementation.

## P8. No silent trade-offs

Every material trade-off is written down with the alternative that was rejected
and why. Hidden assumptions, undocumented shortcuts, and "temporary" workarounds
without a tracked follow-up are violations.

## P9. Security and data handling are first-class

Secrets, credentials, and private data never enter the repository, logs, or
notebook outputs. Data lineage and access constraints are stated in the spec and
respected in the plan.

## P10. Honest reporting

Status reflects reality. If tests fail, say so. If a criterion is unmet, it is
not done. Confidence is stated with evidence; uncertainty is stated plainly.

## Exceptions

An exception to any principle must be recorded in the owning `spec.md` under an
`Exceptions` heading with: the principle, the reason, the risk accepted, the
approver, and an expiry date or removal condition. Undocumented exceptions do not
exist and should be treated as defects in review.
