"""Coverage climb B7: paths.py remaining edge branches.

Q2 adequacy witness: mutmut_slice on doc_engine.paths — asserts bite ``..``
rejection on output paths, join_under OSError/escape, and packaged-rules
fallback (not vacuous line padding).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine import paths as paths_mod
from doc_engine.paths import PathValidationError

pytestmark = pytest.mark.domain_climb_sensor


def test_checked_output_path_rejects_dotdot(tmp_path: Path) -> None:
    with pytest.raises(PathValidationError, match=r"\.\."):
        paths_mod.checked_output_path(tmp_path / ".." / "out.json")


def test_join_under_base_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self: Path, *a: object, **k: object) -> Path:
        if "badbase" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve base"):
        paths_mod.join_under(tmp_path / "badbase", "a")


def test_join_under_candidate_oserror(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = {"n": 0}
    real = Path.resolve

    def boom(self: Path, *a: object, **k: object) -> Path:
        calls["n"] += 1
        if calls["n"] >= 2:
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(PathValidationError, match="cannot resolve path"):
        paths_mod.join_under(tmp_path, "child")


def test_join_under_escape_when_inside_lies(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(paths_mod, "is_path_inside_root", lambda *_a, **_k: False)
    with pytest.raises(PathValidationError, match="escapes base"):
        paths_mod.join_under(tmp_path, "child")


def test_ast_grep_rules_fallback_when_packaged_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_is_file = Path.is_file

    def selective_is_file(self: Path) -> bool:
        if (
            "scanning" in self.parts
            and "resources" in self.parts
            and self.name == "spring_ast_grep_rules.yml"
        ):
            return False
        return real_is_file(self)

    monkeypatch.setattr(Path, "is_file", selective_is_file)
    result = paths_mod.ast_grep_rules_path()
    assert result.name == "spring_ast_grep_rules.yml"
    assert "scripts" in result.parts
