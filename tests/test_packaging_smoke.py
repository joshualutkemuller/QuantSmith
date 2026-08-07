from __future__ import annotations


def test_quantsmith_agentic_quant_imports() -> None:
    from quantsmith.quant.agentic_quant import AgentPipeline, build_pipeline

    pipeline = build_pipeline(periods=30)

    assert AgentPipeline is not None
    assert len(list(pipeline)) > 0


def test_legacy_agentic_quant_alias_imports() -> None:
    from agentic_quant import build_pipeline
    from agentic_quant.sql_data import SQLiteDataSource

    src = SQLiteDataSource(":memory:")
    src.seed_demo_data()

    assert build_pipeline(periods=30) is not None
    assert src is not None


def test_agentic_code_tools_package_imports() -> None:
    from quantsmith.agentic_code_tools import LIOrchestratorAgent, UserRequest

    assert LIOrchestratorAgent is not None
    assert UserRequest(prompt="Build a dashboard").prompt == "Build a dashboard"
