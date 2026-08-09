"""Coverage climb B8: size_ratchet issues exit + __main__; quality gap skip.

Q2 adequacy witness: mutmut_slice on size_ratchet / quality_gate_checks —
asserts bite issues→exit 1, __main__ SystemExit, and missing coverage.xml skip.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

from doc_engine.ci import quality_gate_checks as qgc
from doc_engine.ci import size_ratchet as sr

pytestmark = pytest.mark.domain_climb_sensor


def test_report_gap_average_skips_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    called = {"n": 0}

    def mark(*_a, **_k):
        called["n"] = 1
        return 0

    monkeypatch.setattr(qgc, "_run", mark)
    qgc.report_gap_average(tmp_path / "nope.xml")
    assert called["n"] == 0


def test_size_ratchet_main_issues_exit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    baseline = tmp_path / "baseline.json"
    baseline.write_text(
        '{"file_offender_count":0,"fn_offender_count":0}', encoding="utf-8"
    )
    monkeypatch.setattr(sr, "measure_tree", lambda: ({}, []))
    monkeypatch.setattr(sr, "hard_file_offenders", lambda *_a, **_k: [])
    monkeypatch.setattr(sr, "hard_fn_offenders", lambda *_a, **_k: [])
    monkeypatch.setattr(
        sr,
        "load_baseline",
        lambda *_a, **_k: {"file_offender_count": 0, "fn_offender_count": 0},
    )
    monkeypatch.setattr(sr, "soft_advisories", lambda *_a, **_k: [])
    monkeypatch.setattr(sr, "_print_soft_advisories", lambda *_a, **_k: None)
    monkeypatch.setattr(sr, "compare", lambda *_a, **_k: ["grew"])
    printed: list[str] = []
    monkeypatch.setattr(sr, "_print_issues", lambda issues: printed.extend(issues))
    assert sr.main(["--baseline", str(baseline)]) == 1
    assert printed == ["grew"]


def test_size_ratchet_dunder_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sr, "main", lambda argv=None: 0)
    monkeypatch.setattr(sys, "argv", ["size_ratchet"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("doc_engine.ci.size_ratchet", run_name="__main__")
    assert exc.value.code == 0
