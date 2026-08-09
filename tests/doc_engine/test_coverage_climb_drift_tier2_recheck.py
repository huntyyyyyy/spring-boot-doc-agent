"""Coverage climb B4: spring_drift_tier2 recheck/dispatch remaining paths.

Q2 witness: mutmut_slice on doc_engine.tools.spring_drift_tier2 (not Arm-1 —
this is citation recheck logic, not scan formatting).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.tools import spring_drift_tier2 as t2
from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
    STATUS_UNCHANGED,
)

pytestmark = pytest.mark.domain_climb_sensor


def test_entity_and_repo_field_drift_details() -> None:
    status, detail = t2._entity_citation_verdict(
        {"class_name": "Foo", "table": "OLD", "table_name_source": "ann"},
        {"Foo": {"table": "NEW", "table_name_source": "ann"}},
    )
    assert status == STATUS_DRIFTED
    assert "OLD" in detail and "NEW" in detail

    status, detail = t2._repository_citation_verdict(
        {"repository": "R", "entity": "E", "id_type": "Long"},
        {"R": {"repository": "R", "entity": "E", "id_type": "UUID"}},
    )
    assert status == STATUS_DRIFTED
    assert "Long" in detail and "UUID" in detail


def test_jpql_verdict_entity_gone_without_delete() -> None:
    result = {"status": STATUS_UNCHANGED, "tier": 1, "detail": None}
    t2._apply_jpql_lineage_verdict(
        result, "E", "E.java", {"table": "T"}, None, entity_file_deleted=False
    )
    assert result["status"] == STATUS_DRIFTED
    assert "no longer matches" in result["detail"]


def test_reverify_one_jpql_early_exits() -> None:
    entry = {
        "file": "q.java",
        "line": 1,
        "lineage": {"resolved_via_entity": "Missing"},
    }
    t2._reverify_one_jpql_entry(entry, {"entity_table_map": {}}, {}, set(), set(), {})

    entry2 = {
        "file": "q.java",
        "line": 2,
        "lineage": {"resolved_via_entity": "E"},
    }
    signals = {"entity_table_map": {"E": {"file": "E.java", "table": "T"}}}
    t2._reverify_one_jpql_entry(
        entry2, signals, {}, changed_set=set(), deleted_set=set(), results_by_file_line={}
    )

    result = {"status": STATUS_DRIFTED, "tier": 2, "file": "q.java", "line": 3}
    entry3 = {
        "file": "q.java",
        "line": 3,
        "lineage": {"resolved_via_entity": "E"},
    }
    t2._reverify_one_jpql_entry(
        entry3,
        signals,
        {},
        changed_set={"E.java"},
        deleted_set=set(),
        results_by_file_line={("q.java", 3): result},
    )
    assert result["status"] == STATUS_DRIFTED


def test_dispatch_entity_repo_query_and_tier2_file(tmp_path: Path) -> None:
    java = tmp_path / "E.java"
    java.write_text("class E {}\n", encoding="utf-8")
    results: list = []
    tables = t2._dispatch_tier2_rule(
        "persistence__entity",
        [
            (
                "evidence.persistence",
                {
                    "class_name": "E",
                    "table": "T",
                    "file": "E.java",
                    "line": 1,
                    "rule_id": "persistence__entity",
                },
            )
        ],
        repo_path=str(tmp_path),
        file_rel="E.java",
        fresh_by_rule={},
        fresh_entity_map={"E": {"table": "T", "table_name_source": "ann"}},
        results=results,
        fresh_entity_tables={},
    )
    assert "E" in tables
    assert results[0]["status"] == STATUS_CONFIRMED

    results2: list = []
    t2._dispatch_tier2_rule(
        "persistence__repository",
        [
            (
                "evidence.persistence",
                {
                    "repository": "R",
                    "entity": "E",
                    "id_type": "Long",
                    "file": "R.java",
                    "line": 1,
                    "rule_id": "persistence__repository",
                },
            )
        ],
        repo_path=str(tmp_path),
        file_rel="R.java",
        fresh_by_rule={
            "persistence__repository": [
                {"repository": "R", "entity": "E", "id_type": "Long"}
            ]
        },
        fresh_entity_map={},
        results=results2,
        fresh_entity_tables={},
    )
    assert results2[0]["status"] == STATUS_CONFIRMED

    results3: list = []
    t2._dispatch_tier2_rule(
        "raw_queries__query",
        [
            (
                "evidence.raw",
                {
                    "query_kind": "jpql",
                    "query": "select 1",
                    "file": "q.java",
                    "line": 1,
                    "rule_id": "raw_queries__query",
                },
            )
        ],
        repo_path=str(tmp_path),
        file_rel="q.java",
        fresh_by_rule={
            "raw_queries__query": [{"query_kind": "jpql", "query": "select 1"}]
        },
        fresh_entity_map={},
        results=results3,
        fresh_entity_tables={},
    )
    assert results3[0]["status"] == STATUS_CONFIRMED

    file_results, fresh = t2.tier2_recheck_file(
        str(tmp_path),
        "E.java",
        [
            (
                "evidence.persistence",
                {
                    "class_name": "E",
                    "table": "T",
                    "file": "E.java",
                    "line": 1,
                    "rule_id": "persistence__entity",
                },
            )
        ],
        {"E.java": [{"rule_id": "persistence__entity", "class_name": "E"}]},
        {"E": {"table": "T", "table_name_source": "ann"}},
    )
    assert file_results and file_results[0]["status"] == STATUS_CONFIRMED
    assert "E" in fresh
