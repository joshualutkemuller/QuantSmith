# `app/` — QuantForge

**QuantForge** is a native iOS monitoring companion built on QuantSmith's
existing runtimes, and will live in its **own repository** of that name.
This directory is its design surface: the handoff, the architecture
decision, and the phase breakdown, so the work can start from a settled
scope rather than a conversation. Nothing is built yet.

QuantSmith remains the source of the contracts and computed outputs
QuantForge renders; spec `0047` is what lets the two repositories move
independently without silently breaking each other.

## Status

| Phase | Scope | Status |
| --- | --- | --- |
| 0 | Web-first validation (Streamlit, already scaffoldable) | **recommended first**, not started |
| 1 | `swiftui_profile` + `swiftui_scaffold` — an 8th `DashboardSpec` target | not started |
| 2 | A read API exposing pipeline outputs as JSON | **blocked on a decision**, see `decision_log.md` |
| 3 | SwiftUI client + APNs alert provider | not started, depends on 1 and 2 |

## What this is, and is not

**Is:** a read-only monitoring companion — macro indicators and regime,
a portfolio risk snapshot, backtest results, and alerts.

**Is not:** "QuantSmith on a phone." The bulk of the SDK — 161 agent
contracts, 27 quality gates, the spec-driven workflow, git hooks, CI —
is developer tooling that operates on a repository. There is no iPhone
analogue for `run-stage.sh` or authoring a `spec.md`, and porting it
would build something nobody wants. That boundary is argued in full in
[`handoff.md`](handoff.md).

## Files

- [`handoff.md`](handoff.md) — the comprehensive handoff: context, what
  translates, phase-by-phase scope, risks, and definition of done.
- [`decision_log.md`](decision_log.md) — the material architectural
  decision this initiative forces (whether the SDK starts owning a
  running service) and the two decisions already settled.

## Relationship to `specs/`

This directory holds the **initiative-level** design. Each phase becomes
an ordinary numbered spec under [`../specs/`](../specs/) when it is
built, following the repository's normal
`specs/NNNN-slug/{spec,plan,tasks}.md` convention and its gates. Nothing
here bypasses that; this is the document that says what those specs
should contain and in what order.
