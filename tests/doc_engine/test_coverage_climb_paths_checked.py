"""Coverage climb: checked_path / join_under / scripts meta paths."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from doc_engine import paths as paths_mod
from doc_engine.paths import PathValidationError
from doc_engine.scanning.gap_probe import absence_recall as absence
from doc_engine.tools import semantic_eval_helpers as seh
from doc_engine.tools import spring_signal_scan as sss

pytestmark = pytest.mark.domain_climb_sensor

def test_checked_path_file_and_unknown_want(tmp_path: Path) -> None:
    f = tmp_path / "f.txt"
    f.write_text("x", encoding="utf-8")
    assert paths_mod.checked_path(f, want="file") == f.resolve()
    with pytest.raises(PathValidationError, match="not a file"):
        paths_mod.checked_path(tmp_path, want="file")
    with pytest.raises(PathValidationError, match="not a directory"):
        paths_mod.checked_path(f, want="dir")
    with pytest.raises(ValueError, match="unknown want"):
        paths_mod.checked_path(tmp_path, want="socket")

def test_checked_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self, *a, **k):
        if "bad" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve"):
        paths_mod.checked_path(tmp_path / "bad", want="dir")

def test_checked_output_path_refuses_directory(tmp_path: Path) -> None:
    d = tmp_path / "outdir"
    d.mkdir()
    with pytest.raises(PathValidationError, match="not a file"):
        paths_mod.checked_output_path(d)

def test_checked_output_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self, *a, **k):
        if "boom" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve"):
        paths_mod.checked_output_path(tmp_path / "boom.json")

def test_join_under_absolute_and_escape(tmp_path: Path) -> None:
    with pytest.raises(PathValidationError, match="unsafe|escapes"):
        paths_mod.join_under(tmp_path, "/abs")
    with pytest.raises(PathValidationError, match="unsafe"):
        paths_mod.join_under(tmp_path, "..", "x")
    nested = tmp_path / "a"
    nested.mkdir()
    assert paths_mod.join_under(tmp_path, "a") == nested.resolve()

def test_scripts_meta_path_entries_and_packaged_astgrep() -> None:
    entries = paths_mod.scripts_meta_path_entries()
    assert any(e.endswith("ci") or e.replace("\\", "/").endswith("/ci") for e in entries)
    assert paths_mod.codeql_pack_dir().name == "spring-signals"
    # Prefer packaged rules when present.
    p = paths_mod.ast_grep_rules_path()
    assert p.is_file()
