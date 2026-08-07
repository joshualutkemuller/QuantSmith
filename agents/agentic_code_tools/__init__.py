"""Legacy import shim for packaged agentic code tools.

Prefer ``quantsmith.agentic_code_tools`` in new code.
"""

from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from quantsmith import agentic_code_tools as _runtime

sys.modules[__name__] = _runtime
