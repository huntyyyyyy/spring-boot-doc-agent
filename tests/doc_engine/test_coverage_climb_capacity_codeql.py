"""Coverage climb: capacity_preflight CLI helpers + CodeQL runner edges."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.scanning.support import _codeql_runner as runner
from doc_engine.tools import capacity_preflight as cap


def test_maybe_write_report_and_warnings(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = {
        "warnings": [{"dimension": "d", "message": "m"}],
        "stage4_shared_pool_upper_bound_est_tokens": 10,
        "stage4_summaries_est_tokens": 1,
        "stage4_interview_answers_est_tokens": 2,
        "stage4_interview_answers_omitted": False,
        "stage4_signals_est_tokens": 3,
        "stage4_signals_omitted": True,
        "stage4_omitted_not_estimated": ["x"],
        "stage4_proxy_comparison": {"measured_over_proxy_ratio": 1.25},
    }
    out = tmp_path / "out.json"
    cap._maybe_write_report(str(out), report)
    assert out.is_file()
    cap._print_warnings(report)
    assert "warning" in capsys.readouterr().out.lower()
    report["warnings"] = []
    cap._print_warnings(report)
    assert "No thresholds" in capsys.readouterr().out
    cap._print_l2b_summary(report)
    assert "capacity-preflight" in capsys.readouterr().out


def test_load_optional_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert cap._load_optional_json(None) is None
    path = tmp_path / "a.json"
    path.write_text('{"k":1}', encoding="utf-8")
    monkeypatch.setattr(cap, "checked_path", lambda p, want=None: Path(p))
    assert cap._load_optional_json(str(path)) == {"k": 1}


def test_print_stage0_summary(capsys: pytest.CaptureFixture[str]) -> None:
    report = {
        "num_groups": 2,
        "total_fanout": 4,
        "stage1_slice_est_tokens_max": 100,
        "stage1_slice_est_tokens_total": 200,
        "edge_join_stats": {"reduction_factor": 3},
        "stage4_shared_pool_upper_bound_est_tokens": 50,
        "stage4_omitted_not_estimated": ["summaries"],
        "stage4_signals_omitted": True,
        "warnings": [],
    }
    cap._print_stage0_summary(report)
    out = capsys.readouterr().out
    assert "2 groups" in out
    assert "3x" in out


def test_main_bad_repo(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    from doc_engine.paths import PathValidationError

    monkeypatch.setattr(
        "sys.argv",
        ["capacity_preflight", "/no/such/repo"],
    )
    monkeypatch.setattr(
        cap,
        "checked_path",
        lambda *a, **k: (_ for _ in ()).throw(PathValidationError("bad")),
    )
    with pytest.raises(SystemExit) as exc:
        cap.main()
    assert exc.value.code == 1
    assert "error" in capsys.readouterr().err.lower()


def test_main_l2b_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    summaries = tmp_path / "summaries.json"
    summaries.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "capacity_preflight",
            str(repo),
            "--summaries-file",
            str(summaries),
        ],
    )
    monkeypatch.setattr(cap, "checked_path", lambda p, want=None: Path(p))
    monkeypatch.setattr(
        cap,
        "_run_l2b_calibration",
        lambda args, repo_path: None,
    )
    cap.main()


def test_hash_from_scan_context_and_refuse_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx = SimpleNamespace(
        java_files=[SimpleNamespace(rel_path="A.java")],
        file_signatures={"A.java": "sig", "pom.xml": "p"},
    )
    digest = runner._hash_from_scan_context(ctx)
    assert len(digest) == 32

    link = tmp_path / "link"
    if hasattr(os := __import__("os"), "symlink"):
        try:
            os.symlink(tmp_path, link, target_is_directory=True)
        except OSError:
            pytest.skip("symlink unavailable")
        with pytest.raises(runner.CodeQLError, match="symlink"):
            runner._refuse_symlink_cache_path(link)


def test_validate_one_cached_row_and_non_dict() -> None:
    with pytest.raises(runner.CodeQLError):
        runner._validate_one_cached_row(0, "x")
    assert runner._validate_one_cached_row(0, {"file": "a.java"})["file"] == "a.java"


def test_scan_with_codeql_full_path_mocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    monkeypatch.setattr(runner, "find_codeql", lambda: fake)
    monkeypatch.setattr(runner, "codeql_version", lambda _p: "2.0")
    monkeypatch.setattr(runner, "_load_cached_scan_rows", lambda **k: None)
    monkeypatch.setattr(runner, "install_pack", lambda *a, **k: None)
    monkeypatch.setattr(runner, "_ensure_codeql_database", lambda **k: None)
    monkeypatch.setattr(
        runner,
        "_run_queries_and_maybe_cache",
        lambda **k: [{"file": "A.java"}],
    )
    rows = runner.scan_with_codeql(
        repo,
        "gradlew compileJava",
        pack_dir=pack,
        scanner_version="sv",
    )
    assert rows == [{"file": "A.java"}]
