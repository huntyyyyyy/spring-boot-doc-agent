"""Coverage climb B8: pipeline.runner start-fail / end-error / missing argv.

Q2 adequacy witness: mutmut_slice on doc_engine.pipeline.runner — asserts bite
start-stage failure return, end-stage error argv, missing argv_builder, and
_run_stage start_failure short-circuit.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline import runner as rn
from doc_engine.pipeline.context import StageKind, StageResult, StageSpec

pytestmark = pytest.mark.domain_climb_sensor


def _ctx(tmp_path: Path) -> SimpleNamespace:
    return SimpleNamespace(
        python="python",
        manifest_path=tmp_path / "m.json",
        out_dir=tmp_path,
        groups=None,
    )


def test_start_manifest_returns_failure(tmp_path: Path) -> None:
    spec = StageSpec(
        name="signal_scan",
        kind=StageKind.DETERMINISTIC,
        manifest_stage="signal_scan",
        argv_builder=lambda ctx: ["true"],
    )

    class FailRunner:
        def run(self, argv, context):
            return StageResult(success=False, detail="boom", error="start failed")

    out = rn._start_manifest_stage(FailRunner(), spec, _ctx(tmp_path))
    assert out is not None
    assert out.success is False


def test_end_manifest_argv_includes_error(tmp_path: Path) -> None:
    spec = StageSpec(
        name="signal_scan",
        kind=StageKind.DETERMINISTIC,
        manifest_stage="signal_scan",
        argv_builder=lambda ctx: ["true"],
    )
    result = StageResult(success=False, detail="d", error=None)
    argv = rn._end_manifest_argv(spec, _ctx(tmp_path), result)
    assert "--error" in argv
    assert "d" in argv or "stage failed" in argv


def test_execute_stage_missing_argv_builder(tmp_path: Path) -> None:
    spec = StageSpec(
        name="x",
        kind=StageKind.DETERMINISTIC,
        manifest_stage=None,
        argv_builder=None,
    )

    class Unused:
        def run(self, *a, **k):
            raise AssertionError("should not run")

    out = rn._execute_stage_body(Unused(), Unused(), spec, _ctx(tmp_path))
    assert out.success is False
    assert "argv_builder" in (out.error or out.detail or "")


def test_run_stage_returns_start_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    spec = StageSpec(
        name="signal_scan",
        kind=StageKind.DETERMINISTIC,
        manifest_stage="signal_scan",
        argv_builder=lambda ctx: ["true"],
    )
    fail = StageResult(success=False, detail="start", error="e")
    monkeypatch.setattr(rn, "_start_manifest_stage", lambda *a, **k: fail)
    pipe = rn.PipelineRunner(stages=[spec], validate_boundaries=False)
    assert pipe._run_stage(spec, _ctx(tmp_path)) is fail


def test_end_manifest_returns_prior_failure(tmp_path: Path) -> None:
    spec = StageSpec(
        name="signal_scan",
        kind=StageKind.DETERMINISTIC,
        manifest_stage="signal_scan",
        argv_builder=lambda ctx: ["true"],
    )
    prior = StageResult(success=False, detail="body", error="body err")

    class OkEnd:
        def run(self, argv, context):
            return StageResult(success=True)

    out = rn._end_manifest_stage(OkEnd(), spec, _ctx(tmp_path), prior)
    assert out is prior
