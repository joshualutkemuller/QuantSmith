# Adoption Guide

How to install QuantSmith into an existing quant repository. The SDK is a
scaffold of Markdown and shell — you copy the surfaces you want and wire the gates
into your hooks and CI. See `docs/packaging.md` for the distribution model.

## What You Are Installing

| Surface | What it gives you | Take it if… |
| --- | --- | --- |
| `instructions/` | The constitution and reusable standards | always — this is the backbone |
| `agents/` | Role definitions for research, review, and tooling | you use an agent runtime or want review checklists |
| `hooks/stages/` | Portable quality gates | you want mechanical checks in hooks/CI |
| `templates/` | Spec, doc, and data-contract templates | you want consistent artifacts |
| `prompts/` | Task-ready prompts | you drive work with prompts |
| `specs/` | The per-feature spec convention | you adopt Spec-Driven Development |
| `CLAUDE.md` | Activates the framework for agents in the repo | you use Claude Code or similar |

Adopt incrementally — the gates take named stages, so you can start with one.

## 1. Copy The Surfaces

From the SDK repo, copy the directories you want into your repo root. At minimum:

```sh
cp -R quantsmith/instructions   your-repo/
cp -R quantsmith/hooks          your-repo/
cp    quantsmith/CLAUDE.md       your-repo/    # optional but recommended
# add agents/, templates/, prompts/, specs/ as needed
```

(Or use the SDK repo as a GitHub template / `degit` source once it is marked a
template repository — see `docs/packaging.md`.)

## 2. Wire The Gates Into CI

The portable gates live in `hooks/stages/` and run via `run-stage.sh`. Add to your
CI (advisory first, then enforce what fits):

```sh
# Advisory — prints findings, never fails the build:
sh hooks/stages/run-stage.sh

# Enforce specific gates — fails the build on findings:
QF_STAGE_ENFORCE=1 sh hooks/stages/run-stage.sh spec secret-scan
```

For diff-based gates (`leakage`, `secret-scan`) in a pull request, pass the base:

```sh
QF_DIFF_BASE="origin/${GITHUB_BASE_REF:-main}" sh hooks/stages/run-stage.sh leakage
```

A good starting CI policy: **enforce** `secret-scan` and (if you write specs) `spec`;
run everything else **advisory** until you have tuned the patterns.

## 3. Wire The Gates Into Git Hooks (optional)

To run gates locally on commit/push, call them from your existing hooks:

```sh
# in your .git hooks (or a pre-commit framework):
sh hooks/stages/run-stage.sh implementation secret-scan
```

Note: the SDK's own `.githooks/` and `setup-hooks.sh` enforce *SDK-repo* invariants
(required SDK docs, the agent contract). Adopt those only if you keep the SDK layout;
otherwise wire the `hooks/stages/` gates into your own hooks and skip `.githooks/`.

## 4. Configure

Behavior is controlled by environment variables (see `hooks/README.md`):

| Variable | Effect |
| --- | --- |
| `QF_STAGE_ENFORCE=1` | Make gate findings blocking. |
| `QF_RUN_TESTS=1` | Let the testing gate run your suite. |
| `QF_DIFF_BASE=<ref>` | Diff against a base branch for diff-based gates. |
| `QF_KNOWLEDGE_SOURCES` / `QF_KNOWLEDGE_BASE` | Point the knowledge gate at your knowledge locations. |

If you use the knowledge agents, copy `templates/knowledge/knowledge_sources.yml`
to your repo root as `knowledge_sources.yml` and set real paths.

## 5. Tune The Gates To Your Repo

The gates are conventional, not prescriptive — they look for common artifact names
and doc sections. Adjust the patterns to your layout:

- `backtest-check.sh` / `data-contract-check.sh` — file-name globs for your reports
  and contracts.
- `secret-scan-check.sh` — add path globs to `.secretscanignore`, or append a
  `qf:allow-secret` marker to a line; install `gitleaks`/`detect-secrets` for a
  stronger scan.
- `repro-check.sh` — the lockfile and run-manifest names your repo uses.

## 6. Adopt Spec-Driven Development (recommended)

1. Read `instructions/engineering_principles.md` (the constitution) and
   `instructions/spec_driven_development.md` (the method).
2. For your next non-trivial change, create `specs/NNNN-slug/` from `templates/spec/`
   and assign IDs (`REQ`/`NFR`/`AC`/`RISK`/`T`).
3. Enforce the chain in CI: `QF_STAGE_ENFORCE=1 sh hooks/stages/run-stage.sh spec`.
4. Let the `workflow_orchestrator` agent (or a human) drive the flow through the gates.

Copy `specs/0001-daily-momentum-signal/` as a filled-in reference.

## 7. Keep It Updated

The gates and the heuristic patterns you tune are *yours* to own; the reference
content (constitution, method, agent prompts, templates) is what you will want to
re-sync as the SDK improves. Until a sync CLI exists (see `docs/packaging.md`),
re-copy the reference surfaces and re-apply your local pattern tweaks.

## Minimal Adoption (the 5-minute version)

```sh
cp -R quantsmith/instructions your-repo/
cp -R quantsmith/hooks        your-repo/
# add to CI:
#   QF_STAGE_ENFORCE=1 sh hooks/stages/run-stage.sh secret-scan
#   sh hooks/stages/run-stage.sh        # everything else, advisory
```

That gives you the constitution, the standards, and a secret-scan gate on day one;
grow from there.
