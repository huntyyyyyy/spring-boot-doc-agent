"""Coverage climb B9: gates captured body / abort; cohesion wrappers.

Q2 adequacy witness: mutmut_slice on pipeline.gates + coverage_path_cohesion —
asserts bite stdout/stderr concat, critical abort, and cohesion compat wrappers.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.ci import coverage_path_cohesion as cpc
from doc_engine.pipeline import gates as gates_mod

pytestmark = pytest.mark.domain_climb_sensor

def test_cohesion_compat_wrappers(tmp_path: Path) -> None:
    good = tmp_path / "a.py"
    good.write_text("x", encoding="utf-8")
    assert cpc.cohesion_violations([str(good)], tmp_path) == []
    cpc.assert_paths_cohesive([str(good)], tmp_path)
    with pytest.raises(cpc.PathCohesionError):
        cpc.assert_paths_cohesive(["/elsewhere"], tmp_path)

def test_run_subprocess_combines_streams(monkeypatch: pytest.MonkeyPatch) -> None:
    class Proc:
        returncode = 7
        stdout = "out"
        stderr = "err"

    monkeypatch.setattr("subprocess.run", lambda *a, **k: Proc())
    code, body = gates_mod.run_subprocess_gate(["true"])
    assert code == 7
    assert body == "outerr"

def test_record_gate_outcome_aborts() -> None:
    runner = SimpleNamespace(
        log=lambda *_a, **_k: None,
        record=lambda *_a, **_k: None,
        _record_gate=lambda *_a, **_k: None,
        keep_going=False,
        aborted=False,
    )
    gates_mod._record_gate_outcome(
        runner, "lab", 1, 0.1, gate=True, gate_id="g1", critical=True
    )
    assert runner.aborted is True
