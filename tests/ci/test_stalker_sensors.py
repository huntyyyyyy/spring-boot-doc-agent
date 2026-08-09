"""E-STK1 stalker sensors — characterization for G1–G6 runners."""

from __future__ import annotations

import importlib
from datetime import date
from pathlib import Path

import pytest

from doc_engine.ci import stalker_sensors as stalker_pkg
from doc_engine.ci.stalker_sensors.collect_syntax import scan_collect_syntax
from doc_engine.ci.stalker_sensors.facade_api import scan_facade_api
from doc_engine.ci.stalker_sensors.finding_records import ALL_KINDS, StalkerFinding
from doc_engine.ci.stalker_sensors.ledger_write import write_findings_ledger
from doc_engine.ci.stalker_sensors.parallel_tip import scan_parallel_tip
from doc_engine.ci.stalker_sensors.policy_verify import scan_policy_verify
from doc_engine.ci.stalker_sensors.scan import run_all_sensors, scan_and_write
from doc_engine.ci.stalker_sensors.schema_skew import scan_schema_skew
from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta


def test_schema_skew_clean_on_tip() -> None:
    assert scan_schema_skew(repo_root()) == []


def test_policy_verify_pack_healthy() -> None:
    assert scan_policy_verify(repo_root()) == []


def test_single_active_tip_in_backlog() -> None:
    assert scan_parallel_tip(repo_root()) == []


def test_run_all_sensors_returns_list() -> None:
    findings = run_all_sensors(repo_root())
    assert isinstance(findings, list)
    for item in findings:
        assert item.kind in ALL_KINDS


def test_package_getattr_exports_run_all_sensors() -> None:
    fn = stalker_pkg.run_all_sensors
    assert callable(fn)
    with pytest.raises(AttributeError):
        getattr(stalker_pkg, "not_a_sensor_symbol")


def test_finding_as_dict_round_trip() -> None:
    item = StalkerFinding("ratchet_schema_skew", "sum", "ev", backlog_pointer="P15.1")
    assert item.as_dict()["kind"] == "ratchet_schema_skew"


def test_ledger_write_empty_and_populated(tmp_path: Path) -> None:
    empty = write_findings_ledger(tmp_path, [], day=date(2026, 8, 9))
    text = empty.read_text(encoding="utf-8")
    assert "No G1–G6 findings." in text
    filled = write_findings_ledger(
        tmp_path,
        [StalkerFinding("process_parallel_tip", "two tips", "a | b")],
        day=date(2026, 8, 9),
    )
    body = filled.read_text(encoding="utf-8")
    assert "`process_parallel_tip`" in body
    assert "two tips" in body


def test_scan_and_write_ledger(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "doc_engine.ci.stalker_sensors.scan.run_all_sensors",
        lambda _root: [StalkerFinding("collect_or_syntax", "boom", "x")],
    )
    out = scan_and_write(tmp_path, write_ledger=True)
    assert len(out) == 1
    assert list((tmp_path / "docs/research/findings").glob("*-stalker-scan.md"))
    assert scan_and_write(tmp_path, write_ledger=False) == out


def test_parallel_tip_missing_none_and_multi(tmp_path: Path) -> None:
    assert scan_parallel_tip(tmp_path)[0].kind == "process_parallel_tip"
    backlog = tmp_path / "docs/research/quality-backlog.md"
    backlog.parent.mkdir(parents=True)
    backlog.write_text("# no active\n", encoding="utf-8")
    assert "no **Active:**" in scan_parallel_tip(tmp_path)[0].summary
    backlog.write_text(
        "**Active:** E-A Implement\n**Active:** E-B Implement\n",
        encoding="utf-8",
    )
    multi = scan_parallel_tip(tmp_path)
    assert multi and "2 Active" in multi[0].summary


def test_schema_skew_missing_and_mismatch(tmp_path: Path) -> None:
    assert scan_schema_skew(tmp_path)
    code = tmp_path / "scripts/ci/check_code_quality.py"
    code.parent.mkdir(parents=True)
    code.write_text("SCHEMA_VERSION = 99\n", encoding="utf-8")
    bas = tmp_path / "scripts/ratchets/code_quality_baseline.json"
    bas.parent.mkdir(parents=True)
    bas.write_text('{"schema_version": 1}\n', encoding="utf-8")
    findings = scan_schema_skew(tmp_path)
    assert any("SCHEMA_VERSION=99" in f.summary or "missing pair" in f.summary for f in findings)


def test_policy_verify_json_and_schema_gaps(tmp_path: Path) -> None:
    for rel in (
        "scripts/ratchets/code_quality_baseline.json",
        "scripts/ratchets/size_baseline.json",
        "scripts/ratchets/complexipy_baseline.json",
    ):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not-json", encoding="utf-8")
    assert any("JSON bad" in f.summary for f in scan_policy_verify(tmp_path))
    for rel in (
        "scripts/ratchets/code_quality_baseline.json",
        "scripts/ratchets/size_baseline.json",
        "scripts/ratchets/complexipy_baseline.json",
    ):
        (tmp_path / rel).write_text("{}\n", encoding="utf-8")
    assert any("schema_version" in f.summary for f in scan_policy_verify(tmp_path))


def test_policy_verify_import_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for rel in (
        "scripts/ratchets/code_quality_baseline.json",
        "scripts/ratchets/size_baseline.json",
        "scripts/ratchets/complexipy_baseline.json",
    ):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"schema_version": 1}\n', encoding="utf-8")
    g2 = tmp_path / "tests/ci/test_g2_prelude_core_scope.py"
    g2.parent.mkdir(parents=True)
    g2.write_text("# witness\n", encoding="utf-8")

    def _boom(name: str) -> object:
        raise ImportError(name)

    monkeypatch.setattr(importlib, "import_module", _boom)
    assert any("import failed" in f.summary for f in scan_policy_verify(tmp_path))


def test_collect_syntax_flags_bad_py(tmp_path: Path) -> None:
    bad = tmp_path / "src/doc_engine/ci/broken.py"
    bad.parent.mkdir(parents=True)
    bad.write_text("def oops(\n", encoding="utf-8")
    (tmp_path / "scripts/ci").mkdir(parents=True)
    (tmp_path / "tests/ci").mkdir(parents=True)
    hits = scan_collect_syntax(tmp_path)
    assert any(h.kind == "collect_or_syntax" for h in hits)


def test_facade_api_missing_script(tmp_path: Path) -> None:
    hits = scan_facade_api(tmp_path)
    assert hits and "missing" in hits[0].summary


def test_import_reload_sensors_module() -> None:
    mod = importlib.import_module("doc_engine.ci.stalker_sensors")
    assert hasattr(mod, "__getattr__")
