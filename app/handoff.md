# Handoff: QuantForge (iOS Companion)

- **Owner:** Josh
- **Author:** Claude
- **Status:** Design agreed, nothing built
- **Last updated:** 2026-08-12

> A comprehensive handoff for **QuantForge**, a native iOS companion over
> QuantSmith's computed outputs, planned as a separate repository. It states the scope, the boundary of what does and
> does not translate, the phase order, and the one architectural decision
> that must be settled before Phase 2 can start. Written to be actionable
> without re-deriving the reasoning from a conversation.

## 1. Context

QuantSmith is a spec-driven engineering scaffold: 161 agent contracts, 28
quality gates, 33 instruction standards, and a set of dependency-free
Python reference runtimes under `src/quantsmith/pipelines/`. It is
copied into quant repositories and driven by agents at development time.

The question this handoff answers is *"how does this become an iOS
app"* — and the honest answer begins with a subtraction.

## 2. The boundary: what does not translate

**Most of the SDK is not an app, and should not become one.**

| Surface | Why it does not translate |
| --- | --- |
| `agents/` (161 contracts) | Prompt/instruction contracts consumed by an agent runtime operating on a repository. A phone is not where they run. |
| `hooks/stages/` (28 gates) | Shell scripts that inspect a working tree and a git diff. No working tree on iOS. |
| `specs/`, spec-driven flow | Authoring and traceability of `REQ`/`AC`/`T` IDs — a desk activity, not a mobile one. |
| `.githooks/`, CI | Commit-time and merge-time enforcement. |
| `templates/`, `prompts/` | Source material for authoring, not for consumption on a phone. |

Attempting to port these would produce an app with no user. Recording
this explicitly matters because "turn the repo into an app" is the kind
of scope that expands silently if the exclusion is never written down.

## 3. What does translate

The **computed outputs**, not the machinery. Four candidate surfaces,
all read-only, each already produced by a shipped runtime:

| Surface | Source runtime | Spec |
| --- | --- | --- |
| Macro indicators, regime, curve spreads | `fred_point_in_time.py` + the `economists/` agent chain | `0045`, `0033` |
| Portfolio risk snapshot — factor decomposition, concentration, stress | `factor_risk_model.py` | `0038` |
| Backtest results — fold distribution, net-of-cost metrics | `backtesting.py`, `walk_forward.py` | `0044`, `0046` |
| Alerts — policy breaches, freshness, drift | `alerting.py`, `signal_monitoring.py`, `adapters/alert_delivery/` | `0020`, `0021`, `0032`, `0037` |

That set describes a **monitoring companion**: something you check, not
something you work in.

## 4. Two patterns the repository already has

Two of the three phases are not new architecture — they extend patterns
that already exist and are tested.

**A tool-agnostic dashboard contract.** `dashboard_spec.py` (`0015`)
defines `Panel` and `DashboardSpec`, and seven renderers already consume
it: Power BI, Excel, React (`0015`/`0016`), and Streamlit, Looker,
Superset, Qlik (`0018`). Three have executable scaffolders under
`adapters/dashboard_render/` (`react_scaffold.py`, `streamlit_scaffold.py`,
`xlsx.py`). **A SwiftUI renderer is the eighth target, not a new idea** —
it follows `react_profile.py` and `react_scaffold.py` directly.

**A delivery-provider contract.** `adapters/alert_delivery/` holds eight
providers including `sms_push.py`, each built on the same `transport`
injection seam: the SDK constructs the payload and never makes the
network call. **An APNs provider slots in beside them** with no new
architecture.

The gap is the middle: nothing exposes pipeline outputs to a client
process.

## 5. Phases

### Phase 0 — Web-first validation *(recommended before any of the below)*

Scaffold a Streamlit dashboard against real data using the existing
`streamlit_scaffold.py`, and use it on a phone browser.

- **Cost:** hours. No Apple developer account, no review cycle, no second
  client to maintain.
- **Value:** it answers the question the later phases depend on — *what do
  you actually want to look at on a phone?* — with usage rather than
  speculation.
- **Blocked on:** the same `fred_local.db` the FRED vertical slice needs.
- **Exit criterion:** either the web view is sufficient (stop here, and
  that is a real outcome), or specific gaps justify native.

**A native app is only warranted by one of three needs: push
notifications, offline access, or App Store distribution.** If none
applies, Phase 0 is the whole project.

### Phase 1 — `swiftui_profile` + `swiftui_scaffold`

An eighth `DashboardSpec` target.

- `src/quantsmith/pipelines/swiftui_profile.py` — renders a `DashboardSpec`
  into a validated SwiftUI view payload, mirroring `react_profile.py`.
- `src/quantsmith/adapters/dashboard_render/swiftui_scaffold.py` — writes
  an Xcode-ready project skeleton, mirroring `react_scaffold.py`
  (dry-run-capable, checksum manifest, no-secrets guard).
- **Self-contained:** no infrastructure, no hosting, no account. Useful
  regardless of how Phase 2 resolves.
- **Becomes:** one numbered spec under `specs/`.

### Phase 2 — A read API

The real work, and the one that forces a decision (§6).

- A thin service exposing the four surfaces of §3 as JSON.
- Read-only. No mutation, no order entry, no trading actions — those are
  categorically outside a monitoring companion.
