"""Coverage climb: coverage_measure_cli + size_measure hermetic edges.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.coverage_measure_cli /
size_measure (assert refuse-floor / PathCohesion edges).
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pytest

from doc_engine.ci import coverage_measure_cli as cm_cli
from doc_engine.ci import size_measure
from doc_engine.ci.coverage_artifact_policy import DEFAULT_FLOOR
from doc_engine.ci.coverage_measure_modes import ClimbMeasureStrategy, OracleMeasureStrategy
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


def test_build_strategy_value_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert cm_cli._build_strategy(SimpleNamespace(mode="climb", scope=None)) is None
    assert "error:" in capsys.readouterr().err


def test_validate_cli_args_oracle_and_climb(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    oracle = OracleMeasureStrategy()
    monkeypatch.setattr(cm_cli, "checkout_root", lambda: Path.cwd())
    assert (
        cm_cli._validate_cli_args(
            SimpleNamespace(floor=DEFAULT_FLOOR - 0.1), oracle
        )
        == 2
    )
    err1 = capsys.readouterr().err.lower()
    assert "refuse" in err1 or "weaken" in err1

    climb = ClimbMeasureStrategy(scope_package="doc_engine.ci")
    assert (
        cm_cli._validate_cli_args(SimpleNamespace(floor=DEFAULT_FLOOR + 1), climb)
        == 2
    )
    assert "climb" in capsys.readouterr().err.lower()

    other = Path("/tmp")
    monkeypatch.setattr(cm_cli, "checkout_root", lambda: other)
    assert cm_cli._validate_cli_args(SimpleNamespace(floor=DEFAULT_FLOOR), oracle) == 2
    assert "checkout root" in capsys.readouterr().err

    monkeypatch.setattr(cm_cli, "checkout_root", lambda: Path.cwd())
    assert cm_cli._validate_cli_args(SimpleNamespace(floor=DEFAULT_FLOOR), oracle) is None


def test_finish_report_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    args = SimpleNamespace(no_gap_report=True, floor=DEFAULT_FLOOR, worst=5)
    assert (
        cm_cli._finish_report(
            rc=3,
            xml_path=None,
            args=args,
            strategy=OracleMeasureStrategy(),
            root=tmp_path,
        )
        == 3
    )
    xml = tmp_path / "coverage.xml"
    xml.write_text(SAMPLE_XML, encoding="utf-8")
    assert (
        cm_cli._finish_report(
            rc=0,
            xml_path=xml,
            args=args,
            strategy=OracleMeasureStrategy(),
            root=tmp_path,
        )
        == 0
    )
    assert "wrote" in capsys.readouterr().out

    climb = ClimbMeasureStrategy(scope_package="doc_engine.ci")
    args2 = SimpleNamespace(no_gap_report=False, floor=DEFAULT_FLOOR, worst=5)
    assert (
        cm_cli._finish_report(
            rc=1, xml_path=xml, args=args2, strategy=climb, root=tmp_path
        )
        == 1
    )

    with mock.patch(
        "doc_engine.ci.coverage_measure_cli.build_report_from_coverage",
        side_effect=PathCohesionError("bad path"),
    ):
        assert cm_cli._print_oracle_gap(xml, args2, tmp_path) == 2
    assert "error:" in capsys.readouterr().err


def test_main_skip_pytest_oracle_gap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "src").mkdir()
    xml = tmp_path / "coverage.xml"
    xml.write_text(SAMPLE_XML, encoding="utf-8")
    monkeypatch.setattr(cm_cli, "checkout_root", lambda: tmp_path)

    def fake_execute(self, **_kwargs):  # noqa: ANN001
        return 0, xml

    monkeypatch.setattr(
        "doc_engine.ci.coverage_measure.MeasureRun.execute", fake_execute
    )
    assert cm_cli.main(["--skip-pytest", "--worst", "3"]) == 0
    assert cm_cli.main(["--mode", "climb"]) == 2


def test_size_measure_docstring_strip_and_nested() -> None:
    assert size_measure._strip_leading_docstring([]) == []
    tree = ast.parse("x = 1\n")
    assert size_measure._strip_leading_docstring(list(tree.body)) == list(tree.body)
    with_doc = ast.parse('def f():\n    """d"""\n    return 1\n')
    body = size_measure._strip_leading_docstring(list(with_doc.body[0].body))
    assert len(body) == 1
    assert size_measure.statement_count(with_doc.body[0]) == 1

    nested = ast.parse(
        "def outer():\n"
        "    def inner():\n"
        "        return 1\n"
        "    try:\n"
        "        x = 1\n"
        "    except Exception:\n"
        "        x = 0\n"
        "    else:\n"
        "        x = 2\n"
    )
    out: dict[str, int] = {}
    size_measure._visit_functions(nested, "", "n.py", out)
    assert "n.py::outer" in out
    assert "n.py::outer.inner" in out
    prior = out["n.py::outer"]
    size_measure._record_function(nested.body[0], "", "n.py", out)
    assert out["n.py::outer"] == max(prior, out["n.py::outer"])


def test_measure_tree_skips_syntax_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(size_measure, "REPO_ROOT", tmp_path)
    pkg = tmp_path / "src" / "doc_engine"
    pkg.mkdir(parents=True)
    (pkg / "__pycache__").mkdir()
    (pkg / "__pycache__" / "x.py").write_text("x=1\n", encoding="utf-8")
    (pkg / "ok.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (pkg / "bad.py").write_text("def (\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "t.py").write_text("y = 1\n", encoding="utf-8")
    files = size_measure.iter_package_py_files(("src/doc_engine", "tests", "missing"))
    assert all("__pycache__" not in p.parts for p in files)
    file_loc, functions = size_measure.measure_tree(("src/doc_engine", "tests"))
    assert any(k.endswith("ok.py") for k in file_loc)
    assert any("::f" in k for k in functions)
    assert not any(k.endswith("bad.py") and "::" in k for k in functions)
