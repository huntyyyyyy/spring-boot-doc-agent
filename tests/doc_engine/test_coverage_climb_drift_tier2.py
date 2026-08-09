"""Coverage climb: spring_drift_tier2 entity/repo/query/JPQL helpers."""

from __future__ import annotations

from doc_engine.tools import spring_drift_tier2 as t2
from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
    STATUS_UNCHANGED,
)


def test_entity_and_repository_verdicts() -> None:
    assert "no longer matched" in t2._entity_missing_detail("Foo")
    assert "no class_name" in t2._entity_missing_detail(None)
    assert t2._entity_table_fields_changed(
        {"table": "A", "table_name_source": "ann"},
        {"table": "B", "table_name_source": "ann"},
    )
    status, detail = t2._entity_citation_verdict(
        {"class_name": "Foo", "table": "T"},
        {"Foo": {"table": "T", "table_name_source": "ann"}},
    )
    assert status == STATUS_CONFIRMED and detail is None
    status, _ = t2._entity_citation_verdict({"class_name": "Missing"}, {})
    assert status == STATUS_DRIFTED

    results, fresh = t2._recheck_entities(
        {"Bar": {"table": "B"}},
        [("evidence.persistence", {"class_name": "Bar", "table": "B", "file": "a.java", "line": 1})],
    )
    assert results[0]["status"] == STATUS_CONFIRMED
    assert "Bar" in fresh

    assert "no longer matched" in t2._repository_missing_detail("Repo")
    assert t2._repository_type_args_changed(
        {"entity": "E", "id_type": "Long"},
        {"entity": "E", "id_type": "UUID"},
    )
    st, _ = t2._repository_citation_verdict(
        {"repository": "R", "entity": "E", "id_type": "Long"},
        {"R": {"repository": "R", "entity": "E", "id_type": "Long"}},
    )
    assert st == STATUS_CONFIRMED
    repos = t2._recheck_repositories(
        [{"repository": "R", "entity": "E", "id_type": "Long"}],
        [("evidence.persistence", {"repository": "Gone", "file": "r.java", "line": 2})],
    )
    assert repos[0]["status"] == STATUS_DRIFTED


def test_recheck_queries_and_generic() -> None:
    group = [
        ("evidence.raw", {"query_kind": "jpql", "query": "select 1", "file": "q.java", "line": 1}),
        ("evidence.raw", {"query_kind": "jpql", "query": "missing", "file": "q.java", "line": 2}),
    ]
    out = t2._recheck_queries(
        [{"query_kind": "jpql", "query": "select 1"}],
        group,
    )
    assert out[0]["status"] == STATUS_CONFIRMED
    assert out[1]["status"] == STATUS_DRIFTED
    gen = t2._recheck_generic(
        [{"match": "@GetMapping"}],
        [
            ("evidence.api", {"match": "@GetMapping", "file": "a.java", "line": 1}),
            ("evidence.api", {"match": "@PostMapping", "file": "a.java", "line": 2}),
        ],
    )
    assert gen[0]["status"] == STATUS_CONFIRMED
    assert gen[1]["status"] == STATUS_DRIFTED


def test_jpql_lineage_verdicts_and_reverify() -> None:
    assert t2._jpql_lineage_needs_reverify({"status": STATUS_UNCHANGED})
    assert not t2._jpql_lineage_needs_reverify({"status": STATUS_DRIFTED})
    result = {"status": STATUS_UNCHANGED, "tier": 1, "detail": None}
    t2._apply_jpql_lineage_verdict(
        result, "E", "E.java", {"table": "T"}, None, entity_file_deleted=True
    )
    assert result["status"] == STATUS_DRIFTED
    result = {"status": STATUS_UNCHANGED, "tier": 1, "detail": None}
    t2._apply_jpql_lineage_verdict(
        result, "E", "E.java", {"table": "T"}, {"table": "T"}, False
    )
    assert result["status"] == STATUS_CONFIRMED
    result = {"status": STATUS_UNCHANGED, "tier": 1, "detail": None}
    t2._apply_jpql_lineage_verdict(
        result, "E", "E.java", {"table": "OLD"}, {"table": "NEW"}, False
    )
    assert result["status"] == STATUS_DRIFTED

    signals = {
        "evidence": {
            "raw_queries": [
                {
                    "file": "q.java",
                    "line": 3,
                    "lineage": {"resolved_via_entity": "E"},
                },
                {"file": "n.java", "line": 1},
            ]
        },
        "entity_table_map": {"E": {"file": "E.java", "table": "T"}},
    }
    resolved = list(t2._raw_query_entries_with_resolved_entity(signals))
    assert len(resolved) == 1
    rows = [
        {
            "file": "q.java",
            "line": 3,
            "status": STATUS_UNCHANGED,
            "tier": 1,
            "detail": None,
        }
    ]
    t2._reverify_jpql_lineage_provenance(
        rows,
        signals,
        {"E": {"table": "T2"}},
        changed_set={"E.java"},
        deleted_set=set(),
    )
    assert rows[0]["status"] == STATUS_DRIFTED


def test_build_signal_identity_helpers() -> None:
    assert t2._identity_build_plugin(
        {"rule_id": "deployment__build_plugin", "plugin_id": "p", "plugin_version": "1"}
    ) == ("deployment__build_plugin", "p", "1")
    assert t2._identity_build_dependency(
        {
            "rule_id": "deployment__build_dependency",
            "configuration": "impl",
            "coordinate": {"group": "g", "name": "n", "version": "1"},
        }
    ) == ("deployment__build_dependency", "impl", "g", "n", "1")
    assert t2._identity_build_module(
        {"rule_id": "deployment__build_module", "module": "m"}
    ) == ("deployment__build_module", "m")
    assert t2._identity_build_toolchain(
        {
            "rule_id": "deployment__build_toolchain",
            "toolchain_kind": "jdk",
            "toolchain_value": "17",
        }
    )[1] == "jdk"
    assert t2._identity_version_catalog(
        {"rule_id": "deployment__version_catalog", "catalog_kind": "lib", "catalog_key": "k"}
    )[2] == "k"
    assert t2._identity_fallback_match({"rule_id": "x", "match": "y"}) == ("x", "y")
    assert t2._is_build_signal_rule("deployment__build_dependency")
    assert not t2._is_build_signal_rule("persistence__entity")
    drifted = t2._drifted_group(
        [("s", {"file": "b.gradle", "line": 1})],
        "gone",
    )
    assert drifted[0]["status"] == STATUS_DRIFTED