- **Blocked until the decision in `decision_log.md` is settled.**

### Phase 3 — SwiftUI client + APNs

- The client consuming Phase 2's API and rendering Phase 1's payloads.
- `adapters/alert_delivery/apns.py` following the existing provider
  pattern.
- Requires an Apple developer account and App Store review.

## 6. The architectural decision this forces

**QuantSmith has deliberately never owned a running service.** Every
adapter is a contract plus an injected `transport`; that is precisely why
the repository holds no credentials, makes no network calls, and can
claim P9 cleanly. `dry_run=True` is the default on every provider.

Phase 2 breaks that posture. A hosted API means the project owns uptime,
authentication, secret storage, and a deployment target — none of which
exist today.

This is a genuine fork, comparable to the deferred numpy question in
`0044`, and it should be decided deliberately rather than drifted into.
The options and their consequences are recorded in
[`decision_log.md`](decision_log.md) as `AD-003`, left open.

## 6b. Keeping the QuantForge repository in sync

QuantForge lives in its own repository, so three mechanisms now exist on
the QuantSmith side, shipped as spec `0047`:

- **`DashboardSpec.schema_version`** (`MAJOR.MINOR`, currently `1.0`) plus
  `check_schema_compatibility`. A differing major is rejected; a newer
  minor is accepted with a caveat, so an SDK minor release does not break
  every client until it upgrades. The client refuses a payload it cannot
  render and shows stale data instead of crashing — which matters when a
  fix has to clear App Store review.
- **`.github/workflows/release-notify.yml`** — on a version tag,
  dispatches a `quantsmith-release` event to repositories listed in
  `vars.DOWNSTREAM_REPOS`, using `secrets.DOWNSTREAM_DISPATCH_TOKEN`. It
  **notifies only**; opening and merging the bump PR is the consumer's
  side. Inert until both are configured.
- **`hooks/stages/quantsmith-version-check.sh`** — copy into the app repo.
  Flags a `quantsmith` dependency that is unpinned, or pinned to a version
  other than the installed one. Offline and deterministic; it compares
  against the installed package, never a remote index.

**Two limits worth stating.** `schema_version` is a *declaration*, not a
derivation — bumping it is manual, so a breaking change shipped without a
bump is undetectable from this side. And the version gate only helps a
repository that actually installs the package; a pure-artifact consumer
is covered by `schema_version` on the payload instead.

**The consumer-side pieces belong in the app repository, not here:** a
pip entry in its Dependabot config, and a contract test that decodes a
real `DashboardSpec` from the installed `quantsmith`. That test is the
honest guard the declaration alone cannot provide.

**What this obliges of the SDK.** Once a second repository depends on it,
SemVer stops being a documentation claim and becomes something owed to a
consumer. The package is at `0.1.0` — which by SemVer convention promises
no stability — so publishing (`docs/packaging.md`) and a considered
version floor should land before the app repo is created, not after.

## 7. Risks

| ID | Risk | Mitigation |
| --- | --- | --- |
| RISK-A | Scope creep from "monitoring companion" toward "run the SDK on a phone". | §2 records the exclusion explicitly; any proposal to port an agent, gate, or spec surface should be rejected against it. |
| RISK-B | Building native before knowing what is worth looking at. | Phase 0 exists precisely to answer this with usage; its exit criterion permits stopping. |
| RISK-C | The API becomes a credential and uptime liability the SDK was designed to avoid. | `AD-003` must be settled before Phase 2 starts; a "no" is a legitimate outcome that leaves Phases 0, 1, and 3-minus-push intact. |
| RISK-D | A read-only companion accretes write actions (rebalance, place order) over time. | §5 Phase 2 states read-only as scope, not preference. Any write capability is a new initiative with its own risk review, not an increment. |
| RISK-E | Market data licensing. FRED is public; most equity and intraday data is not redistributable to a device. | Keep the companion on data whose licence permits it. Confirm per source in `sources/` before it reaches a client. |

## 8. Definition of done

The initiative is complete when **either**:

- Phase 0 is in use and judged sufficient — recorded as a decision, not
  an abandonment; **or**
- Phases 1–3 ship, each as a numbered spec passing the repository's
  gates, with a companion app that surfaces the four read-only surfaces
  of §3 and delivers alerts through an APNs provider built on the
  existing `transport` seam.

## 9. Open questions

- Which of the four surfaces in §3 matters most? Phase 0 should answer
  this before Phase 1 fixes a layout.
- Is there a second consumer for a Phase 2 API (a web dashboard, a
  notebook, a teammate's tooling)? A single-client API is much harder to
  justify than a shared one, and this materially affects `AD-003`.
- Single user, or multi-user? Authentication, per-user configuration, and
  data isolation are absent from the current design and would change
  Phase 2's scope substantially.

## 10. First actions

1. Produce `fred_local.db` (see `docs/handoff.md` — the same prerequisite
   as the FRED vertical slice).
2. Scaffold and use the Streamlit view (Phase 0).
3. Settle `AD-003` in `decision_log.md` before any Phase 2 work.
4. If proceeding, open `specs/NNNN-swiftui-dashboard-profile/` for
   Phase 1 — it is independent of the decision and can start earlier.
