# Git Workflow Instructions

## Purpose

Use this instruction set when making repository changes for quant workflow assets, including agents, prompts, instructions, templates, hooks, examples, and documentation.

## Required Inputs

- Intended change scope.
- Current branch and worktree status.
- Files to modify.
- Validation commands or checks.
- Commit or pull request target.

## Expected Output

- Focused change set.
- Clear commit message.
- Validation summary.
- Handoff notes for reviewers.

## Standards

- Keep changes small and reviewable.
- Use Conventional Commits.
- Do not mix unrelated SDK surfaces in one change unless the handoff explains why.
- Preserve user changes that are outside the current task.
- Keep public agent contracts consistent: `README.md`, `prompt.md`, `instructions.md`, and `tasks.md`.
- Update README or handoff docs when public SDK surfaces change.

## Checks

- Is the worktree status understood before editing?
- Are only intended files staged?
- Do hooks and CI still match the repository structure?
- Are new public assets linked from README or docs?
- Are validation results reported?

## Common Failure Modes

- Staging unrelated local work.
- Letting docs drift from folder structure.
- Adding prompts without expected inputs and outputs.
- Adding hooks that assume a downstream app structure.

## Spec-Driven Alignment

This standard supports the Operate step's release record. A pull request is where
the spec chain is made visible to reviewers: list the `REQ-*`/`AC-*` the change
satisfies and confirm the `spec-check` gate passes. Small, reviewable changes are
constitution P7; no silent trade-offs (P8) means recording deviations in the spec,
not the commit alone. Keep the agent contract intact (`README.md`, `prompt.md`,
`instructions.md`, `tasks.md`) so the pre-commit, pre-push, and CI checks pass.
