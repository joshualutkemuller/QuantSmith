# OpenAI LLM Runtime Adapter

## Use For

- Research planning.
- Draft generation.
- Extraction and classification.
- Review workflows that require structured output or tool use.

## Delivery Rules

- Use approved model profiles rather than hard-coded model names.
- Capture prompt URI, input artifacts, output artifact, model, and usage metadata.
- Enforce privacy constraints before invocation.
- Prefer structured outputs when the downstream workflow expects a contract.

## Risks

- Model/provider capabilities and pricing can change.
- Sensitive workflow inputs require explicit profile approval.
- Outputs still require agent-level review before operational use.
