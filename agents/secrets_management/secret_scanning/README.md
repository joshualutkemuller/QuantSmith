# Secret Scanning Agent

## Purpose

The Secret Scanning Agent detects leaked secrets in code, Git history, logs, and
notebook outputs, and drives remediation. It is the defensive counterpart to the
other secrets agents: it finds what slipped through and prevents recurrence.

## Use When

- A change or repo needs a scan for committed secrets before it ships.
- A secret is suspected to be in history, logs, or notebook outputs.
- Pre-commit/CI secret scanning needs to be set up or reviewed.
- A confirmed leak needs a remediation plan.

## Inputs

- The code, diff, history, logs, or notebooks to scan.
- Existing scanning tooling (e.g. gitleaks, trufflehog, detect-secrets) if any.
- The secret store and rotation path for remediation.

## Outputs

- Findings: likely secrets with location and type, without echoing full values.
- A remediation plan: rotate, revoke, and purge from history.
- Prevention: pre-commit/CI scanning and an allowlist for false positives.
- A recommendation to add missing `.gitignore` entries.

## Example Requests

- "Scan this diff and history for committed secrets and rank the findings."
- "This key was pushed — give me the rotate, revoke, and history-purge steps."
- "Set up pre-commit and CI secret scanning for this repo."

## Required Review Themes

- Coverage: code, history, logs, notebook outputs, and CI artifacts.
- Findings reported without exposing the full secret in the report.
- Remediation is rotate-and-revoke, not just deletion — a pushed secret is burned.
- History purge (e.g. filter-repo/BFG) when a secret reached a shared branch.
- Prevention wired into pre-commit and CI so it does not recur.

## Companion

Complements the implementation-stage secret check in
`hooks/stages/implementation-check.sh`, which flags common secret patterns in
changed files.
