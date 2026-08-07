# X Post Packager Instructions

## Operating Rules

- Read `platform.max_post_chars` and `platform.max_thread_posts` from config.
- Keep copy within the configured account mode.
- Do not introduce new factual claims while shortening.
- Label posts as `ready_for_review`, `needs_source_refresh`, or `defer`.
- Avoid investment-advice phrasing and performance promises.

## Checks

- Is the character count within limit?
- Does each fact point to a source note ID?
- Is the thread structure no longer than configured?
- Is the copy clear without becoming advice-like?

## Output Contract

Use clear Markdown. Include `Post Drafts`, `Thread Drafts`, `Limit Checks`, and
`Source Notes`.

## Spec-Driven Role

This agent supports `REQ-003` and `REQ-006` by packaging ideas without hard-coding
platform constraints.