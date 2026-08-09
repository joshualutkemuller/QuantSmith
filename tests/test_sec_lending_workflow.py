"""Acceptance tests for spec 0023 — securities lending workflow.

Each test is named for the acceptance criterion it covers (see
``specs/0023-securities-lending-workflow/tasks.md``). Exercises the existing
agentic pipeline under ``quantsmith.quant.agentic_quant`` (numpy required;
scipy optional — the greedy fallback is exercised directly since this
environment has scipy installed).
"""

from __future__ import annotations

import numpy as np
import pytest

from quantsmith.quant.agentic_quant.framework import Blackboard
from quantsmith.quant.agentic_quant.sec_lending import (
    BorrowRateAnalysisAgent,
    InventoryOptimizationAgent,
    SecLendingRiskAgent,
    SecLendingUniverseAgent,
)
from quantsmith.quant.agentic_quant.sec_lending_workflow import (
    build_sec_lending_demo_pipeline,
    run_sec_lending_demo,
)


def _seeded_universe_board(seed: int = 42, n: int = 10) -> Blackboard:
    board = Blackboard()
    SecLendingUniverseAgent(synthetic_n=n, seed=seed).run(board)
    return board


# --- AC-001: deterministic synthetic universe construction ---


def test_universe_construction_is_deterministic_AC_001():
    board_a = _seeded_universe_board(seed=42)
    board_b = _seeded_universe_board(seed=42)

    universe_a = board_a["sec_lending_universe"]
    universe_b = board_b["sec_lending_universe"]

    assert universe_a.total_book_balance == universe_b.total_book_balance
    assert universe_a.total_daily_fee == universe_b.total_daily_fee
    assert [s.classification for s in universe_a.securities] == [
        s.classification for s in universe_b.securities
    ]

    # A different seed produces a different book (sanity: not a constant).
    board_c = _seeded_universe_board(seed=7)
    universe_c = board_c["sec_lending_universe"]
    assert universe_c.total_book_balance != universe_a.total_book_balance


# --- AC-002: borrow-rate analysis surfaces squeeze and rate-spike candidates ---


def test_borrow_rate_analysis_flags_squeeze_and_spikes_AC_002():
    board = _seeded_universe_board(seed=42)
    universe = board["sec_lending_universe"]

    BorrowRateAnalysisAgent(
        squeeze_util_threshold=0.85, rate_spike_factor=1.30
    ).run(board)
    analysis = board["borrow_rate_analysis"]

    expected_squeeze = {
        s.ticker for s in universe.securities if s.utilization >= 0.85
    }
    expected_spikes = {
        s.ticker
        for s in universe.securities
        if s.rate_30d_avg > 0 and s.rate_bps >= s.rate_30d_avg * 1.30
    }

    assert set(analysis["squeeze_candidates"]) == expected_squeeze
    assert set(analysis["rate_spike_securities"]) == expected_spikes
    assert analysis["classification_counts"]["GC"] + analysis[
        "classification_counts"
    ]["WARM"] + analysis["classification_counts"]["HTB"] == len(universe.securities)


# --- AC-003: inventory optimization respects the balance-sheet cap on both paths ---


def test_inventory_optimization_respects_balance_sheet_cap_AC_003():
    cap = 2_000_000.0
    board = _seeded_universe_board(seed=42)
    universe = board["sec_lending_universe"]

    agent = InventoryOptimizationAgent(max_book_size=cap, assumed_price=100.0)
    agent.run(board)
    result = board["inventory_optimization"]

    total_notional = sum(a.allocated_qty * 100.0 for a in result.allocations)
    assert total_notional <= cap + 1e-6
    assert result.solver_status in ("optimal", "greedy_fallback", "greedy_scipy_missing")

    # The greedy fallback (scipy unavailable / LP infeasible) must respect the
    # same cap; exercised directly since scipy is installed in this environment.
    notional = np.array([s.availability * 100.0 for s in universe.securities])
    fee_per_notional = np.array(
        [s.rate_bps / 10_000 / 252 for s in universe.securities]
    )
    x = InventoryOptimizationAgent._greedy(notional, fee_per_notional, cap)
    assert float((notional * x).sum()) <= cap + 1e-6
    assert (x >= 0).all() and (x <= 1).all()


# --- AC-004: risk agent flags counterparty and single-name concentration breaches ---


def test_risk_agent_flags_concentration_breaches_AC_004():
    board = _seeded_universe_board(seed=42)
    universe = board["sec_lending_universe"]

    # Tight thresholds guarantee at least one breach in the synthetic book.
    SecLendingRiskAgent(
        max_cp_concentration=0.01, max_single_name_pct=0.01, htb_alert_pct=0.01
    ).run(board)
    risk = board["sec_lending_risk"]

    assert len(risk["counterparty_breaches"]) > 0
    assert len(risk["single_name_breaches"]) > 0
    assert risk["recall_count"] == universe.recall_count

    # Loose thresholds on the same book must clear.
    board_loose = _seeded_universe_board(seed=42)
    SecLendingRiskAgent(
        max_cp_concentration=1.0, max_single_name_pct=1.0, htb_alert_pct=1.0
    ).run(board_loose)
    risk_loose = board_loose["sec_lending_risk"]
    assert risk_loose["counterparty_breaches"] == []
    assert risk_loose["single_name_breaches"] == []
    assert risk_loose["htb_alert"] is False


# --- AC-005: the full demo pipeline runs end to end and reports honestly ---


def test_demo_pipeline_runs_end_to_end_AC_005():
    report = run_sec_lending_demo()

    assert "Securities Lending Workflow Report" in report
    assert "Borrow Classification Breakdown" in report
    assert "Risk Flags" in report
    assert "Total book balance" in report

    pipeline = build_sec_lending_demo_pipeline()
    board = pipeline.run()
    assert board.get("sec_lending_risk") is not None
    assert board.get("inventory_optimization") is not None
