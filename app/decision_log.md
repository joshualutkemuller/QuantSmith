# Decision Log: iOS Companion Initiative

> A durable, **append-only** record of material decisions, alternatives
> considered, rationale, and consequences (see `agentic_dictionary.md`'s
> Decision Log entry). A new decision gets a new entry; a superseded
> decision is never edited or deleted — a follow-up entry supersedes it and
> says so, so the record of *why* something changed stays intact
> (constitution P10, honest reporting).

- **Owner:** Josh
- **Scope:** The iOS companion initiative described in [`handoff.md`](handoff.md)

## Entries

Copy the block below for each new decision. Newest entry last, oldest
first — do not reorder past entries.

### AD-001: The companion is read-only monitoring, not the SDK on a phone

- **Date:** 2026-08-12
- **Decision maker(s):** Josh, Claude
- **Status:** decided

**Decision:** The iOS companion surfaces computed outputs — macro
indicators and regime, portfolio risk, backtest results, and alerts. The
agent contracts, quality gates, spec-driven workflow, git hooks, and CI
are explicitly excluded.

**Rationale:** Those surfaces operate on a repository and a git working
tree. There is no iPhone analogue for running `run-stage.sh` or authoring
a `spec.md`, so porting them would produce an app with no user. Writing
the exclusion down is what stops "turn the repo into an app" expanding
silently.

**Alternatives considered:**

| Alternative | Why rejected |
| --- | --- |
| Port the full SDK surface to iOS | The majority of it is development-time tooling over a repository; there is no mobile use case. |
| A general "quant workbench" app with authoring | Authoring specs and reviewing diffs on a phone is worse than on a desk in every respect; it would compete with the tool that already works. |

**Consequences:** Commits the initiative to a read-only consumer of
existing runtime outputs. Any proposal to surface an agent, gate, or spec
authoring flow should be rejected against this entry. Also means the app
has no value until a runtime is producing real output — which is why the
FRED slice is a prerequisite rather than a parallel track.

**Evidence / references:** [`handoff.md`](handoff.md) §2, §3.

### AD-002: Web-first validation precedes any native work

- **Date:** 2026-08-12
- **Decision maker(s):** Josh, Claude
- **Status:** decided

**Decision:** Phase 0 scaffolds a Streamlit dashboard using the existing
`adapters/dashboard_render/streamlit_scaffold.py` and is used on a phone
browser before any native phase begins. If the web view proves
sufficient, stopping there is a successful outcome, recorded as a
decision rather than an abandonment.

**Rationale:** The repository can already scaffold Streamlit, so Phase 0
costs hours and needs no Apple developer account, review cycle, or second
client. It answers the question every later phase depends on — what is
actually worth looking at on a phone — with usage instead of speculation.
A native app is warranted only by push notifications, offline access, or
App Store distribution; absent those, it is cost without benefit.

**Alternatives considered:**

| Alternative | Why rejected |
| --- | --- |
| Build the SwiftUI client first | Fixes a layout and a data contract before anyone knows which surfaces matter, and carries Apple account and review overhead from day one. |
| Skip validation, build all three phases | Highest-cost path to discovering the requirement, and the hardest to reverse once an App Store listing exists. |

**Consequences:** Delays native work by the length of Phase 0 and makes
it conditional. Accepts that the initiative may correctly end at Phase 0.
Phase 1 (the SwiftUI profile) is exempt from the dependency because it is
self-contained and useful regardless.

**Evidence / references:** [`handoff.md`](handoff.md) §5 Phase 0;
`specs/0018-remaining-dashboard-profiles/` for the existing Streamlit
scaffolder.

### AD-003: Whether QuantSmith starts owning a running service

- **Date:** 2026-08-12
- **Decision maker(s):** Josh
- **Status:** **open — must be settled before Phase 2 begins**

**Decision:** *Not yet made.* Phase 2 requires a hosted read API exposing
pipeline outputs as JSON. This would be the first running service the
project owns.

**Rationale (for why it is open, not assumed):** QuantSmith has
deliberately never owned a service. Every adapter is a contract plus an
injected `transport`; `dry_run=True` is the default on all eight alert
providers. That design is exactly why the repository holds no
credentials, makes no network calls, and can claim P9 cleanly. A hosted
API means owning uptime, authentication, secret storage, and a deployment
target — none of which exist today. This is a genuine architectural fork,
comparable to the numpy question deferred in `specs/0044-backtesting/`,
and drifting into it by accident would be the worst outcome.

**Alternatives considered:**

| Alternative | Consequence if chosen |
| --- | --- |
| **A. Own a hosted read API** | Unlocks Phases 2–3 fully. Costs: the project takes on uptime, auth, and secret storage, and P9's "no credentials here" claim needs restating for the service boundary. |
| **B. Precompute and publish static artifacts** | The pipelines already render Markdown reports; publishing them to object storage keeps the no-service posture. Costs: no live data, refresh only as often as the job runs, and no per-user state. |
| **C. Run locally, sync a file** | The companion reads a file the operator produces (the same boundary `0045` uses for `fred_local.db`). Keeps P9 intact entirely. Costs: manual refresh, no push. |
| **D. Do not build Phase 2** | Phases 0, 1, and a push-less Phase 3 remain viable. Costs: no live data in the app at all. |

**Consequences:** Unresolved. Recorded here so Phase 2 cannot start
without an explicit choice, and so a future reader can see that the
no-service posture was a decision rather than an oversight. Options B and
C are deliberately listed because they preserve the existing architecture
and are not obviously worse for a single-user monitoring companion.

**Evidence / references:** [`handoff.md`](handoff.md) §6, RISK-C;
`adapters/alert_delivery/` for the transport-injection precedent;
`instructions/engineering_principles.md` P9.
