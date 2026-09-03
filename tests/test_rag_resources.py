"""Tests for spec 0054 — MCP RAG resources server.

One test per acceptance criterion, named for the AC it verifies, so the
coverage map in ``specs/0054-mcp-rag-server/tasks.md`` can be checked
mechanically.

No I/O — ``build_index`` and ``dispatch_rag`` are pure functions.
"""

from __future__ import annotations

from typing import Any, Dict

from quantsmith.adapters.mcp_servers.rag_resources import (
    ERR_INVALID_PARAMS,
    RagRecord,
    build_index,
    dispatch_rag,
)
from quantsmith.adapters.mcp_servers.contract import (
    ERR_ACCESS_DENIED,
    ERR_METHOD_NOT_FOUND,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _req(method: str, params: Dict[str, Any], req_id: int = 1) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "method": method, "id": req_id, "params": params}


def _make_record(uri: str, text: str, access_level: str = "public") -> RagRecord:
    return RagRecord(uri=uri, text=text, access_level=access_level)


def _empty_index():
    return build_index([])


# ---------------------------------------------------------------------------
# AC-001: missing or unrecognized caller_clearance → -32600
# ---------------------------------------------------------------------------


def test_missing_clearance_returns_access_denied_AC_001() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"query": "momentum"}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_ACCESS_DENIED


def test_unrecognized_clearance_returns_access_denied_AC_001() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "god", "query": "momentum"}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_ACCESS_DENIED


# ---------------------------------------------------------------------------
# AC-002: resources/search with empty query → -32602
# ---------------------------------------------------------------------------


def test_empty_query_returns_invalid_params_AC_002() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": ""}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_INVALID_PARAMS


def test_whitespace_query_returns_invalid_params_AC_002() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "   "}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_INVALID_PARAMS


# ---------------------------------------------------------------------------
# AC-003: resources/search with top_k: 25 → -32602
# ---------------------------------------------------------------------------


def test_top_k_too_large_returns_invalid_params_AC_003() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "signal", "top_k": 25}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_INVALID_PARAMS


def test_top_k_zero_returns_invalid_params_AC_003() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "signal", "top_k": 0}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_INVALID_PARAMS


# ---------------------------------------------------------------------------
# AC-004: resources/search with unknown domain → -32602
# ---------------------------------------------------------------------------


def test_unknown_domain_returns_invalid_params_AC_004() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum", "domain": "unknown"}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_INVALID_PARAMS


# ---------------------------------------------------------------------------
# AC-005: higher-scoring record precedes lower-scoring record
# ---------------------------------------------------------------------------


def test_higher_score_ranks_first_AC_005() -> None:
    # Record A has "momentum" repeated many times → higher TF for "momentum"
    rec_a = _make_record(
        "knowledge://memory/equity/alpha",
        "momentum momentum momentum signal momentum alpha momentum cross sectional momentum",
        "public",
    )
    # Record B mentions "momentum" once
    rec_b = _make_record(
        "knowledge://memory/equity/beta",
        "momentum signal factor model equity returns",
        "public",
    )
    idx = build_index([rec_a, rec_b])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum"}),
        index=idx,
    )
    hits = resp["result"]["hits"]
    assert len(hits) >= 2
    assert hits[0]["uri"] == rec_a.uri
    assert hits[0]["score"] >= hits[1]["score"]


# ---------------------------------------------------------------------------
# AC-006: internal caller cannot see restricted records
# ---------------------------------------------------------------------------


def test_internal_caller_excludes_restricted_records_AC_006() -> None:
    rec_internal = _make_record(
        "knowledge://memory/equity/internal_note",
        "momentum factor cross sectional signal alpha",
        "internal",
    )
    rec_restricted = _make_record(
        "knowledge://memory/equity/restricted_note",
        "momentum factor cross sectional signal alpha secret restricted",
        "restricted",
    )
    idx = build_index([rec_internal, rec_restricted])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "internal", "query": "momentum factor"}),
        index=idx,
    )
    hits = resp["result"]["hits"]
    uris = [h["uri"] for h in hits]
    assert rec_internal.uri in uris
    assert rec_restricted.uri not in uris


# ---------------------------------------------------------------------------
# AC-007: public caller sees neither internal nor restricted records
# ---------------------------------------------------------------------------


def test_public_caller_sees_no_restricted_or_internal_AC_007() -> None:
    rec_internal = _make_record(
        "knowledge://memory/equity/internal_note",
        "momentum factor signal",
        "internal",
    )
    rec_restricted = _make_record(
        "knowledge://memory/equity/restricted_note",
        "momentum factor signal",
        "restricted",
    )
    idx = build_index([rec_internal, rec_restricted])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum"}),
        index=idx,
    )
    assert resp["result"]["hits"] == []


# ---------------------------------------------------------------------------
# AC-008: top_k bounds the result count
# ---------------------------------------------------------------------------


def test_top_k_limits_result_count_AC_008() -> None:
    records = [
        _make_record(
            f"knowledge://memory/equity/rec{i}",
            f"momentum signal factor alpha strategy record {i} equity",
            "public",
        )
        for i in range(5)
    ]
    idx = build_index(records)
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum signal", "top_k": 2}),
        index=idx,
    )
    assert len(resp["result"]["hits"]) <= 2


