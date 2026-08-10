# Role Operations Agents

This folder groups agents aimed at a specific problem: a quant/data-science
lead's job generates a lot of work that isn't the modeling, scoping, or
research that make the role valuable — meeting follow-ups, status updates,
prototype setup, first-pass research scans. These agents absorb that
operational layer so more of the week goes to the work itself.

## Note On Scope

This is **Phase 1 + Phase 2** of a four-pillar roster (Framework Design, Client
& Stakeholder Engagement, Model Governance, Innovation & Prototyping). Phase 1
(spec `0024`) was the lowest-risk, highest-frequency slice, chosen deliberately
so the habit forms on work that never touches a client or a governance
committee before any agent gets near either. Phase 2 (spec
`0029-role-operations-agents-phase2`) extends into prototype accelerators —
still nothing governance-facing. **Phase 3** (model-card drafting, audit-trail
keeping, governance-readiness checklists — higher stakes, sequenced last) is
the remaining follow-up — see `specs/0029-.../tasks.md`'s Follow-ups.

## Configuration

Every agent here is generic by default and sharpens its output when a local,
**gitignored** `role_context.yml` is present at the repo root (copy it from
[`templates/role_operations/role_context.yml`](../../templates/role_operations/role_context.yml)
and fill in your own specifics — never commit it). No agent in this group
requires configuration to produce a sensible result, and none may hardcode a
real platform, firm, or client name in anything tracked by git. See
`instructions/role_operations.md` and the `role-context` gate
(`hooks/stages/role-context-check.sh`), which blocks (under
`QF_STAGE_ENFORCE=1`) if a filled-in `role_context.yml` is ever staged or
tracked.

## Agents

| Agent | Handles | Feeds mainly |
| --- | --- | --- |
| `role_operations/meeting_to_action/` | Raw meeting notes/transcript → decisions, owners, open items, a draft follow-up | Client & Stakeholder Engagement |
| `role_operations/status_rollup/` | Recent activity (commits, notebooks, notes) → a draft status update | Cross-cutting |
| `role_operations/rapid_scaffolder/` | A new prototype idea → a repo/notebook skeleton, data-contract stub, naive baseline | Innovation & Prototyping |
| `role_operations/prior_art_scanner/` | A hypothesis → related approaches, known failure modes, open questions | Framework Design |
| `role_operations/demo_narrative_packager/` | A prototype's results → situation/insight/recommendation narrative + one-pager | Client & Stakeholder Engagement |
| `role_operations/tough_question_rehearsal/` | Demo material → persona-grouped tough questions with suggested answers | Client & Stakeholder Engagement |
| `role_operations/experiment_ledger/` | Every prototype variant tried → an append-only, no-survivorship-bias log | Innovation & Prototyping |

## Shared Principles

Every role-operations agent upholds the constitution and
`instructions/role_operations.md`:

- **Configurable, not hardcoded.** Domain/platform awareness comes from
  `role_context.yml` or the live input — never a baked-in assumption.
- **No company-specific or personal data in this repository, ever** — not in
  a template, an example, or a test fixture.
- **Agents draft, the human decides.** Every output here is a first pass for
  review, never something sent, filed, or committed on the agent's own
  authority.
- **No fabrication.** A name, number, or decision absent from the input stays
  absent from the output — marked as a gap, not invented.
- **Data and visuals are traceable to source.** Actual data is used first;
  any figure, table, or chart this group produces cites its source at the
  point of use. Synthetic data is a documented last resort — every use is
  disclosed, completely, in a companion `synthetic_data_disclosure.md`
  (`templates/docs/synthetic_data_disclosure.md`), never a caveat buried in
  prose. See `instructions/data_provenance.md`.

## Where They Fit

`prior_art_scanner` feeds `research_analyst` (a lighter, faster first pass
before full research planning). `rapid_scaffolder` feeds `implementation` once
a prototype is approved to move toward production-grade code, and
`experiment_ledger` runs alongside it, logging every variant tried along the
way. `demo_narrative_packager` and `tough_question_rehearsal` run together
ahead of a demo: the narrative first, then the rehearsal against it.
`meeting_to_action` and `status_rollup` are cross-cutting and don't feed a
specific pillar agent — they clear the ambient overhead around all of them.

## Related

- `instructions/role_operations.md` — the shared standard behind this group.
- `templates/role_operations/role_context.yml` — the configuration template.
- `hooks/stages/role-context-check.sh` — the data-safety gate.
- `instructions/data_provenance.md` — the source-traceability and
  synthetic-data-disclosure standard this group's outputs follow.
- `templates/docs/synthetic_data_disclosure.md` — the companion disclosure
  report template.
- `agents/research_analyst/` — fuller research planning, downstream of
  `prior_art_scanner`.
