# Spec-Driven Development

Spec-Driven Development (SDD) is the operating model of the QF Workflow SDK. The
specification is the source of truth; every other artifact is derived from it and
traces back to it. This document defines the workflow, the artifacts, the
identifier scheme, and the gates that hold between stages.

Read `instructions/engineering_principles.md` (the constitution) first — SDD is
how those principles are enforced in practice.

## The Flow

```
Constitution
     │
     ▼
 Specify ──▶ Plan ──▶ Tasks ──▶ Implement ──▶ Verify ──▶ Operate
 (WHAT/WHY) (HOW)   (WORK)    (CODE)        (EVIDENCE) (LIVE)
```

Each step maps to a development stage and its companion agent and hook:

| Step | Stage | Artifact | Agent | Hook |
| --- | --- | --- | --- | --- |
| Specify | 1. Planning / Requirements | `spec.md` | `planning_requirements` | `planning-check` |
| Plan | 2. Design | `plan.md` | `design_architecture` | `design-check` |
| Tasks + Implement | 3. Coding / Implementation | `tasks.md` + code | `implementation` | `implementation-check` |
| Verify | 4. Testing | tests + evidence | `testing_validation` | `testing-check` |
| Operate (release) | 5. Deployment | release record | `deployment_release` | `deployment-check` |
| Operate (run) | 6. Maintenance | living spec | `maintenance_monitoring` | `maintenance-check` |

The cross-cutting `spec-check` hook validates the chain and traceability at every
step.

## Where Specs Live

Each unit of work gets a directory:

```
specs/
  NNNN-short-slug/
    spec.md    # WHAT and WHY  — requirements, acceptance criteria, non-goals
    plan.md    # HOW           — architecture, data contracts, trade-offs
    tasks.md   # WORK          — ordered, traceable, testable tasks
```

`NNNN` is a zero-padded sequence number; the slug is a short kebab-case name.
Templates live in `templates/spec/`.

## Identifier Scheme

Stable IDs are what make traceability mechanical. Once assigned, an ID is never
reused or renumbered.

| Prefix | Meaning | Defined in |
| --- | --- | --- |
| `REQ-NNN` | Functional requirement | `spec.md` |
| `NFR-NNN` | Non-functional requirement (latency, cost, capacity, compliance) | `spec.md` |
| `AC-NNN` | Acceptance criterion (testable) | `spec.md` |
| `RISK-NNN` | Identified risk | `spec.md` / `plan.md` |
| `T-NNN` | Implementation task | `tasks.md` |

- Every `AC-*` belongs to a `REQ-*` or `NFR-*`.
- Every `T-*` references at least one `REQ-*`/`NFR-*` it advances.
- Every `AC-*` is covered by at least one test that names it.

## Traceability Rules (enforced)

1. **No plan without an approved spec.** `plan.md` requires a `spec.md`.
2. **No task without a requirement.** Every `T-*` cites a `REQ-*`/`NFR-*`.
3. **No requirement without coverage.** Every `REQ-*`/`NFR-*` maps to at least one
   `T-*` (in `plan.md`'s traceability matrix).
4. **No acceptance criterion without a test.** Every `AC-*` is referenced by a
   test (by ID, e.g. in a test name, docstring, or assertion message).
5. **No orphans.** A `T-*` citing no requirement, or a `REQ-*` with no task, fails
   the gate.
6. **Constitution holds.** No open, un-exception'd violation of a principle in
   `instructions/engineering_principles.md`.

The `spec-check` hook checks rules 1–3 and 5 structurally, and flags missing
`AC-*` test references for rule 4. Reviewers own the judgement calls.

## Stage Gates

A stage is complete only when its exit gate passes:

- **Specify → Plan:** `spec.md` has requirements with IDs, testable `AC-*`, and a
  non-goals section; it is approved.
- **Plan → Tasks:** `plan.md` maps every `REQ-*`/`NFR-*` to a design element and
  records trade-offs; every requirement appears in the traceability matrix.
- **Tasks → Implement:** every `T-*` links to a requirement and has a Definition
  of Done.
- **Implement → Verify:** code exists for the tasks; reproducibility notes present.
- **Verify → Release:** every `AC-*` has passing, deterministic evidence; every
  `NFR-*` is checked.
- **Release → Operate:** rollback path, monitoring, and owner are defined.

## Changing a Live Spec

Live systems have living specs. A change to production behavior starts by amending
the `spec.md` (new or revised `REQ-*`/`AC-*`), then flows through the same gates.
Never patch code ahead of its spec; that breaks P1 and P2.

## Minimal vs Full

Not every change needs a full three-document spec. Use judgement:

- **Trivial** (typo, comment, config bump): no spec dir; note in the commit.
- **Standard** feature or fix: `spec.md` + `tasks.md`; inline the plan if small.
- **Significant** or risky change: full `spec.md` + `plan.md` + `tasks.md`.

When in doubt, write the spec. The cost of a short spec is minutes; the cost of an
undocumented assumption in a live quant system is not.
