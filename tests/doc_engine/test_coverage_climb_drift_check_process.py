"""Coverage climb B4: spring_drift_check citation process helpers.

Q2 witness: mutmut_slice on doc_engine.tools.spring_drift_check (not Arm-1).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.tools import spring_drift_check as drift

pytestmark = pytest.mark.domain_climb_sensor


def _signals_with_cite(file_rel: str = "a.java") -> dict:
    return {
        "schema_version": 2,
        "repo_path": "/r",
        "file_signatures": {file_rel: "sig1"},
        "evidence": {
            "sec": [
                {
                    "file": file_rel,
                    "line": 1,
                    "rule_id": "security__secured",
                    "match": "@Secured",
                }
            ]
        },
        "entity_table_map": {},
        "config_key_sets": {},
        "scanners": ["filesystem"],
    }


def test_process_file_citation_branches(tmp_path: Path) -> None:
    signals = _signals_with_cite("a.java")
    results: list = []
    fresh_tables: dict = {}
    cites = [("evidence.sec", signals["evidence"]["sec"][0])]

    drift._process_file_citations(
        str(tmp_path),
        "a.java",
        cites,
        deleted_set={"a.java"},
        unchanged_set=set(),
        changed_set=set(),
        signals=signals,
        fresh_evidence_by_file={},
        fresh_entity_map={},
        results=results,
        fresh_entity_tables=fresh_tables,
    )
    assert results[0]["status"] == drift.STATUS_FILE_DELETED

    results.clear()
    drift._process_file_citations(
        str(tmp_path),
        "a.java",
        cites,
        deleted_set=set(),
        unchanged_set={"a.java"},
        changed_set=set(),
        signals=signals,
        fresh_evidence_by_file={},
        fresh_entity_map={},
        results=results,
        fresh_entity_tables=fresh_tables,
    )
    assert results[0]["status"] == drift.STATUS_UNCHANGED

    results.clear()
    drift._process_file_citations(
        str(tmp_path),
        "ghost.java",
        [("evidence.sec", {"file": "ghost.java", "line": 1})],
        deleted_set=set(),
        unchanged_set=set(),
        changed_set=set(),
        signals=signals,
        fresh_evidence_by_file={},
        fresh_entity_map={},
        results=results,
        fresh_entity_tables=fresh_tables,
    )
    assert results[0]["status"] == drift.STATUS_UNKNOWN_NO_SIGNATURE


def test_recheck_without_rule_and_changed_file(tmp_path: Path) -> None:
    cfg = tmp_path / "app.yml"
    cfg.write_text("spring:\n  datasource:\n    url: jdbc:h2:mem\n", encoding="utf-8")
    results: list = []
    drift._recheck_citations_without_rule(
        str(tmp_path),
        "app.yml",
        [("evidence.cfg", {"file": "app.yml", "line": 1})],
        {"spring.datasource.url"},
        results,
    )
    assert results[0]["status"] in (
        drift.STATUS_CONFIG_VALUES_ONLY_CHANGED,
        drift.STATUS_CONFIG_STRUCTURE_CHANGED,
    )

    results2: list = []
    drift._recheck_citations_without_rule(
        str(tmp_path),
        "app.yml",
        [("evidence.cfg", {"file": "app.yml", "line": 2})],
        None,
        results2,
    )
    assert results2[0]["status"] == drift.STATUS_NO_RULE_FALLBACK

    results3: list = []
    fresh_tables: dict = {}
    drift._process_changed_file_citations(
        str(tmp_path),
        "a.java",
        [
            (
                "evidence.sec",
                {
                    "file": "a.java",
                    "line": 1,
                    "rule_id": "security__secured",
                    "match": "@Secured",
                },
            ),
            ("evidence.cfg", {"file": "a.java", "line": 2}),
        ],
        {"config_key_sets": {}},
        {
            "a.java": [
                {
                    "rule_id": "security__secured",
                    "match": "@Secured",
                    "file": "a.java",
                    "line": 1,
                }
            ]
        },
        {},
        results3,
        fresh_tables,
    )
    assert any(r["status"] == drift.STATUS_CONFIRMED for r in results3)
    assert any(r["status"] == drift.STATUS_NO_RULE_FALLBACK for r in results3)

    results4: list = []
    drift._process_changed_file_citations(
        str(tmp_path),
        "only.yml",
        [("evidence.cfg", {"file": "only.yml", "line": 1})],
        {"config_key_sets": {}},
        {},
        {},
        results4,
        {},
    )
    assert results4[0]["status"] == drift.STATUS_NO_RULE_FALLBACK
