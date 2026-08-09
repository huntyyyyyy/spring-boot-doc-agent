"""Coverage climb B5: residual symbol + facts branch edges (Stage-0)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.scanning import facts as facts_mod
from doc_engine.scanning import symbol as sym
from doc_engine.scanning._scanner_astgrep import _enrich_query_entry

pytestmark = pytest.mark.domain_climb_sensor


def test_split_package_segments_empty_after_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sym, "_package_has_empty_segment", lambda _p: False)
    with pytest.raises(sym.SymbolError, match="invalid package"):
        sym._split_package_segments("")


def test_split_member_suffix_field_none_falls_through() -> None:
    kind, member, body = sym._split_member_suffix("Outer#.", "Outer#.")
    assert kind == "type"
    assert member is None
    assert body == "Outer#."


def test_facts_append_none_hit_and_covering_true_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rows: list = []
    facts_mod._append_evidence_hit(
        rows, {}, bucket="api", default_scanner="ast-grep"
    )
    assert rows == []
    proof = {
        "inventory_root": "/tmp/inv",
        "receipts": [{"scanner": "ast-grep", "status": "complete"}],
    }
    monkeypatch.setattr(
        "doc_engine.scanning.covering.verify_covering_proof",
        lambda *_a, **_k: (True, None),
    )
    ok, root, astg = facts_mod._covering_state(
        {
            "_covering_proof": proof,
            "scanner_version": "v1",
            "file_signatures": {"A.java": "sig"},
        }
    )
    assert ok is True and root == "/tmp/inv" and astg is True
    # False branch: mapping proof but non-mapping signatures.
    ok2, _root2, _astg2 = facts_mod._covering_state(
        {
            "_covering_proof": proof,
            "scanner_version": "v1",
            "file_signatures": ["not-a-map"],
        }
    )
    assert ok2 is False


def test_facts_from_signals_skips_non_mapping_bags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(facts_mod, "covering_writer_facts", lambda _s: [])
    out = facts_mod.facts_from_signals(
        {
            "evidence": ["not-a-map"],
            "entity_table_map": ["not-a-map"],
            "scanner_version": "v1",
        }
    )
    assert out == []
    monkeypatch.undo()
    skipped = facts_mod.covering_writer_facts(
        {
            "scanner_version": "v1",
            "evidence": {},
            "entity_table_map": {},
            "_scan_partials_meta": "not-a-map",
        }
    )
    assert not any(f.get("predicate") == "RECALL_MISS" for f in skipped)
    with_meta = facts_mod.covering_writer_facts(
        {
            "scanner_version": "v1",
            "evidence": {},
            "entity_table_map": {},
            "_scan_partials_meta": {
                "entity_keys_by_scanner": {
                    "ast-grep": ["Native"],
                    "codeql": ["Missed"],
                }
            },
        }
    )
    assert any(f.get("predicate") == "RECALL_MISS" for f in with_meta)


def test_enrich_query_entry_none_query_text() -> None:
    entry: dict = {}
    _enrich_query_entry(entry, {"metaVariables": {"multi": {"ARGS": []}}})
    assert entry.get("query_kind") is not None or "query_kind" in entry
    assert "query" not in entry
