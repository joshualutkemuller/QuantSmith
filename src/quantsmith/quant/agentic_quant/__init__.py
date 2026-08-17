"""Agentic AI toolkit for quantitative finance.

Portfolio construction
  build_pipeline, run_workflow, build_sp500_pipeline, run_sp500_workflow

ML pipeline
  FeatureEngineeringAgent, ModelTrainingAgent, WalkForwardBacktestAgent
  AnomalyDetectionAgent, MLReportAgent

SQL data layer
  SQLDataSource, SQLiteDataSource, PostgreSQLDataSource, SQLServerDataSource
"""

# ---------------------------------------------------------------------------
# Core framework
# ---------------------------------------------------------------------------
from .framework import Blackboard, Agent, AgentPipeline

# ---------------------------------------------------------------------------
# Portfolio-side agents (existing)
# ---------------------------------------------------------------------------
from .agents import (
    MarketData,
    SignalReport,
    RiskReport,
    PortfolioPlan,
    DataAgent,
    YahooFinanceDataAgent,
    PandasDataReaderDataAgent,
    FactorSignalAgent,
    RiskAgent,
    PortfolioConstructionAgent,
    RiskOverlayAgent,
    ReportAgent,
)
from .rebalancing import (
    RebalancingOptimizationAgent,
    RebalancingReport,
    RebalancingScenario,
)
from .universes import get_sp500_tickers
from .workflow import (
    build_pipeline,
    build_sp500_pipeline,
    run_sp500_workflow,
    run_workflow,
)

# ---------------------------------------------------------------------------
# SQL data integration
# ---------------------------------------------------------------------------
from .sql_data import (
    SQLDataSource,
    SQLiteDataSource,
    PostgreSQLDataSource,
    SQLServerDataSource,
)

# ---------------------------------------------------------------------------
# ML pipeline agents
# ---------------------------------------------------------------------------
from .ml_agents import (
    FeatureSet,
    ModelArtifact,
    BacktestResult,
    FeatureEngineeringAgent,
    ModelTrainingAgent,
    WalkForwardBacktestAgent,
    AnomalyDetectionAgent,
    MLReportAgent,
)

__all__ = [
    # Framework
    "Blackboard",
    "Agent",
    "AgentPipeline",
    # Portfolio agents
    "MarketData",
    "SignalReport",
    "RiskReport",
    "PortfolioPlan",
    "DataAgent",
    "YahooFinanceDataAgent",
    "PandasDataReaderDataAgent",
    "FactorSignalAgent",
    "RiskAgent",
    "PortfolioConstructionAgent",
    "RiskOverlayAgent",
    "ReportAgent",
    "RebalancingOptimizationAgent",
    "RebalancingReport",
    "RebalancingScenario",
    "get_sp500_tickers",
    "build_pipeline",
    "build_sp500_pipeline",
    "run_workflow",
    "run_sp500_workflow",
    # SQL data layer
    "SQLDataSource",
    "SQLiteDataSource",
    "PostgreSQLDataSource",
    "SQLServerDataSource",
    # ML pipeline
    "FeatureSet",
    "ModelArtifact",
    "BacktestResult",
    "FeatureEngineeringAgent",
    "ModelTrainingAgent",
    "WalkForwardBacktestAgent",
    "AnomalyDetectionAgent",
    "MLReportAgent",
]
