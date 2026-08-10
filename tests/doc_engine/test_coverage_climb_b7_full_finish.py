"""Coverage climb B7: full_finish missing suite + docs-in-target log.

Q2 adequacy witness: mutmut_slice on local_runner_phases.full_finish — asserts
bite RuntimeError when split suites absent and docs_in_target_repo inventory
log lines (not padding).
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline.local_runner_phases import full_finish as ff

pytestmark = pytest.mark.domain_climb_sensor


def test_phase_full_finish_raises_without_split_suite(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[str] = []

    class FakeLog:
        def rule(self, msg: str) -> None:
            calls.append(f"rule:{msg}")

        def __call__(self, msg: str = "") -> None:
            calls.append(msg)

    class FakeRunner:
        def run(self, name, argv, gate=False, gate_id=None, env=None):
            calls.append(name)
            return 0

    empty = tmp_path / "empty_tests"
    empty.mkdir()
    monkeypatch.setattr(ff, "REPO_ROOT", str(tmp_path))
    (tmp_path / "tests" / "doc_engine").mkdir(parents=True)

    state = SimpleNamespace(
        log=FakeLog(),
        runner=FakeRunner(),
        args=SimpleNamespace(docs_in_target_repo=False),
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out"),
        docs_dir=str(tmp_path / "docs"),
        py="python",
        strict_citations_effective=False,
        manifest=str(tmp_path / "m.json"),
        signals_path=str(tmp_path / "signals.json"),
        preflight_path=str(tmp_path / "pre.json"),
        profile="local",
        allow_mock=True,
    )
    (tmp_path / "out").mkdir()
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(
        ff.gates, "run_gate_via_runner", lambda *a, **k: calls.append("gate")
    )
    monkeypatch.setattr(ff.gates, "run_validate_all_artifacts", lambda *a, **k: None)
    monkeypatch.setattr(
        ff.gates, "run_pipeline_validators", lambda *a, **k: ("OK", "OK")
    )
    with pytest.raises(RuntimeError, match="test_pipeline_stages_"):
        ff.phase_full_finish(state)


def test_phase_full_finish_docs_in_target_inventory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls: list[str] = []

    class FakeLog:
        def rule(self, msg: str) -> None:
            calls.append(f"rule:{msg}")

        def __call__(self, msg: str = "") -> None:
            calls.append(msg)

    class FakeRunner:
        def run(self, name, argv, gate=False, gate_id=None, env=None):
            calls.append(name)
            return 0

    suite = tmp_path / "tests" / "doc_engine"
    suite.mkdir(parents=True)
    (suite / "test_pipeline_stages_core.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )
    monkeypatch.setattr(ff, "REPO_ROOT", str(tmp_path))

    docs = tmp_path / "target_docs"
    docs.mkdir()
    state = SimpleNamespace(
        log=FakeLog(),
        runner=FakeRunner(),
        args=SimpleNamespace(docs_in_target_repo=True),
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out"),
        docs_dir=str(docs),
        py="python",
        strict_citations_effective=False,
        manifest=str(tmp_path / "m.json"),
        signals_path=str(tmp_path / "signals.json"),
        preflight_path=str(tmp_path / "pre.json"),
        profile="local",
        allow_mock=True,
    )
    (tmp_path / "out").mkdir()
    monkeypatch.setattr(
        ff.gates, "run_gate_via_runner", lambda *a, **k: calls.append("gate")
    )
    monkeypatch.setattr(ff.gates, "run_validate_all_artifacts", lambda *a, **k: None)
    monkeypatch.setattr(
        ff.gates, "run_pipeline_validators", lambda *a, **k: ("OK", "OK")
    )
    monkeypatch.setattr(ff, "run_drift_check", lambda *a, **k: None)
    monkeypatch.setattr(ff, "artifact_inventory", lambda *a, **k: None)
    monkeypatch.setattr(ff, "write_certification_and_finish", lambda *a, **k: 0)

    assert ff.phase_full_finish(state) == 0
    assert any("fourteen docs" in c for c in calls)
