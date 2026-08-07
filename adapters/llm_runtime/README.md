# LLM Runtime Adapters

LLM runtime adapters normalize provider execution for workflows that use language
models. They do not own prompts, evaluation, policy, or final decisions.

## Files

| File | Purpose |
| --- | --- |
| `adapter_contract.md` | Provider-neutral model invocation and result schema. |
| `openai.md` | OpenAI model runtime profile. |
| `anthropic.md` | Anthropic model runtime profile. |
| `local_model.md` | Local or self-hosted model runtime profile. |

## Design Rule

Agents own task framing and review. Runtime adapters own provider selection,
request formatting, rate limits, retries, token accounting, and response metadata.
