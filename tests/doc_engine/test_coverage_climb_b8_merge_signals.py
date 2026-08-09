"""Coverage climb B8: merge_signals dedupe / entity / sort edges.

Q2 adequacy witness: mutmut_slice on doc_engine.scanning._merge_signals —
asserts bite dedupe continue, package copy, missing class_name skip, and
sort_entity_table_map.
"""

from __future__ import annotations

import pytest

from doc_engine.scanning import _merge_signals as ms

pytestmark = pytest.mark.domain_climb_sensor


def test_dedupe_rows_skips_duplicate() -> None:
    rows = [
        {"file": "a.java", "line": 1, "rule_id": "r"},
        {"file": "a.java", "line": 1, "rule_id": "r"},
        {"file": "b.java", "line": 2, "rule_id": "r"},
    ]
    out = ms._dedupe_rows(rows)
    assert len(out) == 2
    assert out[0]["file"] == "a.java"


def test_entity_candidate_copies_package_and_skips_blank() -> None:
    row = {
        "file": "a.java",
        "class_name": "Foo",
        "package": "com.ex",
        "rule_id": "persistence__entity",
    }
    cand = ms._entity_candidate_from_row(row, "Foo")
    assert cand["package"] == "com.ex"
    partial = {
        "evidence": {
            "persistence": [
                {"rule_id": "persistence__entity", "file": "a.java"},  # no class_name
                {
                    "rule_id": "other",
                    "file": "b.java",
                    "class_name": "Bar",
                },
                row,
            ]
        }
    }
    cands = ms._collect_entity_candidates(partial)
    assert list(cands) == ["Foo"]


def test_sort_entity_table_map() -> None:
    assert list(ms.sort_entity_table_map({"Z": 1, "A": 2})) == ["A", "Z"]
