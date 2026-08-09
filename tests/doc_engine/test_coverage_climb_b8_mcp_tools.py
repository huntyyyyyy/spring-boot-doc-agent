"""Coverage climb B8: mcp_tools pin OSError / context_packet / dependents.

Q2 adequacy witness: mutmut_slice on doc_engine.query.mcp_tools — asserts bite
resolve OSError, missing run_dir for context_packet, and dependents dispatch.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.query import mcp_tools as mt
from doc_engine.query.load import QueryError, QueryPathError

pytestmark = pytest.mark.domain_climb_sensor


def test_pin_path_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    real = Path.resolve

    def boom(self: Path, *a: object, **k: object) -> Path:
        if "bad" in str(self):
            raise OSError("io")
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "resolve", boom)
    with pytest.raises(QueryPathError, match="cannot resolve"):
        mt._pin_path(tmp_path / "bad", root=tmp_path)


def test_context_packet_requires_run_dir(tmp_path: Path) -> None:
    with pytest.raises(QueryError, match="run_dir"):
        mt._dispatch_context_packet({"request": "q"}, tmp_path)


def test_query_dependents_dispatches(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    signals = tmp_path / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(mt, "_pin_path", lambda raw, root: Path(raw))
    monkeypatch.setattr(
        mt,
        "run_query",
        lambda kind, **k: {"kind": kind, "ok": True},
    )
    out = mt._query_dependents({"signals": str(signals)}, tmp_path)
    assert out["kind"] == "dependents"
