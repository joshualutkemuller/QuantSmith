# Plan: Evening Quant Content Runnable Pipeline

- **Spec:** 0005-evening-quant-content-runnable-pipeline (`spec.md`)
- **Status:** Implemented
- **Author:** QuantSmith
- **Last updated:** 2026-08-07

> HOW. Requires the approved `spec.md`.

## Approach

Implement the smallest useful runtime loop that can execute the `0003` draft-pack
contract without pretending to be a live research or posting system. The executor
loads config, optional context, and memory, generates deterministic candidate
content, validates safety constraints, and writes YAML plus Markdown artifacts.

## Architecture & Components

```text
config + optional context + memory
  -> runtime/evening_quant_pipeline.py
  -> validation
  -> draft_pack.yml + draft_pack.md
```

| Component | Responsibility |
| --- | --- |
| `runtime/evening_quant_pipeline.py` | CLI, scoped config loading, context parsing, deterministic draft-pack generation, validation, and local artifact writes. |
| `examples/evening_quant_content/context_sample.md` | No-live-data context fixture used by humans and the advisory gate. |
| `scheduler/cron.md` | Deployment profile for daily local execution. |
| `scheduler/evening_quant_content.cron.example` | Copyable crontab entry with local path placeholders. |
| `hooks/stages/content-draft-pack-check.sh` | Structural and smoke-test gate for the pack. |

## Interfaces & Data Contracts

### CLI

```sh
python evening_quant_content_twitter/runtime/evening_quant_pipeline.py \
  --config evening_quant_content_twitter/configs/evening_quant_content.yml \
  --context evening_quant_content_twitter/examples/evening_quant_content/context_sample.md \
  --output-dir /tmp/evening_quant_content_run \
  --generated-at 2026-08-07T22:30:00-04:00
```

### Output

- `draft_pack.yml`
- `draft_pack.md`

Both outputs include run metadata, source notes, review findings, manual approval
flags, ranked ideas, finished posts, thread drafts, visual specs, meme concepts,
deferred ideas, and memory updates.

## Traceability Matrix

| Requirement | Design element | Tasks |
| --- | --- | --- |
| REQ-001 | CLI parser and runtime README | T-001, T-006 |
| REQ-002 | Config loader and content counts | T-001, T-002 |
| REQ-003 | Context loader and source-note builder | T-002, T-003 |
| REQ-004 | Draft-pack builder | T-003 |
| REQ-005 | Runtime validator and content gate smoke test | T-004, T-007 |
| REQ-006 | Manual approval/autopost validation | T-004 |
| REQ-007 | Local artifact writer | T-005 |
| REQ-008 | Cron profile and example crontab | T-006 |
| NFR-001 | Fixed timestamp CLI argument | T-001, T-007 |
| NFR-002 | Standard-library implementation | T-001 |
| NFR-003 | Non-posting validation and scheduler notes | T-004, T-006 |
| NFR-004 | Markdown/YAML local outputs | T-005 |

## Validation Strategy

- `python evening_quant_content_twitter/runtime/evening_quant_pipeline.py ...`
  smoke-runs the executor.
- `content-draft-pack-check` verifies required pack files and runs the smoke test.
- `spec` traces `0003` and `0005` under the workflow pack.
- `docs-link` verifies relative Markdown links.
- `git diff --check` catches whitespace issues.

## Rollout & Rollback

Rollout is additive inside `evening_quant_content_twitter/`. The scheduler profile
is documentation plus an example crontab entry; it does not install itself.
Rollback is removing the crontab locally or reverting the pack changes.

## Open Questions

- Should the next runtime slice add live source adapters or LLM-backed generation?
- Should generated outputs remain outside Git by convention once the pack is
  ignored locally?
