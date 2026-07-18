#!/usr/bin/env python3
"""Demo runner for the securities lending agentic workflow.

Runs the full pipeline against an in-memory SQLite database seeded with
synthetic borrow rates, lending positions, and recall activity — no external
data dependencies required.

Usage
-----
  python run_sec_lending.py                        # default synthetic demo
  python run_sec_lending.py --db path/to/lend.db  # local SQLite file
  python run_sec_lending.py --max-book 500000000   # custom book limit ($500M)
  python run_sec_lending.py --no-ml               # skip ML demand forecast
  python run_sec_lending.py --combined            # portfolio + sec lending
"""

from __future__ import annotations

import argparse
import sys


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run the agentic securities lending workflow."
    )
    p.add_argument(
        "--db",
        metavar="PATH",
        default=None,
        help="Path to a SQLite database file.  Defaults to a seeded in-memory DB.",
    )
    p.add_argument(
        "--max-book",
        metavar="USD",
        type=float,
        default=1_000_000_000,
        help="Maximum lending book balance-sheet limit (default: $1B).",
    )
    p.add_argument(
        "--max-cp-concentration",
        metavar="FRAC",
        type=float,
        default=0.25,
        help="Maximum counterparty concentration fraction (default: 0.25).",
    )
    p.add_argument(
        "--squeeze-threshold",
        metavar="FRAC",
        type=float,
        default=0.85,
        help="Utilization threshold for supply-squeeze alerts (default: 0.85).",
    )
    p.add_argument(
        "--lookback-days",
        metavar="N",
        type=int,
        default=30,
        help="Days of borrow-rate history to pull from SQL (default: 30).",
    )
    p.add_argument(
        "--no-ml",
        action="store_true",
        help="Skip the ML demand forecast and anomaly detection agents.",
    )
    p.add_argument(
        "--combined",
        action="store_true",
        help="Run the combined portfolio + securities lending pipeline.",
    )
    p.add_argument(
        "--tickers",
        metavar="TICKERS",
        default="AAPL,MSFT,GOOGL,AMZN,NVDA",
        help="Comma-separated tickers for the portfolio side (--combined only).",
    )
    p.add_argument(
        "--target-return",
        metavar="FLOAT",
        type=float,
        default=0.12,
        help="Target annualised return for portfolio construction (default: 0.12).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    from agentic_quant.sql_data import SQLiteDataSource

    # Set up the SQL source
    if args.db:
        print(f"Connecting to SQLite database: {args.db}")
        src = SQLiteDataSource(args.db)
    else:
        print("Using seeded in-memory SQLite database (synthetic data).")
        src = SQLiteDataSource(":memory:")
        src.seed_demo_data()

    if args.combined:
        _run_combined(args, src)
    else:
        _run_sec_lending(args, src)


def _run_sec_lending(args: argparse.Namespace, src: object) -> None:
    from agentic_quant.sec_lending_workflow import build_sec_lending_pipeline

    print("\nBuilding securities lending pipeline…")
    pipeline = build_sec_lending_pipeline(
        sql_source=src,
        lookback_days=args.lookback_days,
        max_book_size=args.max_book,
        max_cp_concentration=args.max_cp_concentration,
        squeeze_util_threshold=args.squeeze_threshold,
        include_ml_forecast=not args.no_ml,
        include_anomaly_detection=not args.no_ml,
    )

    print("Running agents:")
    for agent in pipeline:
        print(f"  • {agent.name}")

    print()
    board = pipeline.run()

    report: str = board.get("sec_lending_report", "(no report generated)")
    print(report)

    # Also print anomaly flags separately if present
    anomalies = board.get("anomaly_flags")
    if anomalies:
        ra = anomalies.get("return_anomalies", [])
        rate_a = anomalies.get("rate_anomalies", [])
        if ra or rate_a:
            print("\n--- Anomaly Detail ---")
            for a in ra:
                print(f"  Return anomaly: {a['ticker']}  z={a['z_score']:+.2f}")
            for a in rate_a:
                print(
                    f"  Rate anomaly:   {a['ticker']}  z={a['z_score']:+.2f}  "
                    f"current={a['current_rate_bps']:.0f} bps"
                )


def _run_combined(args: argparse.Namespace, src: object) -> None:
    from agentic_quant.sec_lending_workflow import build_combined_quant_pipeline

    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    print(f"\nBuilding combined pipeline (portfolio: {tickers})…")

    pipeline = build_combined_quant_pipeline(
        portfolio_tickers=tickers,
        target_return=args.target_return,
        sql_source=src,
        max_book_size=args.max_book,
    )

    print("Running agents:")
    for agent in pipeline:
        print(f"  • {agent.name}")

    print()
    board = pipeline.run()

    port_report: str = board.get("report", "")
    sec_report: str = board.get("sec_lending_report", "")

    if port_report:
        print(port_report)
    if sec_report:
        print()
        print(sec_report)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