# ---------------------------------------------------------------------------
# AC-009: each SearchHit contains uri, passage, score, access_level
# ---------------------------------------------------------------------------


def test_search_hit_fields_AC_009() -> None:
    rec = _make_record(
        "knowledge://memory/equity/note1",
        "cross sectional momentum signal factor alpha returns portfolio equity",
        "public",
    )
    idx = build_index([rec])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum signal"}),
        index=idx,
    )
    hits = resp["result"]["hits"]
    assert len(hits) == 1
    hit = hits[0]
    assert "uri" in hit
    assert "passage" in hit
    assert "score" in hit
    assert "access_level" in hit
    assert hit["uri"] == rec.uri
    assert isinstance(hit["score"], float)
    assert len(hit["passage"]) <= 500


# ---------------------------------------------------------------------------
# AC-010: unsupported method → -32601
# ---------------------------------------------------------------------------


def test_unsupported_method_returns_method_not_found_AC_010() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("memory/query", {"caller_clearance": "public"}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_METHOD_NOT_FOUND


# ---------------------------------------------------------------------------
# AC-011: resources/list returns accessible records sorted by URI
# ---------------------------------------------------------------------------


def test_list_returns_accessible_records_sorted_AC_011() -> None:
    rec_public = _make_record("knowledge://memory/equity/pub", "public text alpha", "public")
    rec_internal = _make_record("knowledge://memory/equity/int", "internal text alpha", "internal")
    rec_restricted = _make_record("knowledge://memory/equity/res", "restricted text alpha", "restricted")
    idx = build_index([rec_public, rec_internal, rec_restricted])
    resp = dispatch_rag(
        _req("resources/list", {"caller_clearance": "internal"}),
        index=idx,
    )
    resources = resp["result"]["resources"]
    uris = [r["uri"] for r in resources]
    assert rec_public.uri in uris
    assert rec_internal.uri in uris
    assert rec_restricted.uri not in uris
    # sorted by URI ascending
    assert uris == sorted(uris)


# ---------------------------------------------------------------------------
# AC-012: resources/read with sufficient clearance returns record text
# ---------------------------------------------------------------------------


def test_read_accessible_record_returns_text_AC_012() -> None:
    text = "internal momentum strategy analysis cross sectional factor"
    rec = _make_record("knowledge://memory/equity/int_rec", text, "internal")
    idx = build_index([rec])
    resp = dispatch_rag(
        _req("resources/read", {"caller_clearance": "internal", "uri": rec.uri}),
        index=idx,
    )
    assert "result" in resp
    contents = resp["result"]["contents"]
    assert len(contents) == 1
    assert contents[0]["text"] == text
    assert contents[0]["uri"] == rec.uri


# ---------------------------------------------------------------------------
# AC-013: resources/read for restricted record with internal clearance → -32600
# ---------------------------------------------------------------------------


def test_read_denied_record_returns_access_denied_AC_013() -> None:
    rec = _make_record("knowledge://memory/equity/res_rec", "restricted secret data", "restricted")
    idx = build_index([rec])
    resp = dispatch_rag(
        _req("resources/read", {"caller_clearance": "internal", "uri": rec.uri}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_ACCESS_DENIED


def test_read_nonexistent_uri_also_returns_access_denied_AC_013() -> None:
    idx = _empty_index()
    resp = dispatch_rag(
        _req("resources/read", {"caller_clearance": "internal", "uri": "knowledge://memory/equity/ghost"}),
        index=idx,
    )
    assert resp["error"]["code"] == ERR_ACCESS_DENIED


# ---------------------------------------------------------------------------
# AC-014: domain filter restricts results to the specified authority
# ---------------------------------------------------------------------------


def test_domain_filter_restricts_to_memory_AC_014() -> None:
    rec_memory = _make_record(
        "knowledge://memory/equity/mem1",
        "momentum factor signal equity cross sectional",
        "public",
    )
    rec_mresearch = _make_record(
        "knowledge://market_research/eq/note/n001",
        "momentum factor signal equity cross sectional",
        "public",
    )
    idx = build_index([rec_memory, rec_mresearch])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "public", "query": "momentum factor", "domain": "memory"}),
        index=idx,
    )
    hits = resp["result"]["hits"]
    uris = [h["uri"] for h in hits]
    assert rec_memory.uri in uris
    assert rec_mresearch.uri not in uris


# ---------------------------------------------------------------------------
# AC-015: restricted caller can see restricted records in search
# ---------------------------------------------------------------------------


def test_restricted_caller_sees_restricted_records_AC_015() -> None:
    rec = _make_record(
        "knowledge://memory/equity/res_note",
        "restricted proprietary momentum signal strategy alpha",
        "restricted",
    )
    idx = build_index([rec])
    resp = dispatch_rag(
        _req("resources/search", {"caller_clearance": "restricted", "query": "momentum strategy"}),
        index=idx,
    )
    hits = resp["result"]["hits"]
    uris = [h["uri"] for h in hits]
    assert rec.uri in uris
