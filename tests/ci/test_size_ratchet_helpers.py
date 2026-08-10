"""Coverage climb: size_ratchet pure helpers + main CLI edges (≤225 LOC)."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci import size_measure
from doc_engine.ci import size_ratchet as sr

pytestmark = pytest.mark.domain_ci_meta

def test_line_count_and_statement_count() -> None:
    assert size_measure.line_count("") == 0
    assert size_measure.line_count("a\nb") == 2
    assert size_measure.line_count("a\n") == 1
    tree = ast.parse(
        "def f(x):\n"
        "    if x:\n"
        "        return 1\n"
        "    return 0\n"
        "class C:\n"
        "    def m(self):\n"
        "        y = 1\n"
        "        return y\n"
    )
    fn = tree.body[0]
    assert isinstance(fn, ast.FunctionDef)
    assert size_measure.statement_count(fn) >= 2
    cls = tree.body[1]
    assert isinstance(cls, ast.ClassDef)
    out: dict[str, int] = {}
    size_measure._visit_functions(tree, "", "mod.py", out)
    assert "mod.py::f" in out
    assert "mod.py::C.m" in out

def test_hard_soft_and_compare_offenders() -> None:
    files = {"a.py": sr.FILE_LOC_HARD + 1, "b.py": sr.FILE_LOC_SOFT + 1, "c.py": 10}
    assert "a.py" in sr.hard_file_offenders(files)
    assert "b.py" not in sr.hard_file_offenders(files)
    fns = {
        "a.py::big": sr.FN_STMTS_HARD + 1,
        "a.py::at_ceiling": sr.FN_STMTS_HARD,
        "a.py::tiny": 1,
    }
    assert "a.py::big" in sr.hard_fn_offenders(fns)
    assert "a.py::at_ceiling" not in sr.hard_fn_offenders(fns)
    notes = sr.soft_advisories(files, fns)
    assert any("b.py" in n for n in notes)
    # FN_STMTS_SOFT == HARD: fn advisories fire only at exact ceiling.
    assert any("at_ceiling" in n for n in notes)
    assert not any("big" in n for n in notes)
    assert sr._offender_delta("file", "x.py", None, 9) is not None
    assert sr._offender_delta("file", "x.py", 3, 4) is not None
    assert sr._offender_delta("file", "x.py", 4, 4) is None
    issues = sr.compare_offenders("file", {"a.py": 10}, {"a.py": 11, "n.py": 12})
    assert any("grew" in i for i in issues)
    assert any("count rose" in i for i in issues)

def test_baseline_roundtrip_and_compare(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sr, "checked_path_under_repo", lambda p: Path(p))
    path = tmp_path / "base.json"
    payload = sr.build_baseline_payload({"big.py": 1001}, {"big.py::f": 51})
    assert payload["schema_version"] == sr.SCHEMA_VERSION
    sr.write_baseline(path, {"big.py": 1001}, {"big.py::f": 51})
    loaded = sr.load_baseline(path)
    assert loaded["files"]["big.py"] == 1001
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema_version": 999}), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        sr.load_baseline(bad)
    assert exc.value.code == 2
    issues = sr.compare(
        loaded,
        {"big.py": 1001, "ok.py": 10},
        {"big.py::f": 51},
    )
    assert issues == []
    grown = sr.compare(loaded, {"big.py": 1100}, {"big.py::f": 60})
    assert grown

def test_main_update_missing_and_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sr, "checked_path_under_repo", lambda p: Path(p))
    monkeypatch.setattr(sr, "measure_tree", lambda: ({"a.py": 10}, {"a.py::f": 1}))
    base = tmp_path / "size_baseline.json"
    assert sr.main(["--baseline", str(base), "--update"]) == 0
    assert base.is_file()
    assert "baseline written" in capsys.readouterr().out
    missing = tmp_path / "nope.json"
    assert sr.main(["--baseline", str(missing)]) == 2
    # Matching empty offenders → pass; dropped count prints note.
    base.write_text(
        json.dumps(
            {
                "schema_version": sr.SCHEMA_VERSION,
                "files": {"old.py": 2000},
                "functions": {},
                "file_offender_count": 1,
                "fn_offender_count": 0,
            }
        ),
        encoding="utf-8",
    )
    assert sr.main(["--baseline", str(base)]) == 0
    assert "dropped" in capsys.readouterr().out
    sr._print_soft_advisories([])
    sr._print_soft_advisories([f"n{i}" for i in range(45)])
    assert "more" in capsys.readouterr().out
    sr._print_issues(["boom"])
    assert "failed" in capsys.readouterr().err
