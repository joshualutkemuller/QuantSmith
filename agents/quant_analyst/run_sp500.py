#!/usr/bin/env python3
"""Legacy wrapper for ``quantsmith-sp500``."""

from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from quantsmith.quant.agentic_quant.cli.sp500 import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
