# Scheduler Profiles

The first deployment profile is cron because it is transparent, portable, and easy
to run on a local machine. It triggers the same deterministic executor used for
manual runs and writes draft artifacts locally.

No profile in this folder posts to X/Twitter.

## Cron

- Profile: `cron.md`
- Example crontab entry: `evening_quant_content.cron.example`
- Default cadence: daily at 10:30 PM America/New_York

Before using the crontab example locally, replace the repository path and output
directory with machine-specific locations.
