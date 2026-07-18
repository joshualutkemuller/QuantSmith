# Agentic Quant Framework

This repository contains an agentic AI framework for quantitative finance,
designed for quants supporting **securities lending teams and trading desks**.
Primary languages: Python (core) + SQL (data layer).

The framework consists of three integrated components:

1. **Portfolio construction** — classic mean-variance optimization in
   [`mean_variance.py`](mean_variance.py) plus an agentic pipeline in
   [`agentic_quant`](agentic_quant) (data → signal → risk → optimize → report).
2. **Securities lending workflow** — borrow-rate analysis, LP-based inventory
   optimization, counterparty/concentration risk, and ML demand forecasting,
   all backed by a SQL integration layer that works with SQLite, PostgreSQL,
   and SQL Server.
3. **ML pipeline** — feature engineering, model training, walk-forward
   backtesting, and anomaly detection, composable with any workflow above.

All three share the same **Blackboard / AgentPipeline** pattern so they can
be mixed, chained, or run independently.

---

## Quant Skills Library

See [`Quant Skills Library`](Quant%20Skills%20Library) for the system prompt
that drives AI-assisted development in this repo.  It documents each agent's
skills, coding conventions, and the four canonical workflow patterns:

| Pattern | Use case |
|---------|----------|
| Securities Lending Daily Report | Borrow-rate analytics, inventory opt, risk flags |
| Portfolio + Sec Lending (combined) | Full trading desk support |
| ML Signal Research | Feature engineering, model training, backtest |
| Risk Monitoring | Anomaly detection only |

---

## Securities Lending Workflow (new)

### Quick start (synthetic demo — no database required)

```bash
pip install numpy scipy
python run_sec_lending.py
```

The demo seeds an in-memory SQLite database with synthetic borrow rates,
lending positions, and recall data, then runs the full pipeline: universe
construction → borrow-rate analysis → LP inventory optimization → risk checks
→ ML demand forecast → report.

### Running against a real database

```python
from agentic_quant import run_sec_lending_workflow
from agentic_quant.sql_data import SQLiteDataSource  # or PostgreSQL / SQL Server

src = SQLiteDataSource("path/to/lending.db")
report = run_sec_lending_workflow(sql_source=src)
print(report)
```

For PostgreSQL:
```python
import os
from agentic_quant.sql_data import PostgreSQLDataSource

src = PostgreSQLDataSource(
    host=os.environ["PG_HOST"],
    dbname=os.environ["PG_DB"],
    user=os.environ["PG_USER"],
    password=os.environ["PG_PASS"],
)
report = run_sec_lending_workflow(sql_source=src)
```

For SQL Server (common in institutional environments) via pyodbc:
```python
import os
from agentic_quant.sql_data import SQLServerDataSource

src = SQLServerDataSource(
    dsn=(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.environ['MSSQL_HOST']};"
        f"DATABASE={os.environ['MSSQL_DB']};"
        "Trusted_Connection=yes;"
    )
)
```

### Command-line options

```bash
python run_sec_lending.py --help

# Key flags:
#   --db PATH              SQLite file (default: in-memory demo)
#   --max-book 500000000   Balance-sheet limit ($500M)
#   --max-cp-concentration 0.20  Counterparty concentration limit
#   --no-ml               Skip ML forecast and anomaly detection
#   --combined            Run portfolio + sec lending together
#   --tickers AAPL,MSFT,NVDA  Tickers for portfolio side
```

### Customising the pipeline

```python
from agentic_quant import (
    build_sec_lending_pipeline,
    SecLendingUniverseAgent,
    BorrowRateAnalysisAgent,
    InventoryOptimizationAgent,
    SecLendingRiskAgent,
    SecLendingReportAgent,
)

pipeline = build_sec_lending_pipeline(
    max_book_size=500_000_000,
    max_cp_concentration=0.20,
    squeeze_util_threshold=0.80,
    include_ml_forecast=False,
)
board = pipeline.run()
print(board["sec_lending_report"])

# Access structured data directly
universe = board["sec_lending_universe"]
for sec in universe.securities:
    if sec.classification == "HTB":
        print(f"{sec.ticker}: {sec.rate_bps:.0f} bps, util={sec.utilization:.1%}")

opt = board["inventory_optimization"]
print(f"Optimal daily fee: ${opt.total_expected_fee:,.2f}")
print(f"Solver: {opt.solver_status}")
```

### Inventory optimization (LP)

The `InventoryOptimizationAgent` maximises fee revenue subject to a
balance-sheet limit using `scipy.optimize.linprog` (HiGHS solver) with a
greedy fallback when scipy is unavailable.

```python
from agentic_quant import InventoryOptimizationAgent, build_sec_lending_pipeline

pipeline = build_sec_lending_pipeline(
    max_book_size=2_000_000_000,   # $2B limit
    max_cp_concentration=0.15,     # tighter counterparty limits
)
board = pipeline.run()
result = board["inventory_optimization"]
for alloc in result.allocations[:10]:
    print(f"{alloc.ticker}: {alloc.allocated_qty:,} shares → ${alloc.expected_fee:,.2f}/day")
```

