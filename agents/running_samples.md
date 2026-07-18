# Running Samples and Capturing Output

This guide shows how to run sample prompts with the LI orchestrator CLI and where to find the output.

## Prerequisites

From the repository root:

```bash
cd /workspace/agentic_ds_quant_analytics_workflow
```

Use Python 3 and run commands from the project root so relative paths (`data/demo.sqlite`, `data/tableau_knowledge.json`) resolve correctly.

## 1) Run a Sample and Print Output to Terminal

```bash
python cli.py "Build a regional sales dashboard with profit trends"
```

What you will see:

- A formatted JSON payload printed to terminal.
- `plan` with execution steps and selected target dashboard platform.
- `data` rows and schema returned from SQL + data prep.
- `eda` summary from the EDA specialist agent.
- `tableau_dashboard` or `powerbi_dashboard` payload, depending on prompt intent.
- `report` summary text.

## 2) Save Output to a File

```bash
mkdir -p output
python cli.py "Build a portfolio management dashboard that helps visualize the clients allocations, exposures, risk metrics, performance, etc." > output/portfolio_dashboard.json
```

Then inspect the file:

```bash
head -n 40 output/portfolio_dashboard.json
```

Or pretty-print/validate JSON:

```bash
python -m json.tool output/portfolio_dashboard.json | head -n 60
```

## 3) Force PowerBI Path (Sample)

The current routing chooses PowerBI when the prompt contains the word `PowerBI`.

```bash
python cli.py "Build a PowerBI dashboard for client allocation and risk exposure"
```

You should see:

- `plan.metadata.target` set to `powerbi`
- `powerbi_dashboard` populated
- `tableau_dashboard` as `null`

## 4) Use Mode + LLM Provider Flags

```bash
python cli.py "Build a portfolio management dashboard" \
  --mode portfolio_management \
  --llm-provider langchain \
  --llm-model gpt-4o-mini
```

The output JSON includes mode and LLM metadata under `plan.metadata`.

## 5) Use Custom Database or Knowledge Base

```bash
python cli.py "Build a regional performance dashboard" \
  --db data/demo.sqlite \
  --kb data/tableau_knowledge.json
```

## 6) Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

## Troubleshooting

- If no output appears in terminal, check whether `>` redirection was used (output goes to file).
- If the command fails, verify current working directory is repository root.
- If JSON parsing fails, rerun command and inspect the first error line from terminal output.
