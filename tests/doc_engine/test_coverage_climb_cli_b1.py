"""Coverage climb B1: cli.py scan/success + parser/dispatch edges.

Q2 witness kind: mutmut_slice (scope: doc_engine.cli).
Do not flip ENFORCE=True.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine import cli

pytestmark = pytest.mark.domain_climb_sensor


def test_cmd_scan_success_writes_signals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "signals.json"

    class OkEngine:
        def __init__(self, _config: object) -> None:
            pass

        def scan(self, *_args: object, **_kwargs: object) -> dict:
            return {"files": {"a.java": {"kind": "controller"}}}

    monkeypatch.setattr(cli, "Engine", OkEngine)
    monkeypatch.setattr(cli, "scan_config", lambda *_a, **_k: object())
    assert (
        cli.cmd_scan(
            SimpleNamespace(
                repo=str(tmp_path),
                out=str(out),
                allow_codeql_build=True,
            )
        )
        == 0
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "files" in payload
    assert "Wrote signals" in capsys.readouterr().out


def test_cmd_docs_without_interview(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    signals = tmp_path / "signals.json"
    signals.write_text("{}", encoding="utf-8")
    out = tmp_path / "docs.json"

    class FakeEngine:
        def generate_docs(self, _signals: object, interview_answers=None):  # noqa: ANN001
            return {"interview": interview_answers, "ok": True}

    monkeypatch.setattr(cli, "Engine", FakeEngine)
    assert (
        cli.cmd_docs(
            SimpleNamespace(signals=str(signals), interview=None, out=str(out))
        )
        == 0
    )
    assert json.loads(out.read_text(encoding="utf-8"))["interview"] == {}


def test_cmd_pipeline_run_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[object] = []

    def fake_run(args: object) -> int:
        seen.append(args)
        return 9

    monkeypatch.setattr(cli, "run_pipeline", fake_run)
    ns = SimpleNamespace(mode="deterministic_only")
    assert cli.cmd_pipeline_run(ns) == 9
    assert seen == [ns]


def test_build_parser_wires_func() -> None:
    parser = cli.build_parser()
    args = parser.parse_args(
        ["coverage-measure", "--mode", "oracle", "--skip-pytest"]
    )
    assert callable(args.func)
    assert args.mode == "oracle"
    assert args.skip_pytest is True


def test_main_invokes_parsed_command(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeParser:
        def parse_args(self) -> SimpleNamespace:
            return SimpleNamespace(func=lambda _args: 3)

    monkeypatch.setattr(cli, "build_parser", FakeParser)
    assert cli.main() == 3


def test_module_main_exits_via_sys_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    import runpy
    import sys

    monkeypatch.setattr(
        sys,
        "argv",
        ["doc-engine", "size-ratchet", "--help"],
    )
    monkeypatch.delitem(sys.modules, "doc_engine.cli", raising=False)
    with pytest.raises(SystemExit) as exc:
        runpy.run_module("doc_engine.cli", run_name="__main__", alter_sys=True)
    assert exc.value.code == 0
