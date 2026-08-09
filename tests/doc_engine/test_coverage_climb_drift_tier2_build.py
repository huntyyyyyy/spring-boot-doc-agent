"""Coverage climb: spring_drift_tier2 config/build recheck paths."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.tools import spring_drift_tier2 as t2
from doc_engine.tools.spring_drift_common import (
    STATUS_CONFIG_STRUCTURE_CHANGED,
    STATUS_CONFIG_VALUES_ONLY_CHANGED,
    STATUS_CONFIRMED,
    STATUS_DRIFTED,
)

pytestmark = pytest.mark.domain_climb_sensor


def test_repository_missing_detail_without_name() -> None:
    detail = t2._repository_missing_detail(None)
    assert "no repository name" in detail
    status, msg = t2._repository_citation_verdict({"entity": "E"}, {})
    assert status == STATUS_DRIFTED and msg is not None


def test_recheck_config_keys_paths(tmp_path: Path) -> None:
    assert t2._recheck_config_keys(str(tmp_path), "missing.yml", {"a"}) is None
    cfg = tmp_path / "app.yml"
    cfg.write_text("spring:\n  datasource:\n    url: jdbc:h2:mem\n", encoding="utf-8")
    status, detail = t2._recheck_config_keys(
        str(tmp_path), "app.yml", {"spring.datasource.url", "gone.key"}
    )
    assert status == STATUS_CONFIG_STRUCTURE_CHANGED
    assert "added" in detail or "removed" in detail

    from doc_engine.scanning.support._config_keys import extract_config_keys

    current = set(extract_config_keys(cfg.read_text(encoding="utf-8"), "app.yml"))
    status2, detail2 = t2._recheck_config_keys(str(tmp_path), "app.yml", current)
    assert status2 == STATUS_CONFIG_VALUES_ONLY_CHANGED
    assert "value changed" in detail2 or "human look" in detail2


def test_read_build_file_and_identity_budget(tmp_path: Path) -> None:
    group = [("evidence.deployment", {"file": "../escape.gradle", "line": 1})]
    text, err = t2._read_build_file_text(str(tmp_path), "../escape.gradle", group)
    assert text is None and err is not None
    assert err[0]["status"] == STATUS_DRIFTED

    missing_group = [("evidence.deployment", {"file": "gone.gradle", "line": 1})]
    text2, err2 = t2._read_build_file_text(str(tmp_path), "gone.gradle", missing_group)
    assert text2 is None and err2 is not None

    gradle = tmp_path / "build.gradle"
    gradle.write_text(
        "plugins { id 'java' version '1.0' }\n"
        "dependencies { implementation 'g:n:1.0' }\n",
        encoding="utf-8",
    )
    ok_group = [
        (
            "evidence.deployment",
            {
                "rule_id": "deployment__build_plugin",
                "plugin_id": "java",
                "plugin_version": "1.0",
                "file": "build.gradle",
                "line": 1,
            },
        ),
        (
            "evidence.deployment",
            {
                "rule_id": "deployment__build_plugin",
                "plugin_id": "missing",
                "plugin_version": "9",
                "file": "build.gradle",
                "line": 2,
            },
        ),
    ]
    results = t2._recheck_build_signals(str(tmp_path), "build.gradle", ok_group)
    assert any(r["status"] == STATUS_CONFIRMED for r in results)
    assert any(r["status"] == STATUS_DRIFTED for r in results)

    budget = {("k",): 1}
    confirmed = t2._consume_identity_budget(
        budget, ("k",), "s", {"file": "f", "line": 1}, "gone"
    )
    drifted = t2._consume_identity_budget(
        budget, ("k",), "s", {"file": "f", "line": 2}, "gone"
    )
    assert confirmed["status"] == STATUS_CONFIRMED
    assert drifted["status"] == STATUS_DRIFTED


def test_dispatch_tier2_build_and_generic() -> None:
    results: list = []
    tables = t2._dispatch_tier2_rule(
        "deployment__build_dependency",
        [("s", {"file": "x", "line": 1, "rule_id": "deployment__build_dependency"})],
        repo_path="/tmp/no-such-repo",
        file_rel="missing.gradle",
        fresh_by_rule={},
        fresh_entity_map={},
        results=results,
        fresh_entity_tables={},
    )
    assert tables == {}
    assert results and results[0]["status"] == STATUS_DRIFTED

    results2: list = []
    t2._dispatch_tier2_rule(
        "security__whatever",
        [("s", {"match": "@Secured", "file": "a.java", "line": 1})],
        repo_path="/tmp",
        file_rel="a.java",
        fresh_by_rule={"security__whatever": [{"match": "@Secured"}]},
        fresh_entity_map={},
        results=results2,
        fresh_entity_tables={},
    )
    assert results2[0]["status"] == STATUS_CONFIRMED

    assert t2._build_signal_identity(
        {"rule_id": "unknown", "match": "m"}
    ) == ("unknown", "m")
