# QuantSmith Agent Guidance

This file describes helpful automation and assistant patterns for the QuantSmith repo.

## Purpose
- Provide a clear structure for future agents or AI helpers.
- Keep agent behavior aligned with the SDK roadmap and handoff documents.
- Help contributors use consistent prompts and tasks.

## Ideal Agent Responsibilities
- Suggest next small SDK tasks based on the handoff document.
- Validate local hook and documentation status.
- Summarize repo state before making edits.
- Avoid making large workflow or packaging decisions without explicit approval.

## Useful Agent Prompts
- "Review `docs/sdk_plan.md` and propose the next public agent to scaffold."
- "Inspect `docs/handoff.md` and add a backlog entry for hook migration."
- "Run the local hook syntax checks and report any errors."

## Recommended Agent Behavior
- Always read `docs/sdk_plan.md` and `docs/handoff.md` before changing SDK structure.
- Prefer updating existing files instead of adding new unrelated files.
- Keep commits small and focused.
- Do not overwrite roadmap or handoff docs without user approval.

## Git Focused Agent Rules
- When asked to commit, use Conventional Commit format.
- If there are unstaged changes, report them before pushing.
- If a branch is not clean, ask whether to stash, commit, or discard changes.

## Future Enhancements
- Add GitHub Actions workflows for Markdown, hook, and agent contract checks.
- Add public agent folders under `agents/`.
- Add document templates for model cards, dataset cards, and research memos.
