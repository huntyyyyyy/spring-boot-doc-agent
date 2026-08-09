"""Coverage climb B8: build_cross_group_edges ingest / fanout / main IO.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.build_cross_group_edges —
asserts bite missing-path ingest return, package-fanout resolve, and main
JSON/OS error exit 2.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.tools import build_cross_group_edges as bce

pytestmark = pytest.mark.domain_climb_sensor


def test_ingest_reference_row_skips_missing_path() -> None:
    decl: dict = {}
    stem: dict = {}
    imports: dict = {}
    bce._ingest_reference_row(
        {"match": "package com.ex;"}, decl, stem, imports
    )
    assert decl == {} and stem == {} and imports == {}


def test_resolve_type_import_package_fanout() -> None:
    decl = {"com.ex": {"a/A.java", "a/B.java"}}
    stem: dict = {}
    files, conf = bce._resolve_type_import("com.ex.Thing", decl, stem)
    assert conf == "package-fanout"
    assert files == ["a/A.java", "a/B.java"]


def test_main_json_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    bad = tmp_path / "groups.json"
    bad.write_text("{not-json", encoding="utf-8")
    signals = tmp_path / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        ["build_cross_group_edges", str(bad), str(signals)],
    )
    assert bce.main() == 2
    assert "error:" in capsys.readouterr().err
