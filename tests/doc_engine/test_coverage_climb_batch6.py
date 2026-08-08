"""Coverage climb batch6: CodeQL cache edges, drift helpers, capacity pools."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from doc_engine.scanning.support import _codeql_runner as runner
from doc_engine.tools import capacity_preflight as cap
from doc_engine.tools import spring_drift_check as drift


# --- _codeql_runner ---------------------------------------------------------


def test_reject_unsafe_and_resolve_exe(tmp_path: Path) -> None:
    with pytest.raises(runner.CodeQLError, match="non-empty"):
        runner._reject_unsafe_option("")
    with pytest.raises(runner.CodeQLError, match="single-line"):
        runner._reject_unsafe_option("bad\nopt")
    missing = tmp_path / "nope"
    with pytest.raises(runner.CodeQLError, match="not a file"):
        runner._resolve_codeql_exe(missing)
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    assert runner._resolve_codeql_exe(fake) == fake.resolve()


def test_invoke_codeql_rejects_and_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    with pytest.raises(runner.CodeQLError, match="non-allowlisted"):
        runner._invoke_codeql(fake, ("database", "delete"), timeout=1)

    import subprocess

    def boom(*a, **k):
        raise subprocess.TimeoutExpired(cmd="codeql", timeout=1)

    monkeypatch.setattr(runner.subprocess, "run", boom)
    with pytest.raises(runner.CodeQLError, match="timed out"):
        runner._invoke_codeql(fake, ("--version",), timeout=1)


def test_find_codeql_env_and_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("DOC_ENGINE_CODEQL", raising=False)
    monkeypatch.setattr(runner.shutil, "which", lambda _n: None)
    with pytest.raises(runner.CodeQLNotFoundError):
        runner.find_codeql()
    bad = tmp_path / "missing-bin"
    monkeypatch.setenv("DOC_ENGINE_CODEQL", str(bad))
    with pytest.raises(runner.CodeQLNotFoundError, match="not an existing"):
        runner.find_codeql()
    good = tmp_path / "cq"
    good.write_text("", encoding="utf-8")
    monkeypatch.setenv("DOC_ENGINE_CODEQL", str(good))
    assert runner.find_codeql() == good


def test_cache_metadata_and_results_roundtrip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "a.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    db = tmp_path / "db"
    db.mkdir()
    runner._write_cache_metadata(db, repo, pack, "./gradlew compileJava", codeql_cli_version="2.0")
    assert runner._cache_is_valid(
        db, repo, pack, "./gradlew compileJava", codeql_cli_version="2.0"
    )
    assert not runner._cache_is_valid(
        db, repo, pack, "./gradlew compileJava", codeql_cli_version="9.9"
    )
    assert runner._cache_metadata(tmp_path / "missing-db") is None
    rows = [{"file": "A.java", "line": 1}]
    runner._save_results_cache(
        repo, pack, "./gradlew compileJava", "sv1", rows, codeql_cli_version="2.0"
    )
    loaded = runner._load_results_cache(
        repo, pack, "./gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    assert loaded == rows
    with pytest.raises(runner.CodeQLError, match="not a list"):
        runner._validate_cached_evidence_rows({"file": "x"})
    with pytest.raises(runner.CodeQLError, match="missing file"):
        runner._validate_cached_evidence_rows([{"line": 1}])


def test_prepare_scan_and_cleanup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("//", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    resolved, db, using, keep = runner._prepare_scan_targets(
        repo, "./gradlew compileJava", pack, None, False, None, "2.0"
    )
    assert resolved == pack
    assert using is True
    assert keep is True
    assert db.parent.is_dir()
    with pytest.raises(runner.CodeQLError, match="query pack not found"):
        runner._prepare_scan_targets(
            repo, "./gradlew compileJava", tmp_path / "no-pack", None, False, None, "2.0"
        )
    db2 = tmp_path / "explicit-db"
    db2.mkdir()
    tmp = tmp_path / "tmp"
    tmp.mkdir()
    runner._cleanup_scan_temps(db2, str(tmp), keep_database=False)
    assert not db2.exists()
    assert not tmp.exists()
    assert runner._load_cached_scan_rows(
        using_cache=False,
        scanner_version="sv",
        repo_path=repo,
        pack_dir=pack,
        build_command="./gradlew compileJava",
        scan_context=None,
        cli_version="2.0",
    ) is None
    assert runner._is_codeql_hash_file("build.gradle")
    assert runner._is_codeql_walk_filename("Foo.java")
    dirs = [".git", "src", "build"]
    runner._prune_hash_walk_dirs(dirs)
    assert dirs == ["src"]


def test_ensure_regular_file_and_codeql_version(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = tmp_path / "dir"
    d.mkdir()
    with pytest.raises(runner.CodeQLError, match="non-regular"):
        runner._ensure_regular_file(d)
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: SimpleNamespace(
            returncode=0, stdout="CodeQL command-line toolchain release 2.20.0.\n"
        ),
    )
    assert runner.codeql_version(fake) == "2.20.0"
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: SimpleNamespace(returncode=1, stderr="boom", stdout=""),
    )
    with pytest.raises(runner.CodeQLError, match="--version failed"):
        runner.codeql_version(fake)


# --- spring_drift_check -----------------------------------------------------


def test_classify_and_citations_helpers() -> None:
    clf = drift.classify_files(
        {"a.java": "1", "b.java": "2", "c.java": "3"},
        {"a.java": "1", "b.java": "9", "d.java": "4"},
    )
    assert clf["unchanged"] == ["a.java"]
    assert clf["changed"] == ["b.java"]
    assert clf["deleted"] == ["c.java"]
    assert clf["added"] == ["d.java"]

    signals = {
        "evidence": {
            "persistence": [
                {"file": "a.java", "line": 1, "rule_id": "r1"},
            ]
        },
        "entity_table_map": {
            "Foo": {"file": "Foo.java", "line": 2, "table": "FOO"},
        },
        "file_signatures": {"a.java": "1"},
        "repo_path": "/r",
    }
    cites = list(drift.all_citations(signals))
    assert any(s.startswith("evidence.") for s, _ in cites)
    assert any(s.startswith("entity_table_map.") for s, _ in cites)
    by_file = drift._group_citations_by_file(signals)
    assert "a.java" in by_file
    indexed = drift._index_fresh_evidence_by_file(signals)
    assert "a.java" in indexed
    sigs, prov = drift._baseline_signatures_and_provenance(signals, None)
    assert prov["source"] == "spring_signals.json"
    assert sigs == {"a.java": "1"}
    man = {
        "file_signatures": {"x": "y"},
        "run_id": "rid",
        "target_repo": {"path": "/t", "commit_hash": "c", "dirty": False},
    }
    _, prov2 = drift._baseline_signatures_and_provenance(signals, man)
    assert prov2["source"] == "run_manifest.json"
    assert prov2["run_id"] == "rid"
    results = []
    drift._append_uniform_status(
        results, [("evidence.persistence", {"file": "a.java", "line": 1})], "unchanged"
    )
    assert results[0]["status"] == "unchanged"
    report = drift._assemble_drift_report(
        "/repo", signals, prov, clf, list(results)
    )
    assert report["citations_checked"] == 1
    assert report["schema_version"]


def test_load_signals_rejects_old_schema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "signals.json"
    path.write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        drift.load_signals(str(path))
    assert exc.value.code == 1


def test_empty_signatures_and_manifest_validate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    data = {"target_repo": {"path": str(empty)}, "file_signatures": {}}
    monkeypatch.setattr(drift.spring_signal_scan, "dfs_walk", lambda _p: [])
    assert drift._empty_signatures_are_legitimate(data) is True
    assert drift._empty_signatures_are_legitimate({"target_repo": {}}) is False

    with pytest.raises(SystemExit):
        drift._validate_manifest_baseline(str(tmp_path / "m.json"), {"status": "ok"})
    with pytest.raises(SystemExit):
        drift._validate_manifest_baseline(
            str(tmp_path / "m.json"),
            {"file_signatures": {}, "status": "running", "target_repo": {"path": str(empty)}},
        )
    # Empty signatures + empty repo is accepted.
    drift._validate_manifest_baseline(
        str(tmp_path / "m.json"),
        {"file_signatures": {}, "status": "complete", "target_repo": {"path": str(empty)}},
    )
    assert "empty-repo baseline" in capsys.readouterr().err

    ctx = SimpleNamespace(file_signatures={"A.java": "sig"})
    assert drift.tier1_scan("/unused", scan_context=ctx) == {"A.java": "sig"}


# --- capacity_preflight -----------------------------------------------------


def test_stage4_pool_helpers_and_compare() -> None:
    edges = {"groups": {"g1": {"a": 1}, "g2": {"b": list(range(50))}}}
    dist = cap.estimate_stage1_slice_tokens(edges)
    assert dist["max"] >= dist["mean"]
    assert dist["total"] >= dist["max"]
    assert cap._json_est_tokens(None) == 0
    assert cap._json_est_tokens({"k": "v"}) >= 1

    proxy = cap.estimate_stage4_shared_pool_tokens(
        {"groups": [{"est_tokens": 10}, {"est_tokens": 5}]},
        signals_data={"n": 1},
    )
    assert proxy["metric_kind"] == "partial_proxy_pre_stage4"
    assert proxy["summaries_est_tokens"] == 15
    assert proxy["signals_omitted"] is False

    measured = cap.measure_stage4_shared_pool_tokens(
        {"summaries": [1]},
        interview_answers={"q": "a"},
        signals_data=None,
    )
    assert measured["metric_kind"] == "measured_stage4_inputs"
    assert measured["interview_answers_omitted"] is False
    assert measured["signals_omitted"] is True
    with pytest.raises(ValueError):
        cap.measure_stage4_shared_pool_tokens(None)

    cmp = cap.compare_stage4_proxy_to_measured(proxy, measured)
    assert cmp["measured_over_proxy_ratio"] is not None
    fields = cap._stage4_pool_fields(measured)
    assert fields["stage4_metric_kind"] == "measured_stage4_inputs"
    warn = cap._stage4_shared_pool_warning(measured, threshold=0)
    assert warn is not None
    assert cap._stage4_shared_pool_warning(measured, threshold=10**9) is None
    fan = cap._stage_fanout_for_groups(3)
    assert fan["stage1_file_summarizer"] == 3
    assert fan["stage4_doc_writer"] == cap.STAGE4_FIXED_FANOUT
    included, omitted = cap._measured_included_omitted(True, True)
    assert "summaries" in included
    assert "interview_answers" in omitted
