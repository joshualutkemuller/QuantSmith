# Cron Deployment Profile: Evening Quant Content

## Purpose

Run the evening quant content draft-pack pipeline at the configured schedule and
write local artifacts for manual review. This is a scheduler profile, not a social
posting integration.

## Command

Run from the repository root:

```sh
python evening_quant_content_twitter/runtime/evening_quant_pipeline.py \
  --config evening_quant_content_twitter/configs/evening_quant_content.yml \
  --context evening_quant_content_twitter/examples/evening_quant_content/context_sample.md \
  --output-dir evening_quant_content_twitter/output/$(date +\%Y-\%m-\%d)
```

## Schedule

The default config expresses:

- frequency: daily
- time: `22:30`
- timezone: `America/New_York`

Cron itself uses the machine's local timezone unless configured otherwise. On a
local machine, set the host timezone to Eastern or convert the schedule explicitly.

## Safety Controls

- `auto_post_enabled` must remain `false`.
- `require_manual_approval` must remain `true`.
- The command writes draft artifacts only.
- Logs must not include credentials, private desk context, client details, MNPI, or
  private inventory/position information.

## Expected Outputs

- `draft_pack.yml`
- `draft_pack.md`

## Rollback

Remove or comment the crontab entry. No external platform state is mutated.
