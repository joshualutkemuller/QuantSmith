"""Executable adapters — the boundary between rendered payloads and live artifacts.

Adapter *contracts* are documented under the repo-root ``adapters/`` tree; this package
holds executable provider implementations. Optional third-party dependencies (e.g.
``openpyxl``) are imported lazily so importing a provider never requires them.
"""
