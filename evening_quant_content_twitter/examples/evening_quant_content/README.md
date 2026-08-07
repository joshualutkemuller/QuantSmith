# Evening Quant Content Example

This example is a deterministic, no-live-data fixture for the evening quant content
workflow. It demonstrates the draft-pack contract without fetching current news,
posting to any platform, or using private desk context.

- `sample_draft_pack.yml` shows the expected output shape.
- `evening_quant_content_twitter/configs/evening_quant_content.yml` controls the production workflow settings.
- `context_sample.md` provides deterministic input notes for the runtime smoke
  test.
- `evening_quant_content_twitter/templates/docs/evening_quant_draft_pack.md` is the human-readable delivery
  template.

Use this as a structural test fixture, not as current market commentary.
