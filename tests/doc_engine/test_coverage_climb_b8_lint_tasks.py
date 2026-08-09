"""Coverage climb B8: lint_tasks anchor / waves CycleError edges.

Q2 adequacy witness: mutmut_slice on stf.validators.lint_tasks — asserts bite
non-path tokens skipped, missing anchor file FAIL, and CycleError on waves.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from stf.validators import lint_tasks as lt

pytestmark = pytest.mark.domain_climb_sensor


def test_anchor_rel_filters() -> None:
    assert lt._anchor_rel("plain") is None
    assert lt._anchor_rel("`src/a.java`") == "src/a.java"
    assert lt._anchor_rel("docs/readme.txt") is None


def test_lint_locate_anchors_missing(tmp_path: Path) -> None:
    events: list[tuple] = []

    def check(level: str, label: str, ok: bool, detail: str = "") -> None:
        events.append((level, label, ok, detail))

    task = SimpleNamespace(id="T1", locate="src/missing/Thing.java, bareword")
    lt._lint_locate_anchors(task, tmp_path, check)
    assert any(not ok and "Thing.java" in label for _l, label, ok, _d in events)


def test_lint_waves_cycle_error(monkeypatch: pytest.MonkeyPatch) -> None:
    events: list[tuple] = []

    def check(level: str, label: str, ok: bool, detail: str = "") -> None:
        events.append((level, label, ok, detail))

    class Boom(lt.CycleError):
        pass

    def raise_cycle(_deps):
        raise Boom("cycle")

    monkeypatch.setattr(lt, "compute_waves", raise_cycle)
    lt._lint_waves({"T1": ["T2"], "T2": ["T1"]}, None, check)
    assert any(not ok for _l, _label, ok, _d in events)
