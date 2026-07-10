# Git & Release Agent

## Purpose

The Git & Release Agent keeps commits, branches, pull requests, changelogs, and
release records clean and reviewable. It enforces the repository's Git workflow so
history stays a reliable audit trail.

## Use When

- A change needs to be committed and pushed following the repo's conventions.
- A pull request needs a description that maps to the spec and its acceptance criteria.
- A release needs a changelog entry and a version tag.
- Branch or commit hygiene has drifted and needs cleanup.

## Inputs

- The change and its owning spec (`spec.md` / `plan.md` / `tasks.md`).
- Repository Git conventions (`instructions/git_workflow.md`, `.githooks/`).
- Target branch and release/versioning policy.

## Outputs

- Conventional Commit messages scoped to the change.
- A pull request description mapped to requirements and acceptance criteria.
- Changelog entries and version tags.
- Branch and history hygiene recommendations.

## Example Requests

- "Write Conventional Commit messages for this change set."
- "Draft a PR description that maps each requirement to what changed."
- "Prepare the changelog entry and version bump for this release."

## Required Review Themes

- Commit messages follow Conventional Commits and are scoped.
- The PR traces to the spec IDs it satisfies.
- History is reviewable: small, coherent commits.
- Changelog and version reflect the actual change.
- Local hooks and CI gates pass before push.
