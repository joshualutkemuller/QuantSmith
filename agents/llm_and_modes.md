# LLM Providers and Analytical Workflow Modes

## Which LLM does this use today?

The current scaffold is **provider-agnostic** and runs in a deterministic rules-based mode by default (`--llm-provider none`).

You can still pass provider/model metadata to the orchestrator for environment wiring and future adapter hooks.

## Can this use other LLMs or LangChain?

Yes. The workflow now includes a provider-neutral LLM config interface (`LLMConfig`, `LLMRouter`) so you can set providers such as:

- `openai`
- `anthropic`
- `local`
- `langchain`
- any custom provider label used by your runtime adapter

Example command:

```bash
python cli.py "Build a portfolio management dashboard" --llm-provider langchain --llm-model gpt-4o-mini
```

> Note: this scaffold stores provider/model settings and exposes them in plan metadata. You can plug in actual LangChain chains/agents in a follow-up integration layer.

## Analytical Workflow Modes

The orchestrator supports explicit analytical workflow modes via `--mode`:

- `general`
- `portfolio_management`
- `securities_lending_collateral`
- `sales_specialist`
- `broad_data_scientist`

### Mode examples

```bash
python cli.py "Analyze exposure and allocation trends" --mode portfolio_management
python cli.py "Review lending utilization and haircut quality" --mode securities_lending_collateral
python cli.py "Build revenue trend dashboard by rep" --mode sales_specialist
python cli.py "Perform broad EDA on the dataset" --mode broad_data_scientist
```

## EDA Specialist Agent

An `eda-specialist-agent` is now part of the workflow and produces a lightweight EDA report including:

- row count and detected columns
- numeric min/max/mean summaries
- quick insight bullets for downstream reporting/dashboard steps
