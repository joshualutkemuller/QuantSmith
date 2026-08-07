"""Compatibility alias for the moved agentic quant runtime.

Prefer importing from ``quantsmith.quant.agentic_quant`` in new code.
"""

from __future__ import annotations

import sys

from quantsmith.quant import agentic_quant as _runtime

sys.modules[__name__] = _runtime
