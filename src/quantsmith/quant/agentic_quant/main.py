"""Command line entry point for running the agentic quant workflow."""

from __future__ import annotations

from .workflow import run_workflow


def main() -> None:
    report = run_workflow()
    print(report)


if __name__ == "__main__":
    main()
