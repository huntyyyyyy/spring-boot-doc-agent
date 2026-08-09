"""Unit tests for E-TEST domain catalog, classifier, and marker ratchet."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.test_domain_catalog import (
    known_markers,
    parallel_shard_markers,
    serial_expression,
)
from doc_engine.ci.test_domain_classify import (
    classify_test_path,
    declared_domain_markers,
    ensure_pytestmark,
)
from doc_engine.ci.test_domain_markers_check import evaluate_module, run_check

pytestmark = pytest.mark.domain_ci_meta

def test_catalog_parallel_excludes_serial_and_optin() -> None:
    parallel = set(parallel_shard_markers())
    assert "domain_schemas" in parallel
    assert "domain_integration" not in parallel
    assert "domain_unclassified" not in parallel
    assert "domain_live_optin" not in parallel
    assert "domain_integration" in serial_expression()

def test_classify_dir_and_filename_rules(tmp_path: Path) -> None:
    repo = tmp_path
    climb = repo / "tests" / "doc_engine" / "test_coverage_climb_batch8.py"
    climb.parent.mkdir(parents=True)
    climb.write_text("def test_a():\n    pass\n", encoding="utf-8")
    assert classify_test_path(repo, climb) == "domain_climb_sensor"
    ci_climb = repo / "tests" / "ci" / "test_coverage_climb_b3_domains.py"
    ci_climb.parent.mkdir(parents=True)
    ci_climb.write_text("def test_a():\n    pass\n", encoding="utf-8")
    assert classify_test_path(repo, ci_climb) == "domain_climb_sensor"
    ci = repo / "tests" / "ci" / "test_size_ratchet.py"
    ci.write_text("def test_a():\n    pass\n", encoding="utf-8")
    assert classify_test_path(repo, ci) == "domain_ci_meta"

def test_ensure_pytestmark_idempotent_and_check(tmp_path: Path) -> None:
    repo = tmp_path
    path = repo / "tests" / "doc_engine" / "test_artifact_schemas.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        '"""Doc."""\n\nfrom __future__ import annotations\n\n'
        "import os\n\ndef test_x():\n    pass\n",
        encoding="utf-8",
    )
    marker = classify_test_path(repo, path)
    assert marker == "domain_schemas"
    once = ensure_pytestmark(path.read_text(encoding="utf-8"), marker)
    path.write_text(once, encoding="utf-8")
    twice = ensure_pytestmark(path.read_text(encoding="utf-8"), marker)
    assert once == twice
    assert declared_domain_markers(once) == [marker]
    assert evaluate_module(repo, path, require_classifier_match=True) == []
    assert "import pytest" in once
    assert once.index("import pytest") < once.index("pytestmark")

def test_missing_marker_fails_evaluate(tmp_path: Path) -> None:
    repo = tmp_path
    path = repo / "tests" / "doc_engine" / "test_other_thing.py"
    path.parent.mkdir(parents=True)
    path.write_text("def test_x():\n    pass\n", encoding="utf-8")
    issues = evaluate_module(repo, path, require_classifier_match=False)
    assert any("missing domain_" in item for item in issues)
    assert known_markers()

def test_doc_engine_inventory_excludes_meeting_from_debt(tmp_path: Path) -> None:
    """Meeting modules leave the debt set (gap-average analogy)."""
    from doc_engine.ci.test_domain_inventory import build_doc_engine_inventory

    repo = tmp_path
    de = repo / "tests" / "doc_engine"
    de.mkdir(parents=True)
    (de / "test_artifact_schemas.py").write_text(
        "def test_x():\n    pass\n", encoding="utf-8"
    )
    (de / "test_still_misc.py").write_text(
        "def test_y():\n    pass\n", encoding="utf-8"
    )
    inv = build_doc_engine_inventory(repo)
    assert inv.total == 2
    assert len(inv.meeting) == 1
    assert len(inv.debt) == 1
    assert inv.debt[0].name == "test_still_misc.py"
    assert inv.floor == 98.7
    assert not inv.meets_floor
