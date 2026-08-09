# Spec: Asset Class Mechanics Agent Expansion

- **ID:** 0022-asset-class-mechanics-agents
- **Status:** Approved
- **Author:** Claude
- **Approver:** Josh
- **Last updated:** 2026-08-09

## Problem & Context

The `agents/quant_analyst/` router and `agents/trading_strategies/` archetypes are
asset-class-agnostic by design: an archetype like `momentum_trend/` spans equities,
futures, FX, and commodities in one agent, and `quant_analyst/` composes agents
into a workflow plan without naming asset-class mechanics. That is a deliberate
choice (see `agents/trading_strategies/README.md`, "Note On Scope") to avoid
duplicating archetype review logic per market. But it leaves a real gap: equities,
fixed income/rates/credit, FX, commodities, and digital assets each have
market-structure and data mechanics — settlement conventions, corporate actions,
curve construction, roll, custody — that are genuinely different across classes and
are a documented leakage/bias surface in the constitution and
`instructions/point_in_time.md`. No agent currently owns that mechanics layer.

## Goals

- Add a new `agents/asset_classes/` category folder with one narrow, mechanics-only
  agent per covered asset class: equities, fixed income/rates/credit, FX,
  commodities, digital assets.
- Keep each agent scoped to market structure and data mechanics — settlement,
  sessions, conventions, corporate actions/roll, curve/rating construction, custody
  — and explicitly out of strategy design (owned by `trading_strategies/`) and
  financing pricing (owned by `securities_financing/`).
- Add a backing instruction standard, `instructions/asset_class_mechanics.md`.
- Update the agent catalog, spec index, and top-level README so the group is
  discoverable and routable.

## Non-Goals

- No runtime code or executable pipeline in this slice; agent contracts and docs
  only, consistent with the group's mechanics-brief output (Markdown, not code).
- No new strategy-archetype coverage; `trading_strategies/` is unchanged.
- No live market-data or vendor integrations; conventions and mechanics are
  documented guidance, not a pricing/data service.
- No exhaustive instrument taxonomy; five asset classes are covered by
  design judgment, not every possible instrument type (see the group's
  "Taxonomy Note").

## Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| REQ-001 | The system shall provide a `agents/asset_classes/` category folder with a group README describing scope and routing. | must |
| REQ-002 | The system shall provide one four-file agent per covered asset class (equities, fixed income/rates/credit, FX, commodities, digital assets), each scoped to market-structure/data mechanics and not to strategy design or financing pricing. | must |
| REQ-003 | The system shall provide a backing instruction standard, `instructions/asset_class_mechanics.md`, shared by the group. | must |
| REQ-004 | The agent catalog (`agents/README.md`), spec index (`specs/README.md`), and top-level `README.md` shall list the new group and its agents. | must |

## Non-Functional Requirements

| ID | Requirement | Target |
| --- | --- | --- |
| NFR-001 | Agent contract consistency | Every new public agent has `README.md`, `prompt.md`, `instructions.md`, and `tasks.md`, each with a `Spec-Driven Role` section in `instructions.md`. |
| NFR-002 | Repository hygiene | `agent-catalog`, `docs-link`, `spec`, `spec-index`, and whitespace checks pass. |
| NFR-003 | Scope boundary | Agent docs state explicitly that strategy design and financing pricing remain owned by `trading_strategies/` and `securities_financing/`, not duplicated here. |

## Acceptance Criteria

| ID | Given / When / Then | Covers |
| --- | --- | --- |
| AC-001 | Given the repo's agents directory, when the agent-catalog gate runs, then every new `agents/asset_classes/*` agent is listed in `agents/README.md`. | REQ-002, REQ-004, NFR-001 |
| AC-002 | Given the new agent contracts, when each `instructions.md` is read, then it names the mechanics-only scope and a handoff to `trading_strategies/` and/or `securities_financing/`. | REQ-002, NFR-003 |
| AC-003 | Given `specs/README.md`, when the spec-index gate runs, then `0022-asset-class-mechanics-agents` is checked against the index. | REQ-004, NFR-002 |
| AC-004 | Given the documentation set, when `docs-link` and `spec` gates run, then all new/changed docs pass with no broken links or traceability orphans. | NFR-002 |

## Data & Dependencies

No data dependencies. This slice creates agent contracts, an instruction standard,
and documentation updates only. A future implementation spec may add runtime
mechanics helpers (e.g. a corporate-action adjuster, a point-in-time curve
builder) under `src/quantsmith/` if a concrete workflow needs one.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| RISK-001 | The new group's scope overlaps with `trading_strategies/` or `securities_financing/`, causing duplicated or conflicting guidance. | Confusing routing; agents give inconsistent advice on the same concern. | Each agent's `instructions.md` states the mechanics-only boundary explicitly and names the downstream handoff instead of making strategy or financing calls. |
| RISK-002 | Five asset classes is an incomplete taxonomy (e.g. no dedicated credit-derivatives or private-markets agent). | A request outside the five classes has no clear owner. | The group README's "Taxonomy Note" states the scope is judgment-based and documents how to add a class when its mechanics are genuinely distinct. |
| RISK-003 | Docs imply live data/pricing capability that does not exist. | Users may expect an executable mechanics service. | State runtime implementation is out of scope in this slice; outputs are advisory briefs, not live data. |

## Assumptions & Open Questions

- Assumption: grouping by asset class (mechanics) rather than duplicating it inside
  each `trading_strategies/` archetype keeps both groups narrow and inspectable.
- Assumption: fixed income, rates, and credit share enough convention/curve
  machinery to be one agent rather than three.
- Open question: does digital assets eventually need a runtime helper (e.g. a
  perpetual-funding-rate point-in-time series builder) once a concrete workflow
  needs one?

## Exceptions

None.
