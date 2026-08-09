"""Coverage climb B8: coverage_path_cohesion absolute / foreign / resolve.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.coverage_path_cohesion —
asserts bite empty absolute miss, Windows-looking path ValueError, escape None,
and foreign-segment / assert_cohesive raise.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci import coverage_path_cohesion as cpc

pytestmark = pytest.mark.domain_climb_sensor


def test_looks_absolute_variants() -> None:
    assert cpc._looks_absolute("") is False
    assert cpc._looks_absolute("   ") is False
    assert cpc._looks_absolute("/abs/path") is True
    assert cpc._looks_absolute(r"C:\Users\x") is True


def test_candidate_foreign_os_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="foreign-os"):
        cpc._candidate_under_root(r"C:\Users\x\file.py", tmp_path)


def test_resolve_and_violations(tmp_path: Path) -> None:
    good = tmp_path / "src" / "a.py"
    good.parent.mkdir(parents=True)
    good.write_text("x", encoding="utf-8")
    assert cpc._resolve_under_root(str(good), tmp_path) == good.resolve()
    assert cpc._resolve_under_root("/totally/elsewhere.py", tmp_path) is None
    guard = cpc.PathCohesionGuard(tmp_path)
    bad = guard.violations(["", "  ", "/elsewhere/x.py", str(good)])
    assert any("escapes" in v or "foreign" in v for v in bad)
    with pytest.raises(cpc.PathCohesionError):
        guard.assert_cohesive(["/elsewhere/x.py"])
