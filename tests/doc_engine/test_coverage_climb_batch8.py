"""Coverage climb batch8: gap_probe CLI + full_finish phase wiring."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.pipeline.local_runner_phases import full_finish as ff
from doc_engine.tools import gap_probe as gp

pytestmark = pytest.mark.domain_climb_sensor

def test_gap_probe_validate_and_summary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    args = SimpleNamespace(
        repo=tmp_path,
        signals=tmp_path / "missing.json",
        facts=tmp_path / "facts.jsonl",
    )
    assert gp._validate_input_paths(args) == 2
    signals = tmp_path / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    args.signals = signals
    args.facts = tmp_path / "missing_facts.jsonl"
    assert gp._validate_input_paths(args) == 2
    facts = tmp_path / "facts.jsonl"
    facts.write_text("{}\n", encoding="utf-8")
    args.facts = facts
    assert gp._validate_input_paths(args) is None
    err = capsys.readouterr().err
    assert "reserved" in err

    out = tmp_path / "out"
    out.mkdir()
    gp._print_gap_summary(
        {
            "uncertainty": {"U": 0.1},
            "rates": {
                "R_sym": {"rate": 0.0},
                "R_coll": {"rate": 0.1},
                "R_join": {"rate": 0.2},
                "R_lin": {"mean_rate": 0.3},
                "R_code_dep": {"rate": 0.4},
            },
            "measurement": {
                "truncation": {"L": 1},
                "delta_r_scoring_env": {"R_lin_mean": 0.01},
            },
        },
        out,
    )
    captured = capsys.readouterr()
    assert "gap_probe" in captured.err
    assert "Wrote" in captured.out

def test_gap_probe_main_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    signals = tmp_path / "signals.json"
    facts = tmp_path / "facts.jsonl"
    out = tmp_path / "gap"
    signals.write_text("{}", encoding="utf-8")
    facts.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(
        gp,
        "run_gap_probe",
        lambda *a, **k: (_ for _ in ()).throw(gp.CoveringPreconditionError("nope")),
    )
    assert (
        gp.main(
            [
                "--signals",
                str(signals),
                "--facts",
                str(facts),
                "--out",
                str(out),
            ]
        )
        == 3
    )
    monkeypatch.setattr(
        gp,
        "run_gap_probe",
        lambda *a, **k: {
            "uncertainty": {},
            "rates": {},
            "measurement": {},
        },
    )
    assert (
        gp.main(
            [
                "--signals",
                str(signals),
                "--facts",
                str(facts),
                "--out",
                str(out),
                "--covering",
                str(tmp_path / "covering.json"),
            ]
        )
        == 0
    )

def test_phase_full_finish_wires_gates(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
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

    monkeypatch.setattr(ff.gates, "run_gate_via_runner", lambda *a, **k: calls.append(k.get("gate_id") or a[1]))
    monkeypatch.setattr(ff.gates, "run_validate_all_artifacts", lambda *a, **k: None)
    monkeypatch.setattr(ff.gates, "run_pipeline_validators", lambda *a, **k: ("OK", "OK"))
    monkeypatch.setattr(ff, "_run_drift_check", lambda *a, **k: None)
    monkeypatch.setattr(ff, "_artifact_inventory", lambda *a, **k: None)
    monkeypatch.setattr(ff, "_write_certification_and_finish", lambda *a, **k: 0)

    assert ff.phase_full_finish(state) == 0
    assert any("check_pipeline_output" in c for c in calls)
