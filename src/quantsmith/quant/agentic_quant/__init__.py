"""Agentic AI toolkit for quantitative finance.

Covers two complementary domains:

Portfolio construction (existing)
  build_pipeline, run_workflow, build_sp500_pipeline, run_sp500_workflow

Securities lending & trading desk support (new)
  build_sec_lending_pipeline, run_sec_lending_workflow
  build_sec_lending_demo_pipeline, run_sec_lending_demo
  build_combined_quant_pipeline

ML pipeline
  FeatureEngineeringAgent, ModelTrainingAgent, WalkForwardBacktestAgent
  BorrowDemandForecastAgent, AnomalyDetectionAgent, MLReportAgent

SQL data layer
  SQLDataSource, SQLiteDataSource, PostgreSQLDataSource, SQLServerDataSource
  SQLSecLendingDataAgent
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
    SQLSecLendingDataAgent,
    SecLendingRawData,
)

# ---------------------------------------------------------------------------
# Securities lending agents
# ---------------------------------------------------------------------------
from .sec_lending import (
    BorrowSecurity,
    LendingPosition,
    CounterpartyRisk,
    SecLendingUniverse,
    OptimizedAllocation,
    InventoryOptimizationResult,
    SecLendingUniverseAgent,
    BorrowRateAnalysisAgent,
    InventoryOptimizationAgent,
    SecLendingRiskAgent,
    SecLendingReportAgent,
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
    BorrowDemandForecastAgent,
    AnomalyDetectionAgent,
    MLReportAgent,
)

# ---------------------------------------------------------------------------
# Workflow builders
# ---------------------------------------------------------------------------
from .sec_lending_workflow import (
    build_sec_lending_pipeline,
    run_sec_lending_workflow,
    build_sec_lending_demo_pipeline,
    run_sec_lending_demo,
    build_combined_quant_pipeline,
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
    "SQLSecLendingDataAgent",
    "SecLendingRawData",
    # Securities lending agents
    "BorrowSecurity",
    "LendingPosition",
    "CounterpartyRisk",
    "SecLendingUniverse",
    "OptimizedAllocation",
    "InventoryOptimizationResult",
    "SecLendingUniverseAgent",
    "BorrowRateAnalysisAgent",
    "InventoryOptimizationAgent",
    "SecLendingRiskAgent",
    "SecLendingReportAgent",
    # ML pipeline
    "FeatureSet",
    "ModelArtifact",
    "BacktestResult",
    "FeatureEngineeringAgent",
    "ModelTrainingAgent",
    "WalkForwardBacktestAgent",
    "BorrowDemandForecastAgent",
    "AnomalyDetectionAgent",
    "MLReportAgent",
    # Workflow builders
    "build_sec_lending_pipeline",
    "run_sec_lending_workflow",
    "build_sec_lending_demo_pipeline",
    "run_sec_lending_demo",
    "build_combined_quant_pipeline",
]
