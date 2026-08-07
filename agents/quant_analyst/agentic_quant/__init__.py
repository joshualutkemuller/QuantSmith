"""Legacy import shim for the packaged agentic quant runtime.

This keeps old commands run from ``agents/quant_analyst`` working while the real
implementation lives in ``src/quantsmith/quant/agentic_quant``.
"""

from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from quantsmith.quant import agentic_quant as _runtime

sys.modules[__name__] = _runtime
