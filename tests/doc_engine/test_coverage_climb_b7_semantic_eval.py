"""Coverage climb B7: semantic_eval overlap / path / main edges.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.semantic_eval —
asserts bite empty-token skip, PathValidationError continues, empty mermaid,
and main() path-validation exits.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.paths import PathValidationError
from doc_engine.tools import semantic_eval as seh
from doc_engine.tools.semantic_eval_confirmed import best_overlap
from doc_engine.tools.semantic_eval_scan import (
    markdown_names,
    resolve_architecture_path,
    scan_mermaid,
)

pytestmark = pytest.mark.domain_climb_sensor


def test_best_overlap_skips_empty_tokens() -> None:
    ratio, entry = best_overlap({"a", "b"}, [([], {"topic": "x"}), ({"a"}, {"topic": "y"})])
    assert entry["topic"] == "y"
    assert ratio > 0


def test_markdown_names_skips_invalid(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "ok.md").write_text("# hi", encoding="utf-8")
    (tmp_path / "skip.txt").write_text("x", encoding="utf-8")
    (tmp_path / "bad.md").write_text("# bad", encoding="utf-8")

    def fake_join(docs_dir: str, name: str):
        if name == "bad.md":
            raise PathValidationError("unsafe")
        return Path(docs_dir) / name

    monkeypatch.setattr(seh, "join_under", fake_join)
    names = markdown_names(str(tmp_path))
    assert names == ["ok.md"]


def test_resolve_architecture_path_validation_continue(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = {"n": 0}

    def boom(artifacts_dir: str, *parts: str):
        calls["n"] += 1
        raise PathValidationError("nope")

    monkeypatch.setattr(seh, "join_under", boom)
    assert resolve_architecture_path(str(tmp_path)) is None
    assert calls["n"] >= 1


def test_scan_mermaid_empty_when_no_block(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "architecture.md").write_text("# no mermaid here\n", encoding="utf-8")
    assert scan_mermaid(str(tmp_path)) == []


def test_main_path_validation_exits(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["semantic_eval_helpers", str(tmp_path / "missing")],
    )
    with pytest.raises(SystemExit) as exc:
        seh.main()
    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err

    good = tmp_path / "arts"
    good.mkdir()
    (good / "docs").mkdir()
    out_bad = tmp_path / ".." / "escape.json"
    monkeypatch.setattr(
        "sys.argv",
        ["semantic_eval_helpers", str(good), "--out", str(out_bad)],
    )
    with pytest.raises(SystemExit) as exc2:
        seh.main()
    assert exc2.value.code == 1
