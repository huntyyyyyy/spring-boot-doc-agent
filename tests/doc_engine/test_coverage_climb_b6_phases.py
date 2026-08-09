"""Coverage climb B6: post_stage0 + generative phase edges.

Q2 adequacy witness: mutmut_slice on local_runner_phases.post_stage0 and
generative — asserts bite SCAN_ONLY finish, evidence pool logging, generative
abort vs readme note (not vacuous coverage padding).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline.compliance import ComplianceProfile
from doc_engine.pipeline.local_runner_phases import generative as gen
from doc_engine.pipeline.local_runner_phases import post_stage0 as post

pytestmark = pytest.mark.domain_climb_sensor


class _Log:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def rule(self, msg: str) -> None:
        self.lines.append(f"rule:{msg}")

    def __call__(self, msg: str = "") -> None:
        self.lines.append(str(msg))


class _Runner:
    def __init__(self, *, aborted: bool = False) -> None:
        self.aborted = aborted

    def run(self, *a: object, **k: object) -> int:
        return 0


class _Ctx:
    def __init__(self) -> None:
        self.signals = None
        self.groups = {"num_groups": 2, "total_files_considered": 5}
        self.pool = None


def _certified_state(tmp_path: Path, signals: Path, out: Path) -> SimpleNamespace:
    return SimpleNamespace(
        pipeline_ctx=_Ctx(),
        signals_path=str(signals),
        profile=ComplianceProfile.CERTIFIED,
        log=_Log(),
        runner=_Runner(),
        repo_path=str(tmp_path),
        out_dir=str(out),
        allow_mock=True,
    )


def test_post_stage0_evidence_pool(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    signals = tmp_path / "spring_signals.json"
    signals.write_text(json.dumps({"evidence": {}}), encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    state = _certified_state(tmp_path, signals, out)
    monkeypatch.setattr(
        post, "load_citations", lambda *_a, **_k: {"api": ["a.java:1"], "empty": []}
    )
    assert post.phase_post_stage0(state) is None
    assert state.pipeline_ctx.signals is not None
    assert any("evidence pool" in line for line in state.log.lines)
    assert any("groups:" in line for line in state.log.lines)


def test_post_stage0_scan_only_finish(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    signals = tmp_path / "spring_signals.json"
    signals.write_text(json.dumps({"evidence": {}}), encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    finish: list[object] = []
    monkeypatch.setattr(
        post.gates, "run_gate_via_runner", lambda *a, **k: finish.append("gate")
    )
    monkeypatch.setattr(post.gates, "run_validate_spring_signals", lambda *_a: None)
    monkeypatch.setattr(post, "artifact_inventory", lambda *_a: finish.append("inv"))
    monkeypatch.setattr(
        post,
        "write_certification_and_finish",
        lambda *a, **k: finish.append(k.get("success_lines")) or 0,
    )
    scan_state = SimpleNamespace(
        pipeline_ctx=_Ctx(),
        signals_path=str(signals),
        profile=ComplianceProfile.SCAN_ONLY,
        log=_Log(),
        runner=_Runner(),
        repo_path=str(tmp_path),
        out_dir=str(out),
        allow_mock=False,
    )
    assert post.phase_post_stage0(scan_state) == 0
    assert "gate" in finish and "inv" in finish
    assert any("scan-only" in str(item).lower() for item in finish if item)


def test_generative_abort_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    recorded: list[object] = []

    class FakeGenRunner:
        def __init__(self, *a: object, **k: object) -> None:
            recorded.append("gen")

        def run(self, ctx: object) -> list[str]:
            return ["mock-stage"]

    monkeypatch.setattr(gen, "PipelineRunner", FakeGenRunner)
    monkeypatch.setattr(
        gen,
        "record_pipeline_stage_results",
        lambda runner, results, ok_status="MOCK": recorded.append(ok_status),
    )
    finish_kw: dict = {}
    monkeypatch.setattr(
        gen,
        "write_certification_and_finish",
        lambda *a, **kwargs: finish_kw.update(kwargs) or 4,
    )
    abort_state = SimpleNamespace(
        log=_Log(),
        runner=_Runner(aborted=True),
        pipeline_ctx={"x": 1},
        mock_executor=object(),
        generative_specs=["summarize"],
        profile=ComplianceProfile.CERTIFIED,
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out"),
        allow_mock=True,
    )
    assert gen.phase_generative(abort_state) == 4
    assert "aborted after generative" in finish_kw["notice_lines"][0]


def test_generative_readme_note(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeGenRunner:
        def __init__(self, *a: object, **k: object) -> None:
            return None

        def run(self, ctx: object) -> list[str]:
            return ["mock-stage"]

    monkeypatch.setattr(gen, "PipelineRunner", FakeGenRunner)
    monkeypatch.setattr(
        gen, "record_pipeline_stage_results", lambda *a, **k: None
    )
    (tmp_path / "README.md").write_text("# hi\n", encoding="utf-8")
    ok_log = _Log()
    ok_state = SimpleNamespace(
        log=ok_log,
        runner=_Runner(aborted=False),
        pipeline_ctx={"x": 1},
        mock_executor=object(),
        generative_specs=["summarize"],
        profile=ComplianceProfile.CERTIFIED,
        repo_path=str(tmp_path),
        out_dir=str(tmp_path / "out2"),
        allow_mock=True,
    )
    assert gen.phase_generative(ok_state) is None
    assert any("already exists" in line for line in ok_log.lines)
