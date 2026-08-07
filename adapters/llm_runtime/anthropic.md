# Anthropic LLM Runtime Adapter

## Use For

- Long-context review.
- Drafting and reasoning workflows where an approved Anthropic profile is
  available.
- Cross-provider comparison in evaluation workflows.

## Delivery Rules

- Use approved model profiles rather than hard-coded model names.
- Capture prompt URI, input artifacts, output artifact, model, and usage metadata.
- Enforce privacy and data-classification constraints before invocation.
- Record provider-specific stop, tool, and context settings in run metadata.

## Risks

- Cross-provider outputs can differ materially for the same prompt.
- Long-context runs can obscure which evidence drove the answer unless artifacts
  are cited and hashed.
