# Plan: Asset Class Mechanics Agent Expansion

- **Spec:** 0022-asset-class-mechanics-agents (`spec.md`)
- **Status:** Approved
- **Author:** Claude
- **Last updated:** 2026-08-09

## Approach

Create one category folder, `agents/asset_classes/`, with a group README plus five
narrow four-file public agents (`equities/`, `fixed_income_rates/`, `fx/`,
`commodities/`, `digital_assets/`). Add the backing instruction standard
`instructions/asset_class_mechanics.md`. Update the agent catalog, spec index, and
top-level README so the group is discoverable and routable alongside
`trading_strategies/` and `securities_financing/`.

## Architecture & Components

```text
quant_analyst (router) / workflow_orchestrator
  -> asset_classes/<class>          # market-structure & data mechanics, point-in-time
       -> trading_strategies/<archetype>   # strategy design & review
       -> securities_financing/<agent>     # financing pricing (shorts, repo, collateral)
       -> data_quality | risk               # lineage/quality and exposure review
  -> lifecycle agents: planning_requirements -> design_architecture ->
     implementation -> testing_validation
  -> spec artifacts under specs/NNNN-slug/
  -> runtime code under src/quantsmith/ only if a future spec needs it
```

## Interfaces & Data Contracts

The new files are Markdown contracts only. Each agent's inputs/outputs are
agent-level control context: instrument/venue descriptions, price/curve/rating
series and their conventions, and point-in-time snapshot dates. No runtime schema
or provider API is introduced in this slice.

## Constitution Check

| Principle | Upheld? | Notes |
| --- | --- | --- |
| P3 Point-in-time | yes | Every agent's core job is point-in-time treatment of conventions, curves, ratings, and universe membership. |
| P4 Correct by construction | yes | Mechanics-only scope prevents the group from making unreviewed strategy or financing calls. |
| P5 Reversibility | yes | Changes are docs/contracts only and isolated on a branch. |
| P9 Security & data | yes | Contracts prohibit credentials, private data, client identifiers, and MNPI (inherited from the constitution; no new exception needed). |

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | `agents/asset_classes/README.md` | T-001 |
| REQ-002 | `agents/asset_classes/{equities,fixed_income_rates,fx,commodities,digital_assets}/` | T-001 |
| REQ-003 | `instructions/asset_class_mechanics.md` | T-002 |
| REQ-004 | `agents/README.md`, `specs/README.md`, top-level `README.md` updates | T-003 |
| NFR-001 | Four-file contract per agent, `Spec-Driven Role` section | T-001, T-004 |
| NFR-002 | Validation gates | T-004 |
| NFR-003 | Explicit scope-boundary language in each `instructions.md` | T-001 |

## Trade-offs & Alternatives

| Decision | Chosen | Rejected alternative | Why |
| --- | --- | --- | --- |
| Organize by asset class as a new group | Separate `agents/asset_classes/` category | Add asset-class sections inside each `trading_strategies/` archetype | Would duplicate mechanics guidance across 8 archetype agents instead of once per class; the group README documents the intended handoff instead. |
| Fixed income scope | One combined `fixed_income_rates/` agent (bonds, rates, credit) | Separate rates and credit agents | Curve, day-count, and rating conventions are closely coupled; splitting them would fragment one coherent mechanics review. |
| Runtime scope | Contracts and docs only | Add a mechanics runtime helper now (e.g. adjuster, curve builder) | No concrete workflow yet needs one; premature runtime code without a driving spec/use case. |
| Taxonomy breadth | Five asset classes (equities, fixed income/rates/credit, FX, commodities, digital assets) | Cover every instrument type (options, private markets, structured products, …) | Matches the existing `trading_strategies/` archetype taxonomy's stated approach: judgment-based coverage, extended when a class's mechanics are genuinely distinct. |

## Validation Strategy

Run `hooks/stages/run-stage.sh spec agent-catalog docs-link spec-index`, plus
`git diff --check` for whitespace, and confirm all four contract files exist for
each of the five new agents. AC-001 is covered by `agent-catalog`. AC-002 is
covered by direct inspection of each `instructions.md`'s `Spec-Driven Role`
section. AC-003 is covered by `spec-index`. AC-004 is covered by `spec` and
`docs-link`.

## Rollout, Observability & Rollback

Rollout is a branch commit (and push, if requested). Rollback is reverting the
single docs/contracts commit. A future runtime spec can add mechanics helpers
(corporate-action adjuster, point-in-time curve builder, funding-rate series
builder) under `src/quantsmith/` once a concrete workflow needs one, following the
`0006`/`0007` pattern of promoting an agent-contract group into a tested runtime.

## Open Questions

- Which mechanics runtime helper, if any, gets built first once a concrete
  workflow needs one: corporate-action adjuster, point-in-time curve builder, or
  perpetual-funding-rate series builder?
