"""Coverage climb: cli.py optional-arg facades + scan re-raise edges."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine import cli

pytestmark = pytest.mark.domain_climb_sensor


def _capture_main(monkeypatch: pytest.MonkeyPatch, target: str) -> list[list[str]]:
    captured: list[list[str]] = []

    def fake_main(argv: list[str] | None = None) -> int:
        captured.append(list(argv or []))
        return 0

    monkeypatch.setattr(target, fake_main)
    return captured


def test_cmd_scan_rethrows_non_codeql_errors(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class BoomEngine:
        def __init__(self, _config: object) -> None:
            pass

        def scan(self, *_args: object, **_kwargs: object) -> dict:
            raise RuntimeError("unexpected scanner failure")

    monkeypatch.setattr(cli, "Engine", BoomEngine)
    monkeypatch.setattr(cli, "scan_config", lambda *_a, **_k: object())
    with pytest.raises(RuntimeError, match="unexpected"):
        cli.cmd_scan(
            SimpleNamespace(
                repo=str(tmp_path),
                out=str(tmp_path / "out.json"),
                allow_codeql_build=False,
            )
        )


def test_pipeline_gates_omits_optional_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_main(monkeypatch, "doc_engine.pipeline.live_gates.main")
    assert (
        cli.cmd_pipeline_gates(
            SimpleNamespace(
                out_dir="/run",
                target_repo="/repo",
                docs_dir=None,
                compliance_profile=None,
                strict_citations=False,
                no_write_check=False,
            )
        )
        == 0
    )
    argv = captured[0]
    assert "--docs-dir" not in argv
    assert "--compliance-profile" not in argv
    assert "--strict-citations" not in argv
    assert "--no-write-check" not in argv


def test_certification_verify_without_allow_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_main(monkeypatch, "doc_engine.tools.certification.main")
    assert (
        cli.cmd_certification_verify(
            SimpleNamespace(path="/c.json", allow_mock=False)
        )
        == 0
    )
    assert captured[0] == ["/c.json"]


def test_quality_gates_and_gap_average_argv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    q_cap = _capture_main(monkeypatch, "doc_engine.ci.quality_gates.main")
    assert (
        cli.cmd_quality_gates(
            SimpleNamespace(
                compare_ref="origin/main",
                coverage_xml=None,
                skip_coverage=False,
                no_fail_fast=False,
            )
        )
        == 0
    )
    assert q_cap[0] == ["--compare-ref", "origin/main"]

    assert (
        cli.cmd_quality_gates(
            SimpleNamespace(
                compare_ref="HEAD~1",
                coverage_xml=Path("coverage.xml"),
                skip_coverage=True,
                no_fail_fast=True,
            )
        )
        == 0
    )
    joined = " ".join(q_cap[1])
    assert "--coverage-xml" in joined and "--skip-coverage" in joined
    assert "--no-fail-fast" in joined

    g_cap = _capture_main(monkeypatch, "doc_engine.ci.coverage_gap_average.main")
    assert (
        cli.cmd_coverage_gap_average(
            SimpleNamespace(
                coverage_xml=None,
                floor=None,
                worst=None,
                markdown=False,
                append_github_summary=False,
            )
        )
        == 0
    )
    assert g_cap[0] == []
    assert (
        cli.cmd_coverage_gap_average(
            SimpleNamespace(
                coverage_xml=Path("c.xml"),
                floor=98.7,
                worst=10,
                markdown=True,
                append_github_summary=True,
            )
        )
        == 0
    )
    assert "--markdown" in g_cap[1] and "--append-github-summary" in g_cap[1]


def test_coverage_measure_and_ratchet_argv_builders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    empty = SimpleNamespace(
        mode=None,
        scope=None,
        floor=None,
        worst=None,
        skip_pytest=False,
        no_gap_report=False,
        pytest_args=[],
    )
    assert cli._coverage_measure_argv(empty) == []
    full = SimpleNamespace(
        mode="climb",
        scope="doc_engine.ci",
        floor=98.7,
        worst=5,
        skip_pytest=True,
        no_gap_report=True,
        pytest_args=["tests/ci"],
    )
    argv = cli._coverage_measure_argv(full)
    assert "--mode" in argv and "climb" in argv
    assert "--skip-pytest" in argv and "--no-gap-report" in argv
    assert "tests/ci" in argv

    m_cap = _capture_main(monkeypatch, "doc_engine.ci.coverage_measure_cli.main")
    assert cli.cmd_coverage_measure(full) == 0
    assert m_cap[0] == argv

    c_cap = _capture_main(monkeypatch, "doc_engine.ci.complexipy_ratchet.main")
    assert cli.cmd_complexipy_ratchet(SimpleNamespace(baseline=None, update=False)) == 0
    assert c_cap[0] == []
    assert (
        cli.cmd_complexipy_ratchet(
            SimpleNamespace(baseline=Path("b.json"), update=True)
        )
        == 0
    )
    assert "--update" in c_cap[1]

    s_cap = _capture_main(monkeypatch, "doc_engine.ci.size_ratchet.main")
    assert cli.cmd_size_ratchet(SimpleNamespace(baseline=None, update=False)) == 0
    assert s_cap[0] == []
    assert (
        cli.cmd_size_ratchet(SimpleNamespace(baseline=Path("s.json"), update=True))
        == 0
    )
    assert "--baseline" in s_cap[1]


def test_main_dispatches_parsed_func(monkeypatch: pytest.MonkeyPatch) -> None:
    called: list[object] = []

    class FakeParser:
        def parse_args(self) -> SimpleNamespace:
            return SimpleNamespace(func=lambda args: called.append(args) or 7)

    monkeypatch.setattr(cli, "build_parser", FakeParser)
    assert cli.main() == 7
    assert len(called) == 1
