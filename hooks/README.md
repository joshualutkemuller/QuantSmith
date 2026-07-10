# QF Workflow SDK Hooks

This is the public hook surface of the SDK. It ships lightweight quality gates
aligned to the six development stages, each paired with the agent that owns that
stage.

Active local Git hooks live in `.githooks/` and are wired by `setup-hooks.sh`.
The scripts here are portable stage checks you can run manually, in CI, or wire
into Git hooks.

## Stage Hooks

Located in `hooks/stages/`, one per development stage:

| Stage | Script | Companion agent |
| --- | --- | --- |
| 1. Planning / Requirements | `planning-check.sh` | `agents/planning_requirements/` |
| 2. Design | `design-check.sh` | `agents/design_architecture/` |
| 3. Coding / Implementation | `implementation-check.sh` | `agents/implementation/` |
| 4. Testing | `testing-check.sh` | `agents/testing_validation/` |
| 5. Deployment | `deployment-check.sh` | `agents/deployment_release/` |
| 6. Maintenance | `maintenance-check.sh` | `agents/maintenance_monitoring/` |

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
