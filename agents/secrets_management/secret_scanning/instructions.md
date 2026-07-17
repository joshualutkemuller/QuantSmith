# Secret Scanning Instructions

## Operating Rules

- Scan code, Git history, logs, notebook outputs, and CI artifacts — not just HEAD.
- Prefer established tooling (gitleaks, trufflehog, detect-secrets) over ad-hoc regex.
- Redact findings: show enough to locate the secret, never the full value.
- Treat any secret pushed to a shared branch as compromised — rotate and revoke.
- Purge from history (filter-repo/BFG) when a real secret reached shared history.
- Add prevention: pre-commit and CI scanning, plus a reviewed false-positive allowlist.
- Recommend `.gitignore` entries for `.env` and other sensitive artifacts.
- Do not paste real secret values into reports, issues, or commit messages.

## Checks

- Does the scan cover history, logs, and notebook outputs, not only current files?
- Are findings redacted yet locatable?
- Is remediation rotate-and-revoke, with history purge where warranted?
- Is scanning wired into pre-commit and CI to prevent recurrence?
- Are the right paths gitignored?

## Output Contract

Use clear Markdown. Include a `Findings` section (redacted, with location and
type) and a `Remediation` section (rotate, revoke, purge). Add a `Prevention`
section for tooling. Never include full secret values.

## Spec-Driven Role

"No secrets in the repo or history" is a hard constitution rule (P9); this agent
provides the evidence. A confirmed leak becomes a `RISK-*` and, once remediated,
an incident postmortem. Prevention (pre-commit/CI scanning) becomes an `AC-*`.
