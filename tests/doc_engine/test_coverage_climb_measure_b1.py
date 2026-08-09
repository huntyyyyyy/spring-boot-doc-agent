"""Coverage climb B1: coverage_measure + size_measure hermetic edges.

Q2 witness kind: mutmut_slice (scope: doc_engine.ci.coverage_measure,
doc_engine.ci.size_measure, doc_engine.ci.coverage_measure_cli).
Do not flip ENFORCE=True.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from doc_engine.ci import coverage_measure as cm
from doc_engine.ci import coverage_measure_cli as cm_cli
from doc_engine.ci import size_measure
from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR
from doc_engine.ci.coverage_measure_modes import OracleMeasureStrategy
from doc_engine.ci.coverage_path_cohesion import PathCohesionError

pytestmark = pytest.mark.domain_climb_sensor

SAMPLE_XML = """\
<?xml version="1.0" ?>
<coverage line-rate="1" branch-rate="1" version="7.0" timestamp="1">
  <packages>
    <package name="demo" line-rate="1" branch-rate="1" complexity="0">
      <classes>
        <class name="ok.py" filename="src/ok.py"
               line-rate="1" branch-rate="1" complexity="0">
          <lines><line number="1" hits="1"/></lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
"""


def test_unlink_skips_coverage_directories(tmp_path: Path) -> None:
    (tmp_path / ".coverage").write_bytes(b"db")
    (tmp_path / ".coverage.d").mkdir()
    removed = cm._unlink_coverage_dbs(tmp_path)
    assert all(path.is_file() or not path.exists() for path in removed)
    assert not (tmp_path / ".coverage").exists()
    assert (tmp_path / ".coverage.d").is_dir()


def test_load_and_validate_missing_xml(tmp_path: Path) -> None:
    run = cm.MeasureRun(tmp_path)
    with pytest.raises(FileNotFoundError, match="missing coverage report"):
        run.load_and_validate()


def test_execute_pytest_fail_with_and_without_xml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run = cm.MeasureRun(tmp_path)
    monkeypatch.setattr(run, "wipe_local_artifacts", lambda: [])

    def fail_without_xml(**_kwargs: object) -> int:
        return 1

    monkeypatch.setattr(run, "run_pytest_cov", fail_without_xml)
    rc, xml = run.execute(fail_under=DEFAULT_FLOOR)
    assert rc == 1 and xml is None

    def fail_with_xml(**_kwargs: object) -> int:
        path = tmp_path / "coverage.xml"
        path.write_text(SAMPLE_XML, encoding="utf-8")
        return 1

    monkeypatch.setattr(run, "run_pytest_cov", fail_with_xml)
    rc2, xml2 = run.execute(fail_under=DEFAULT_FLOOR)
    assert rc2 == 1 and xml2 is not None
    assert xml2.name == "coverage.xml"


def test_validated_ok_reports_cohesion_and_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    run = cm.MeasureRun(tmp_path)
    monkeypatch.setattr(
        run,
        "load_and_validate",
        mock.Mock(side_effect=PathCohesionError("foreign path")),
    )
    rc, xml = run._validated_ok()
    assert rc == 2 and xml is None
    assert "error:" in capsys.readouterr().err

    monkeypatch.setattr(
        run,
        "load_and_validate",
        mock.Mock(side_effect=FileNotFoundError("missing coverage report")),
    )
    rc2, xml2 = run._validated_ok()
    assert rc2 == 2 and xml2 is None


def test_size_measure_empty_and_non_docstring_expr() -> None:
    assert size_measure.line_count("") == 0
    body = [ast.Expr(value=ast.Constant(value=1))]
    assert size_measure._strip_leading_docstring(body) is body
    named = [ast.Expr(value=ast.Name(id="x", ctx=ast.Load()))]
    assert size_measure._strip_leading_docstring(named) is named

    tree = ast.parse(
        "class Box:\n"
        "    def method(self):\n"
        "        return 1\n"
        "    async def amethod(self):\n"
        "        return 2\n"
    )
    out: dict[str, int] = {}
    size_measure._visit_functions(tree, "", "box.py", out)
    assert "box.py::Box.method" in out
    assert "box.py::Box.amethod" in out


def test_finish_report_propagates_gap_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    xml = tmp_path / "coverage.xml"
    xml.write_text(SAMPLE_XML, encoding="utf-8")
    args = SimpleNamespace(no_gap_report=False, floor=DEFAULT_FLOOR, worst=5)
    monkeypatch.setattr(cm_cli, "_print_oracle_gap", lambda *_a, **_k: 2)
    assert (
        cm_cli._finish_report(
            rc=0,
            xml_path=xml,
            args=args,
            strategy=OracleMeasureStrategy(),
            root=tmp_path,
        )
        == 2
    )
