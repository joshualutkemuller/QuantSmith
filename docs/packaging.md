# Packaging & Distribution Decision Record

- **Status:** Accepted (direction set; phased)
- **Decision:** Formalize the copyable template now; add a Copier-style sync CLI
  when update pain is real; reach for a Python package only when there is real
  executable logic to ship.
- **Last updated:** 2026-07-17

This record answers the open question "should the SDK be a Python package, a CLI
scaffold, or a copyable repo template?" It is a decision record, not a tutorial;
the adoption mechanics belong in `docs/adoption_guide.md` (to be written).

## Context

The SDK ships almost no code. Its deliverables are static content (agents,
instructions, prompts, templates, the constitution), shell gates
(`hooks/stages/*.sh`), and conventions (the spec-driven flow, the ID scheme, the
agent contract). None of it is importable, so the decision is not a package
*format* — it is the **consumption and update model**. There are no packaging
manifests today; consumption is "copy the files in," and `setup-hooks.sh` wires
only this repo's own git hooks.

Two questions drive the choice:

1. **Copy-once or living dependency?** Snapshot and own forever, or stay
   subscribed to upstream improvements.
2. **Own or pinned?** The gates are meant to be tuned per repo (heuristic
   patterns, artifact names); tuned files and upstream-synced files pull apart.

## The Core Tension

The surfaces split into two classes that want to be consumed differently:

| Class | Examples | Wants to be… |
| --- | --- | --- |
| Reference / stable | constitution, SDD method, agent prompts, templates | pinned & updatable (get upstream fixes) |
| Owned / tuned | `hooks/stages/*` patterns, CI wiring, `specs/*` | copied & owned (local edits, never overwritten) |

Any approach that treats the SDK as one blob forces a bad trade: updates clobber
local tuning, or teams fork and never get improvements. Good designs let the two
classes be consumed differently.

## Options Considered

### A. Copyable template (status quo, formalized)
GitHub "template repository," `degit`, or manual copy.
- **Pros:** zero tooling; total control; language/runtime agnostic.
- **Cons:** no update path; permanent drift; every team re-tunes from scratch.
- **Fit:** great for owned/tuned files, useless for keeping reference content current.

### B. Git subtree / submodule
Vendor under `vendor/qf_sdk/`; `git subtree pull` to update.
- **Pros:** real update path; clear ours/theirs boundary; no registry.
- **Cons:** submodule ergonomics confuse non-platform users; subtree merges get
  messy once vendored gate files are edited locally — which teams will do.
- **Fit:** workable for un-edited reference content; poor where local tuning is expected.

### C. CLI scaffolder (Copier / Cookiecutter / custom)
`qf init` / `copier copy` stamps selected pieces into a target repo; Copier can
re-run to pull updates while preserving local answers via `.copier-answers.yml`.
- **Pros:** selective adoption (take 5 of 21 agents); guided setup wires hooks + CI;
  Copier's update mode is the closest thing to "update without clobbering"; can
  template the CI YAML correctly per repo.
- **Cons:** a tool to maintain; update still conflicts on heavily edited files;
  adds a Python/`pipx` dependency to a mostly-Markdown product.
- **Fit:** best all-rounder for a growing SDK with many optional pieces.

### D. Python (or npm) package
`pip install qf-workflow-sdk`; vendor the Markdown/shell as data files; expose a
console-script CLI.
- **Pros:** familiar version pinning; natural home if the SDK gains real Python
  (e.g. an AST leakage checker).
- **Cons:** shipping Markdown as a pip package is an impedance mismatch; assets in
  `site-packages` still need a `qf sync` step to materialize where git hooks/CI see
  them — so you build the CLI from option C anyway; ties an agnostic SDK to Python.
- **Fit:** compelling only if the SDK acquires meaningful executable logic. It has
  none today.

### E. Hybrid: template for owned files + pinned/synced reference (chosen direction)
- Reference content → a versioned, syncable set teams pin and update, read-only.
- Owned files → scaffolded once and owned locally, never auto-overwritten.
- A thin `qf` CLI ties them together: `qf init`, `qf sync` (reference only),
  `qf add <agent>` for selective adoption.

## What The Codebase Already Signals

- `run-stage.sh` takes named stages — partial adoption is already first-class; a
  CLI selecting gates is the natural extension.
- Gates are advisory-by-default and degrade gracefully — built to be copied and
  tuned, i.e. they belong to the owned class.
- The agent contract is mechanically checkable (`prompt.md` detection) — a CLI can
  scaffold/validate agents trivially.
- Everything is self-contained Markdown/shell with no dependencies — an argument
  against a Python package as the primary vehicle today.

## Decision

Treat packaging as a **sequence**, not a single choice:

1. **Now — formalize the template.** Mark the repo a GitHub template repository and
   write `docs/adoption_guide.md` documenting the copy-and-own model and how to
   tune the gates. Near-zero effort; unblocks adoption immediately. Copy-once is
   honest for a first cohort.
2. **Next — add a Copier-style `qf` CLI** when a second or third team feels the
   update pain. Implement the hybrid: scaffold owned files once, sync pinned
   reference content on demand, support selective agent/gate installation. This is
   where the SDK's scale (21 agents, 14 gates) pays off.
3. **Later — a Python package** only once there is real executable logic worth
   shipping (e.g. replacing regex leakage/secret heuristics with an AST/entropy
   engine). The package then ships that engine plus the CLI; the Markdown stays
   template-distributed.

**Trap to avoid:** jumping straight to a pip package because it feels more
finished. It adds a runtime dependency and a `site-packages` indirection to a
product that is ~95% Markdown, and you would still have to build the sync CLI.
Earn the package with code.

## Decision Criteria (revisit if these change)

- **Who adopts?** Quants copying into one repo → template. A platform team
  standardizing many repos → CLI with sync.
- **Update cadence?** Frequent changes teams must track → need sync (C/E).
  "Stamp once, rarely revisit" → template (A) is honest.
- **How much do adopters edit the gates?** Heavy local tuning kills
  submodule/subtree; favors Copier's answer-preserving update.
- **Will there ever be real code?** If yes, a package eventually houses it. If it
  stays content-only, a package is ceremony.
- **Who maintains the tooling?** A CLI is a product with its own releases; take it
  on only if someone owns it.

## Consequences

- The immediate next deliverable is `docs/adoption_guide.md`, not tooling.
- Keep the reference/owned split visible as the SDK grows, so a future `qf sync`
  can update reference content without touching tuned gates.
- Do not add a packaging manifest or publish to a registry until step 2/3 is
  triggered by real demand.
