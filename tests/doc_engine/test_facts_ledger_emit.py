"""Cohesive suite from tests/doc_engine/test_facts_ledger.py: test_write_rejects_bare_maps_to_subject, test_jsonl_round_trip_preserves_symbol_subjects, test_fact_emit_counts_by_predicate_and_contested_status."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from doc_engine.scanning.facts import (
    fact_emit_counts,
    facts_from_signals,
    facts_path_for_signals_out,
    write_facts_jsonl,
)
from doc_engine.scanning.symbol import SymbolError, parse

pytestmark = pytest.mark.domain_stage0

def test_write_rejects_bare_maps_to_subject(tmp_path: Path) -> None:
    """Deviation: write_facts_jsonl accepts MAPS_TO with simple-name subject."""
    bad = [
        {
            "predicate": "MAPS_TO",
            "subject": "User",
            "object": "users",
            "qualifiers": {"display_name": "User", "fqcn": "User", "symbol_kind": "type"},
            "file": "User.java",
            "line": None,
            "rule_id": None,
            "scanner": "ast-grep",
        }
    ]
    with pytest.raises(SymbolError, match="claim-symbol"):
        write_facts_jsonl(tmp_path / "facts.jsonl", bad)

def test_jsonl_round_trip_preserves_symbol_subjects(tmp_path: Path) -> None:
    """Deviation: write/load corrupts MAPS_TO identity fields."""
    signals = {
        "scanners": ["ast-grep"],
        "evidence": {
            "entities": [
                {
                    "file": "A.java",
                    "line": 3,
                    "match": "@Entity",
                    "rule_id": "persistence__entity",
                }
            ]
        },
        "entity_table_map": {
            "A": {
                "file": "A.java",
                "table": "a",
                "table_name_source": "default",
                "package": "com.example",
                "fqcn": "com.example.A",
            }
        },
    }
    facts = facts_from_signals(signals)
    path = tmp_path / "facts.jsonl"
    write_facts_jsonl(path, facts)
    loaded = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert loaded == facts
    maps = [f for f in loaded if f["predicate"] == "MAPS_TO"]
    assert parse(maps[0]["subject"]).fqcn == "com.example.A"

def test_fact_emit_counts_by_predicate_and_contested_status() -> None:
    """Deviation: emit counters mis-count MAPS_TO vs evidence (identity strings irrelevant)."""
    facts = [
        {
            "predicate": "persistence__entity",
            "subject": "A.java",
            "object": "@Entity",
            "qualifiers": {},
            "file": "A.java",
            "line": 1,
            "rule_id": "persistence__entity",
            "scanner": "ast-grep",
        },
        {
            "predicate": "MAPS_TO",
            "subject": "doc-engine spring . com/example/a/User#",
            "object": "a_user",
            "qualifiers": {"status": "contested"},
            "file": "pkg_a/User.java",
            "line": None,
            "rule_id": None,
            "scanner": "ast-grep",
        },
        {
            "predicate": "MAPS_TO",
            "subject": "doc-engine spring . com/example/b/User#",
            "object": "b_user",
            "qualifiers": {"status": "contested"},
            "file": "pkg_b/User.java",
            "line": None,
            "rule_id": None,
            "scanner": "ast-grep",
        },
        {
            "predicate": "MAPS_TO",
            "subject": "doc-engine spring . com/acme/Order#",
            "object": "orders",
            "qualifiers": {},
            "file": "Order.java",
            "line": None,
            "rule_id": None,
            "scanner": "ast-grep",
        },
    ]
    assert fact_emit_counts(facts) == {
        "facts_total": 4,
        "facts_maps_to": 3,
        "facts_maps_to_contested": 2,
        "facts_evidence": 1,
        "facts_absence": 0,
        "facts_unproven": 0,
        "facts_recall_miss": 0,
    }
