# Agentic Code Tools Runtime Shim

This directory is a compatibility shim only. The executable code lives in
`src/quantsmith/agentic_code_tools/`.

New code should import from `quantsmith.agentic_code_tools`. The legacy
`agents.agentic_code_tools` import path remains available temporarily for older
examples and notebooks.
