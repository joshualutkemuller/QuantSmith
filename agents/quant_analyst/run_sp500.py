"""Runner script for executing the S&P 500 agentic workflow via pandas_datareader."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from agentic_quant import (
    PandasDataReaderDataAgent,
    build_pipeline,
    get_sp500_tickers,
)


def _parse_frequency_list(value: str) -> list[int]:
    parts = [segment.strip() for segment in value.split(",")]
    frequencies: list[int] = []
    for part in parts:
        if not part:
            continue
        try:
            frequency = int(part)
        except ValueError as exc:  # pragma: no cover - argparse validation
            raise argparse.ArgumentTypeError(
                f"Invalid rebalance frequency '{part}'. Expected integers."
            ) from exc
        if frequency <= 0:
            raise argparse.ArgumentTypeError(
                "Rebalance frequencies must be positive integers."
            )
        frequencies.append(frequency)
    if not frequencies:
        raise argparse.ArgumentTypeError(
            "At least one rebalance frequency must be provided."
        )
    return frequencies


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute the agentic quant workflow configured for the current "
            "S&P 500 universe using pandas_datareader to source historical prices."
        )
    )
    parser.add_argument(
        "--max-tickers",
        type=int,
        default=None,
        help=(
            "Limit the number of S&P 500 constituents fetched. Useful for "
            "prototyping or reducing runtime."
        ),
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start date (YYYY-MM-DD) for price history. Defaults to 5 years ago.",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Explicit end date (YYYY-MM-DD) for price history.",
    )
    parser.add_argument(
        "--data-source",
        type=str,
        default="stooq",
        help=(
            "pandas_datareader source to use (e.g., 'stooq', 'av', 'fred'). "
            "Defaults to 'stooq'."
        ),
    )
    parser.add_argument(
        "--min-history",
        type=int,
        default=252,
        help="Minimum number of observations required for each ticker.",
    )
    parser.add_argument(
        "--target-return",
        type=float,
        default=0.12,
        help="Desired annualized return target for the optimizer.",
    )
    parser.add_argument(
        "--rebalance-frequencies",
        type=_parse_frequency_list,
        default=None,
        help=(
            "Comma-separated list of trading-day intervals to evaluate when "
            "optimizing rebalancing (defaults to 1,5,21,63)."
        ),
    )
    parser.add_argument(
        "--transaction-cost",
        type=float,
        default=0.001,
        help=(
            "Per-unit transaction cost applied to rebalancing turnover "
            "(e.g., 0.001 = 10 basis points)."
        ),
    )
    parser.add_argument(
        "--skip-rebalancing",
        action="store_true",
        help="Disable the rebalancing optimization agent.",
    )

    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    tickers = get_sp500_tickers(limit=args.max_tickers)
    data_agent = PandasDataReaderDataAgent(
        tickers,
        data_source=args.data_source,
        start=args.start,
        end=args.end,
        min_history=args.min_history,
    )
    optimize_rebalancing = not args.skip_rebalancing
    frequencies: Sequence[int] | None = args.rebalance_frequencies
    pipeline = build_pipeline(
        tickers=tickers,
        periods=args.min_history + 1,
        target_return=args.target_return,
        data_agent=data_agent,
        optimize_rebalancing=optimize_rebalancing,
        rebalancing_frequencies=frequencies,
        transaction_cost=args.transaction_cost,
    )
    board = pipeline.run()
    warnings = board.get("data_warnings")
    if warnings and warnings.get("missing_tickers"):
        dropped = ", ".join(warnings["missing_tickers"][:10])
        extra = "" if len(warnings["missing_tickers"]) <= 10 else " (truncated)"
        print(
            "Warning: dropped tickers with insufficient data: "
            f"{dropped}{extra}",
            file=sys.stderr,
        )
    rebalancing_report = board.get("rebalancing_report")
    if rebalancing_report and not args.skip_rebalancing:
        print(
            "Recommended rebalance frequency: every "
            f"{rebalancing_report.recommended_frequency} trading days",
            file=sys.stderr,
        )
    report = board["report"]
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
