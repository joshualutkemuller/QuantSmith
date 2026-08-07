# Evening Quant Content Twitter Workflow Pack

Root-level workflow pack for the non-posting evening quant X/Twitter content
pipeline. This folder is intentionally self-contained so it can later live on a
local machine and be ignored by Git without scattering private content workflow
state across the SDK.

## Contents

| Path | Purpose |
| --- | --- |
| `agents/content/` | Agent contracts for orchestration, market context, angle generation, post packaging, visuals, memes, claim review, and content memory. |
| `configs/evening_quant_content.yml` | Default schedule, platform limits, topic weights, review rules, memory path, and delivery target. |
| `runtime/evening_quant_pipeline.py` | Runnable deterministic draft-pack executor. |
| `scheduler/` | Cron deployment profile and example crontab entry. |
| `specs/0003-evening-quant-content-workflow/` | Original workflow contract and design spec. |
| `specs/0005-evening-quant-content-runnable-pipeline/` | Runtime pipeline spec. |
| `examples/evening_quant_content/` | Deterministic sample context and draft-pack fixture. |
| `templates/docs/evening_quant_draft_pack.md` | Human-readable draft-pack template. |
| `memory/evening_quant_content/` | Metadata-only workflow memory scaffold. |

## Manual Run

```sh
python evening_quant_content_twitter/runtime/evening_quant_pipeline.py \
  --config evening_quant_content_twitter/configs/evening_quant_content.yml \
  --context evening_quant_content_twitter/examples/evening_quant_content/context_sample.md \
  --output-dir /tmp/evening_quant_content_run
```

The executor writes:

- `draft_pack.yml`
- `draft_pack.md`

The workflow never posts automatically. The output remains a review artifact that
requires manual approval.
