"""Utilities for working with investable universes."""

from __future__ import annotations

from typing import Iterable, List


WIKIPEDIA_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def get_sp500_tickers(limit: int | None = None) -> List[str]:
    """Return the current S&P 500 constituents as Yahoo Finance tickers.

    The tickers are sourced from the official S&P 500 constituents table hosted
    on Wikipedia.  Identifiers that contain periods are normalized to the
    hyphenated variants that Yahoo Finance expects (for example ``BRK-B``
    instead of ``BRK.B``).  Duplicates are removed while preserving the order
    published in the source table.

    Args:
        limit: Optionally cap the number of tickers that are returned.  This can
            be useful for prototyping or reducing the size of downstream data
            downloads.  When ``None`` (the default), all tickers are returned.

    Returns:
        A list of normalized ticker symbols ready to be passed to
        :class:`~agentic_quant.agents.YahooFinanceDataAgent` or other agents.

    Raises:
        RuntimeError: If the required HTML parsing dependencies are missing or
            the constituents table cannot be retrieved from Wikipedia.
        ValueError: If ``limit`` is provided but not positive, or if the
            Wikipedia table contains no tickers after normalization.
    """

    if limit is not None and limit <= 0:
        raise ValueError("limit must be positive when provided")

    try:
        import requests  # type: ignore
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError as exc:  # pragma: no cover - defensive import
        raise RuntimeError(
            "requests and beautifulsoup4 are required to retrieve the S&P 500 universe"
        ) from exc

    try:
        response = requests.get(
            WIKIPEDIA_SP500_URL,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; AgenticQuant/1.0; +https://github.com/)"
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            "Failed to download the S&P 500 constituents from Wikipedia"
        ) from exc

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if table is None:
        raise RuntimeError(
            "Unable to locate the S&P 500 constituents table on the Wikipedia page"
        )

    body = table.find("tbody") or table
    rows = body.find_all("tr") if body else []
    raw_tickers: Iterable[str] = []
    symbols: List[str] = []
    for row in rows:
        cells = row.find_all("td")
        if not cells:
            continue
        ticker = cells[0].get_text(strip=True)
        if ticker:
            symbols.append(ticker)
    raw_tickers = symbols

    normalized: List[str] = []
    seen = set()
    for ticker in raw_tickers:
        clean = str(ticker).strip().upper().replace(".", "-")
        if not clean or clean in seen:
            continue
        seen.add(clean)
        normalized.append(clean)

    if not normalized:
        raise ValueError("No tickers returned for the S&P 500 universe")

    if limit is not None:
        normalized = normalized[:limit]

    return normalized
