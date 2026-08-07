# BLS API Profile

## Use For

- Labor market, CPI, PPI, wage, productivity, employment, and survey datasets
  from the U.S. Bureau of Labor Statistics.
- Scheduled macro releases used in daily briefings, regime classification,
  factor research, or model features.

## Required Metadata

- `series_id`
- `survey_code`
- `period`
- `year`
- `release_date`
- `revision_date` when available
- `seasonal_adjustment`
- `units`
- `retrieved_at_utc`
- `source_url`

## Delivery Rules

- Keep BLS series IDs intact; parse survey, seasonal adjustment, area, item, and
  data-type components only into additional fields.
- Store annual averages and monthly observations separately when both are
  returned.
- Preserve footnotes, preliminary flags, and data quality notes.
- Record request batch boundaries because API limits can shape retry behavior.
- Use release calendars when aligning observations to trading or reporting dates.

## Risks

- CPI, jobs, wages, and productivity series may be revised after initial release.
- Annual averages can be accidentally joined as if they were monthly readings.
- Survey-specific definitions differ and should not be blended without an
  explicit transformation layer.
