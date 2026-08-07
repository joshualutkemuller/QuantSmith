# QuantSmith Git & GitHub Best Practices

## Branching
- Keep `main` clean and deployable.
- Create feature branches for new work, e.g. `feat/research-agent`, `docs/model-card-template`.
- Use descriptive branch names and avoid long-lived branches.

## Commit Messages
- Follow Conventional Commits:
  - `feat(...)`: new feature
  - `fix(...)`: bug fix
  - `docs(...)`: documentation only
  - `chore(...)`: build or tooling
  - `refactor(...)`: code change that neither fixes a bug nor adds a feature
  - `perf(...)`: performance improvement
  - `test(...)`: adding or fixing tests
  - `build(...)`: build system changes
- Example: `docs(agents): add data quality review agent`

## Pull Requests
- One PR per coherent feature or fix.
- Include a short description, key changes, and test/verification steps.
- Link PRs to relevant roadmap, handoff, or workflow docs.
- Keep diffs small and reviewable.

## Code Quality
- Keep agents, prompts, instructions, and templates scoped to one workflow concern when possible.
- Check shell hook syntax before changing hooks:
  - `sh -n setup-hooks.sh`
  - `for hook in .githooks/*; do sh -n "$hook"; done`
- Keep documentation changes tied to the workflow surface they describe.

## Git Hooks
- This repo contains local hooks in `.githooks/`.
- Run the setup script after cloning:
  - `./setup-hooks.sh`
- Or manually enable them:
  - `git config core.hooksPath .githooks`
  - `chmod +x .githooks/*`
- Hooks included:
  - `pre-commit`: validates required SDK docs and hook shell syntax
  - `commit-msg`: validates Conventional Commit format
  - `pre-push`: validates required SDK docs

## Dependency Workflow
- Keep dependency managers and lockfiles scoped to the package or tool that needs them.
- Do not add runtime dependencies for documentation-only changes.

## Agent / Automation Guidance
- Keep public agent definitions in `agents/`.
- Keep reusable instructions in `instructions/`.
- Keep task prompts in `prompts/`.
- Keep roadmap and handoff material in `docs/`.
- Prefer small, incremental commits when adding SDK surfaces.

## Future GitHub Integrations
- Consider adding GitHub Actions for:
  - Markdown linting and link checks
  - PR title/pattern validation
  - agent folder contract validation
  - dependency security scans when package manifests are introduced
- Keep CI fast and focused on preventing workflow regressions.