---

## ML Pipeline

### Signal research (market data → model → backtest)

```python
from agentic_quant import (
    DataAgent,
    FeatureEngineeringAgent,
    ModelTrainingAgent,
    WalkForwardBacktestAgent,
    MLReportAgent,
    AgentPipeline,
)

pipeline = AgentPipeline([
    DataAgent(tickers=["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"], periods=504),
    FeatureEngineeringAgent(momentum_windows=[5, 21, 63], target_horizon=5),
    ModelTrainingAgent(train_pct=0.75),
    WalkForwardBacktestAgent(n_folds=5),
    MLReportAgent(),
])
board = pipeline.run()
print(board["ml_report"])

# Access artifacts
artifact = board["model_artifact"]
print(f"Val R²: {artifact.val_score:.4f}, IC: {artifact.metrics.get('ic', 0):.4f}")
```

### Plugging in your own sklearn model

```python
from sklearn.ensemble import RandomForestRegressor
from agentic_quant import ModelTrainingAgent

agent = ModelTrainingAgent(
    model_factory=lambda: RandomForestRegressor(n_estimators=200, max_depth=4),
    model_type="random_forest",
)
```

### Borrow demand forecasting

```python
from agentic_quant import BorrowDemandForecastAgent, build_sec_lending_pipeline

pipeline = build_sec_lending_pipeline(include_ml_forecast=True)
board = pipeline.run()
for forecast in board["borrow_demand_forecast"][:5]:
    print(f"{forecast['ticker']}: {forecast['predicted_demand']:,.0f} shares "
          f"({forecast['confidence']})")
```

### Anomaly detection

```python
from agentic_quant import AnomalyDetectionAgent

# Detects z-score outliers in returns and borrow rates
agent = AnomalyDetectionAgent(lookback=21, n_sigma=2.5)
```

---

## Combined Portfolio + Securities Lending

Run both workflows through a single blackboard pass:

```python
from agentic_quant import build_combined_quant_pipeline

pipeline = build_combined_quant_pipeline(
    portfolio_tickers=["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
    target_return=0.12,
    max_book_size=500_000_000,
)
board = pipeline.run()
print(board["report"])           # portfolio report
print(board["sec_lending_report"])  # sec lending report
```

Or from the command line:

```bash
python run_sec_lending.py --combined --tickers AAPL,MSFT,NVDA,TSLA
```

---

## Portfolio Construction (existing)

### Quick start

1. Ensure you have Python 3.9+ with NumPy installed.
2. Run the classic optimization example:

   ```bash
   python mean_variance.py
   ```

   The script prints the weights and risk/return characteristics of the global
   minimum variance portfolio, an efficient portfolio for a chosen target
   return, and a few points sampled from the efficient frontier.

3. Run the agentic workflow to see the autonomous pipeline in action:

   ```bash
   python -m agentic_quant.main
   ```

   You will receive a multi-section report summarizing simulated data, signal
   estimates, risk analytics, the resulting portfolio after a risk overlay
   agent applies leverage and concentration limits, and recommended
   rebalancing cadences based on historical drift and transaction cost
   assumptions.

   If you prefer to integrate the workflow into your own script or notebook
   without invoking the CLI entry point, import from `agentic_quant` directly.
   The package exposes both a ready-made `run_workflow` helper and a
   lower-level `build_pipeline` constructor if you want to customize agents
   before running them:

   ```python
   from agentic_quant import build_pipeline, run_workflow

   # One-liner that executes the default pipeline and returns the report text.
   report = run_workflow(target_return=0.12)
   print(report)

   # Or build the pipeline, swap or inspect agents, then execute manually.
   pipeline = build_pipeline(target_return=0.12)
   pipeline.append(MyCustomAgent())
   board = pipeline.run()
   print(board["report"])
   print(board.get("rebalancing_report"))
   ```

### Using real market data via Yahoo Finance

The default pipeline relies on a synthetic `DataAgent` that generates lognormal
price paths.  To work with real equities, install the optional dependencies and
swap in the `YahooFinanceDataAgent` when constructing the workflow:

```bash
pip install yfinance pandas beautifulsoup4
```

```python
from agentic_quant import YahooFinanceDataAgent, run_workflow

tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
data_agent = YahooFinanceDataAgent(tickers, period="3y", min_history=252)

report = run_workflow(tickers=tickers, data_agent=data_agent)
print(report)
```

The Yahoo-backed agent downloads adjusted close prices, enforces a minimum
history length, and passes the resulting numpy arrays to the downstream signal
and risk agents.  You can customize parameters such as `start`/`end` dates,
`period`, or `interval` to align with your research horizon.

### Pulling prices with pandas_datareader

If your environment already uses `pandas_datareader`, swap in the
`PandasDataReaderDataAgent` and optionally call the dedicated runner script
[`run_sp500.py`](run_sp500.py).  The agent defaults to the "stooq" data source
but supports any backend accepted by `pandas_datareader.DataReader`:

