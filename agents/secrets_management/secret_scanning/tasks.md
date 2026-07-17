# Secret Scanning Tasks

## Scan For Leaks

Input: code, diff, history, logs, or notebooks.

Output: redacted findings with location and type, ranked by severity.

## Remediate A Leak

Input: a confirmed committed secret.

Output: a rotate-revoke-purge plan, including history rewrite steps and a note to
notify affected consumers.

## Set Up Prevention

Input: a repo without secret scanning.

Output: pre-commit and CI scanning configuration and a false-positive allowlist.

## Notebook & Log Sweep

Input: notebooks and log outputs.

Output: findings of secrets in outputs/logs and steps to clear and prevent them.
