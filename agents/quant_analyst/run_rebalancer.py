"""Synthetic workflow runner focused on the rebalancing optimization agent."""

from __future__ import annotations

import argparse
import json
from typing import Optional, Sequence

from agentic_quant import build_pipeline


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
            "Run the synthetic agentic workflow and surface detailed rebalancing "
            "statistics without configuring an external data source."
        )
    )
    parser.add_argument(
        "--target-return",
        type=float,
        default=0.12,
        help="Desired annualized return target for the optimizer.",
    )
    parser.add_argument(
        "--periods",
        type=int,
        default=756,
        help="Number of synthetic observations to generate (252 trading days * 3 years).",
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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the rebalancing diagnostics as JSON instead of a formatted table.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    optimize_rebalancing = not args.skip_rebalancing
    frequencies: Sequence[int] | None = args.rebalance_frequencies
    pipeline = build_pipeline(
        target_return=args.target_return,
        periods=args.periods,
        optimize_rebalancing=optimize_rebalancing,
        rebalancing_frequencies=frequencies,
        transaction_cost=args.transaction_cost,
    )

    board = pipeline.run()
    report = board["report"]
    print(report)

    if optimize_rebalancing:
        rebalancing_report = board.get("rebalancing_report")
        if rebalancing_report is None:
            print("No rebalancing diagnostics were produced.")
        elif args.json:
            print(json.dumps(rebalancing_report.as_dict(), indent=2))
        else:
            print("\nRebalancing diagnostics:")
            print(rebalancing_report.pretty_format())
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution entry point
    raise SystemExit(main())