```bash
pip install pandas pandas_datareader beautifulsoup4 requests
```

```python
from agentic_quant import PandasDataReaderDataAgent, build_pipeline, get_sp500_tickers

tickers = get_sp500_tickers(limit=50)
data_agent = PandasDataReaderDataAgent(
    tickers,
    data_source="stooq",
    min_history=252,
    skip_failed=True,
)

pipeline = build_pipeline(tickers=tickers, data_agent=data_agent)
board = pipeline.run()
print(board["report"])
print(board.get("data_warnings", {}))
```

Running the included `run_sp500.py` script wraps the same setup in a CLI.  Any
tickers that fail to download are automatically dropped (with a warning on
stderr) so transient outages or partial coverage from the selected backend do
not halt the entire workflow.  You can also tune the rebalancing analysis from
the command line—override the default trading-day cadences, change the assumed
per-unit transaction cost, or disable the simulation entirely if desired:

```bash
python run_sp500.py \
    --max-tickers 50 \
    --data-source stooq \
    --min-history 300 \
    --rebalance-frequencies 1,5,21,63 \
    --transaction-cost 0.0005
```

The script fetches the current S&P 500 constituents from Wikipedia before
requesting daily closes via `pandas_datareader`, making it easy to switch
between data providers without touching the rest of the workflow.

When no explicit `--start`/`--end` dates are supplied, the runner defaults to a
five-year window ending today.  If you pass a future start or end date, the
agent automatically clamps the request to the latest available trading session
and records the adjustment under `data_warnings` so you can confirm the
resolved download range.

### Optimizing rebalancing strategies

Every pipeline constructed through `build_pipeline` now includes a
`RebalancingOptimizationAgent` by default.  The agent simulates portfolio drift
under multiple trading-day cadences, estimates the turnover required to return
to the target allocation, and computes the net performance impact after applying
per-unit transaction costs.  The synthesized report highlights the recommended
rebalancing frequency, while the full diagnostics are stored on the blackboard
under `"rebalancing_report"` for programmatic consumption:

```python
from agentic_quant import build_pipeline

pipeline = build_pipeline(
    target_return=0.1,
    rebalancing_frequencies=(1, 5, 10, 21, 63),
    transaction_cost=0.00025,
)
board = pipeline.run()
print(board["report"])
print(board["rebalancing_report"].recommended_frequency)
```

If you prefer to handle rebalancing externally, disable the agent by passing
`optimize_rebalancing=False` to `build_pipeline`, `run_workflow`, or the S&P 500
helpers.  This keeps the legacy report structure intact while still allowing you
to plug in alternative post-processing steps.

For a dedicated command-line demo that prints the rebalancing summary alongside
the full workflow report, run the included helper script.  It accepts the same
frequency and transaction-cost knobs as the pipeline constructor:

```bash
python run_rebalancer.py --rebalance-frequencies 5,21,63 --transaction-cost 0.00025
```

The script emits the recommended cadence and detailed turnover statistics to
stdout so you can quickly compare scenarios without wiring up your own harness.

### Optimizing an S&P 500 universe

To spin up the full pipeline with the current S&P 500 constituents, leverage
the helper utilities exposed at the package root.  They scrape the official
Wikipedia constituents table to build the ticker universe and then stream
historical prices from Yahoo Finance into the workflow automatically (an
internet connection is required for both steps):

```python
from agentic_quant import run_sp500_workflow

# Run against the entire index with five years of daily history.
report = run_sp500_workflow(target_return=0.10)
print(report)
```

If you would like to prototype with a smaller slice of the index, supply
`max_tickers` when building the pipeline.  The helper ensures the identifiers
are normalized (e.g., converting `BRK.B` to the Yahoo-compatible `BRK-B`) and
will raise an informative error if the optional dependencies (``requests`` and
``beautifulsoup4`` in addition to ``yfinance``/``pandas``) are missing.  You can
also access the raw list of constituents with `get_sp500_tickers()` if you want
to perform custom filtering before wiring up the workflow.

## Extending the model

The `MeanVarianceOptimizer` class offers the following methods you can reuse in
other workflows:

* `global_minimum_variance_weights()` – Compute the minimum-variance portfolio
  satisfying the full-investment constraint.
* `efficient_weights(target_return)` – Generate the weights that minimize
  variance for a requested expected return.
* `efficient_frontier(num_points=20)` – Sample points along the efficient
  frontier to visualize the trade-off between risk and return.
* `portfolio_performance(weights)` – Evaluate the expected return and
  volatility of any portfolio weights.

These building blocks can be integrated into more sophisticated investment or
risk analysis pipelines.  The agentic toolkit builds directly on top of this
optimizer, giving you a template for orchestrating autonomous research
workflows in quantitative finance.  You can customize the agents in
[`agentic_quant/agents.py`](agentic_quant/agents.py) to plug in live data,
alternative alpha models, or bespoke risk overlays.
