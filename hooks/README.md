# QF Workflow SDK Hooks

This is the public hook surface of the SDK. It ships lightweight quality gates
aligned to the six development stages, each paired with the agent that owns that
stage.

Active local Git hooks live in `.githooks/` and are wired by `setup-hooks.sh`.
The scripts here are portable stage checks you can run manually, in CI, or wire
into Git hooks.

## Stage Hooks

Located in `hooks/stages/`, one per development stage plus a cross-cutting
spec-driven check that runs first:

| Stage | Script | Companion agent |
| --- | --- | --- |
| 0. Spec-driven chain (cross-cutting) | `spec-check.sh` | all — enforces `instructions/spec_driven_development.md` |
| 1. Planning / Requirements | `planning-check.sh` | `agents/planning_requirements/` |
| 2. Design | `design-check.sh` | `agents/design_architecture/` |
| 3. Coding / Implementation | `implementation-check.sh` | `agents/implementation/` |
| 4. Testing | `testing-check.sh` | `agents/testing_validation/` |
| 5. Deployment | `deployment-check.sh` | `agents/deployment_release/` |
| 6. Maintenance | `maintenance-check.sh` | `agents/maintenance_monitoring/` |

### Quant Gates (cross-cutting)

Quant-specific heuristic checks that run after the SDLC stages. Advisory and
pattern-based; tune them to your repository.

| Gate | Script | Companion |
| --- | --- | --- |
| Look-ahead & leakage | `leakage-check.sh` | `instructions/point_in_time.md`, `agents/feature_engineering/` |
| Backtest integrity | `backtest-check.sh` | `agents/backtest_review/` |
| Reproducibility | `repro-check.sh` | `templates/docs/run_card.md`, `agents/implementation/` |
| Data contract | `data-contract-check.sh` | `templates/data/data_contract.md`, `agents/data_quality/` |

### Repo Gates (security & docs integrity)

| Gate | Script | Companion |
| --- | --- | --- |
| Secret leak scan | `secret-scan-check.sh` | `agents/secrets_management/` |
| Markdown link check | `docs-link-check.sh` | all docs |
| Agent catalog sync | `agent-catalog-check.sh` | `agents/README.md` |

Each script:

- checks for the artifacts and hygiene that stage cares about;
- **degrades gracefully** — missing tools or files produce a warning, not a crash;
- is **advisory by default** (prints findings, exits `0`) so it never blocks
  exploratory work.

## Usage

```sh
# Run every stage check:
hooks/stages/run-stage.sh

# Run one or several stages:
hooks/stages/run-stage.sh testing
hooks/stages/run-stage.sh planning design

# Run only the spec-driven traceability check:
hooks/stages/run-stage.sh spec

# Run only the quant gates:
hooks/stages/run-stage.sh leakage backtest repro data-contract
```

## Quant Gates

- **`leakage-check.sh`** scans changed Python/notebook files for high-signal
  look-ahead and leakage smells (negative `shift`, `bfill`, unshuffled
  `train_test_split`, whole-sample scaler fit) per `instructions/point_in_time.md`.
  Heuristic — it points a reviewer at lines, it does not prove leakage.
- **`backtest-check.sh`** verifies a backtest report artifact addresses transaction
  costs, out-of-sample, benchmark, turnover/capacity, and multiple-testing.
- **`repro-check.sh`** checks for a run manifest (`run_card`), a dependency
  lockfile, and seeded randomness in changed code.
- **`data-contract-check.sh`** verifies a data contract declares schema, keys,
  point-in-time rules, and missingness rules.

## Repo Gates

- **`secret-scan-check.sh`** detects committed secrets. Uses `gitleaks` or
  `detect-secrets` when installed; otherwise a high-signal regex fallback over
  changed code/config files (docs and SDK scaffolding are skipped). Allowlist a
  file via `.secretscanignore`, or a line with a trailing `qf:allow-secret`
  marker. Enforced in CI.
- **`docs-link-check.sh`** verifies relative Markdown links and image paths
  resolve to existing files. External links and pure anchors are skipped.
- **`agent-catalog-check.sh`** verifies every public agent (a directory with
  `prompt.md`) is listed in `agents/README.md`.

## Spec-Driven Check

`spec-check.sh` validates the Spec-Driven Development chain across every
`specs/<id>/` directory (see `instructions/spec_driven_development.md`):

- `spec.md`, `plan.md`, `tasks.md` are present (no plan/tasks without a spec).
- `spec.md` declares requirements (`REQ-*`/`NFR-*`) and acceptance criteria (`AC-*`).
- Every requirement is covered in `plan.md` or `tasks.md`.
- Every acceptance criterion is referenced in `tasks.md` (test coverage map).
- No orphan tasks — every `T-*` cites a requirement.

Run it in enforce mode to block merges that break traceability:

```sh
QF_STAGE_ENFORCE=1 hooks/stages/run-stage.sh spec
```

## Configuration

Behavior is controlled by environment variables:

| Variable | Effect |
| --- | --- |
| `QF_STAGE_ENFORCE=1` | Make findings blocking (non-zero exit). Use in CI or as a strict gate. |
| `QF_RUN_TESTS=1` | Let the testing stage actually run the suite (`pytest`) when present. |
| `QF_DIFF_BASE=<ref>` | Diff changed files against `<ref>` (e.g. `origin/main`) instead of the working tree. |

## Wiring Into Git

To run a subset of stage checks on commit, add a call from `.githooks/pre-commit`:

```sh
# In .githooks/pre-commit
sh hooks/stages/run-stage.sh implementation testing
```

To gate a push against the release-oriented stages:

```sh
# In .githooks/pre-push
QF_STAGE_ENFORCE=1 sh hooks/stages/run-stage.sh deployment
```

## Wiring Into CI

Run the full set in enforce mode against the pull request base:

```sh
QF_STAGE_ENFORCE=1 QF_DIFF_BASE=origin/main sh hooks/stages/run-stage.sh
```

## Design Notes

- Hooks are guardrails, not traps. Advisory mode keeps research fast; enforce
  mode is opt-in for the paths that must not regress.
- Checks are conventional, not prescriptive: they look for common artifact names
  and doc sections. Adjust the patterns to your repository's layout.
- Every stage hook points back to its companion agent so a finding has an owner.
