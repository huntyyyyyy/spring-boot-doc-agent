"""Fake log/runner + monkeypatch setup for deterministic-only phase tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from doc_engine.pipeline.compliance import ComplianceProfile
from doc_engine.pipeline.local_runner_phases import deterministic as det


class FakeLog:
    def __init__(self, calls: list[str]) -> None:
        self._calls = calls

    def rule(self, msg: str) -> None:
        self._calls.append(f"rule:{msg}")

    def __call__(self, msg: str = "") -> None:
        self._calls.append(str(msg))


class FakeRunner:
    def __init__(self, calls: list[str]) -> None:
        self._calls = calls

    def run(self, name, argv, gate=False, gate_id=None, env=None):
        self._calls.append(name)
        return 0


def patch_det_phase_side_effects(
    monkeypatch: pytest.MonkeyPatch,
    calls: list[str],
    finish_kwargs: dict[str, Any],
) -> None:
    def fake_finish(*_a, **kwargs):
        finish_kwargs.update(kwargs)
        calls.append("finish")
        return 0

    monkeypatch.setattr(
        det.gates,
        "run_gate_via_runner",
        lambda *a, **k: calls.append(k.get("gate_id") or "gate"),
    )
    monkeypatch.setattr(det.gates, "run_validate_all_artifacts", lambda *_a, **_k: None)
    monkeypatch.setattr(det, "run_drift_check", lambda *_a, **_k: calls.append("drift"))
    monkeypatch.setattr(det, "artifact_inventory", lambda *_a, **_k: calls.append("inv"))
    monkeypatch.setattr(det, "write_certification_and_finish", fake_finish)


def make_phase_state(tmp_path, *, profile, generative_specs, out_name, until_stage, allow_mock, calls):
    return SimpleNamespace(
        profile=profile,
        generative_specs=generative_specs,
        log=FakeLog(calls),
        runner=FakeRunner(calls),
        args=SimpleNamespace(skip_drift=True, prior_signals=None),
        out_dir=str(tmp_path / out_name) if out_name else str(tmp_path),
        manifest=str(tmp_path / "m.json"),
        signals_path=str(tmp_path / "s.json"),
        preflight_path=str(tmp_path / "p.json"),
        repo_path=str(tmp_path),
        until_stage=until_stage,
        allow_mock=allow_mock,
    )
