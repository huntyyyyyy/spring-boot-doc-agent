"""Coverage climb B7: query.load OSError resolve / read edges.

Q2 adequacy witness: mutmut_slice on doc_engine.query.load — asserts bite
server-root resolve OSError, root resolve OSError, and read OSError.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.query import load as load_mod
from doc_engine.query.load import QueryError, QueryPathError

pytestmark = pytest.mark.domain_climb_sensor


def test_require_server_root_oserror(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("DOC_ENGINE_ROOT", str(tmp_path / "badroot"))
    real = Path.resolve

    def boom(self: Path, *a: object, **k: object) -> Path:
        if "badroot" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(QueryPathError, match="cannot resolve server root"):
        load_mod.require_server_root()


def test_resolve_root_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    path.write_text("{}", encoding="utf-8")
    real = Path.resolve
    state = {"seen_path": False}

    def boom(self: Path, *a: object, **k: object) -> Path:
        text = str(self)
        if text.endswith("a.json") or self.name == "a.json":
            state["seen_path"] = True
            return real(self, *a, **k)
        if state["seen_path"]:
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(QueryPathError, match="cannot resolve root"):
        load_mod._resolve(path, root=tmp_path / "rooty")


def test_read_artifact_text_oserror(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = tmp_path / "x.json"
    path.write_text("{}", encoding="utf-8")

    def read_boom(*_a: object, **_k: object) -> str:
        raise OSError("io")

    monkeypatch.setattr(Path, "read_text", read_boom)
    with pytest.raises(QueryError, match="cannot read"):
        load_mod._read_artifact_text(path, kind="JSON")
