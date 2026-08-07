# Evening Quant Content Runtime

The runtime executor is intentionally deterministic and dependency-light. It
turns a config plus optional context notes into a draft-pack artifact that follows
the `0003` output contract and satisfies the `0005` runnable-pipeline spec.

It does not:

- fetch live market/news data by itself;
- call an LLM;
- post to X/Twitter;
- store credentials or private desk context.

Run it from the repository root:

```sh
python evening_quant_content_twitter/runtime/evening_quant_pipeline.py \
  --config evening_quant_content_twitter/configs/evening_quant_content.yml \
  --context evening_quant_content_twitter/examples/evening_quant_content/context_sample.md \
  --output-dir /tmp/evening_quant_content_run
```
