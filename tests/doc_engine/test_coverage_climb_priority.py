"""Focused coverage climb for worst below-floor modules (wave1).

Targets (from ``coverage_gap_average.py``): query/protocols, scanning/spring,
core/timeouts, scanning/_scanner_codeql, pipeline/local_runner_phases/support,
query/kinds, core/excludes — plus CodeQL runner edge paths not yet exercised.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping
from unittest.mock import MagicMock

import pytest

from doc_engine.core import excludes as excludes_mod
from doc_engine.core import timeouts as timeouts_mod
from doc_engine.pipeline.local_runner_phases import support as phase_support
from doc_engine.query import kinds as kinds_mod
from doc_engine.query.protocols import FreshnessPolicy, PacketProvider
from doc_engine.scanning import spring as spring_mod
from doc_engine.scanning._scanner_codeql import CodeQLBackend
from doc_engine.scanning.support import _codeql_runner as runner


# --- query/protocols.py -----------------------------------------------------


class _StubPacket:
    name = "stub"

    def provide(
        self,
        request: str,
        *,
        signals: Mapping[str, Any],
        facts_rows: list[Mapping[str, Any]],
        run_dir: Path,
        limit: int,
    ) -> list[dict[str, Any]]:
        return [{"path": "a.java", "reason": request, "limit": limit}]


class _StubFreshness:
    def freshness_for(self, rel_path: str | None) -> str:
        return "unknown" if not rel_path else "live"


def test_packet_provider_protocol_runtime_checkable(tmp_path: Path) -> None:
    stub = _StubPacket()
    assert isinstance(stub, PacketProvider)
    items = stub.provide(
        "need",
        signals={},
        facts_rows=[],
        run_dir=tmp_path,
        limit=3,
    )
    assert items[0]["reason"] == "need"


def test_freshness_policy_protocol_runtime_checkable() -> None:
    stub = _StubFreshness()
    assert isinstance(stub, FreshnessPolicy)
    assert stub.freshness_for(None) == "unknown"
    assert stub.freshness_for("a.java") == "live"


# --- core/timeouts.py + core/excludes.py ------------------------------------


def test_env_seconds_rejects_non_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "not-an-int")
    with pytest.raises(ValueError, match="integer"):
        timeouts_mod.tool_timeout_seconds()


def test_env_seconds_rejects_non_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_CODEQL_TIMEOUT", "0")
    with pytest.raises(ValueError, match="positive"):
        timeouts_mod.codeql_database_timeout_seconds()


def test_env_seconds_blank_uses_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_TOOL_TIMEOUT", "   ")
    assert timeouts_mod.tool_timeout_seconds() == 600


def test_load_gitignore_returns_none_without_file(tmp_path: Path) -> None:
    assert excludes_mod.load_gitignore_spec(str(tmp_path)) is None


def test_load_gitignore_returns_none_when_pathspec_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / ".gitignore").write_text("*.class\n", encoding="utf-8")
    real_import = __import__

    def _fake_import(name, *args, **kwargs):
        if name == "pathspec":
            raise ImportError("no pathspec")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", _fake_import)
    assert excludes_mod.load_gitignore_spec(str(tmp_path)) is None


# --- query/kinds.py ---------------------------------------------------------


def test_mcp_input_properties_signal_fact_edge_filters() -> None:
    full = kinds_mod.QueryKindSpec(
        kind="dependents",
        handler=lambda **_: [],
        requires_signals=True,
        requires_facts=True,
        accepts_edges=True,
        filter_keys=("file", "type"),
    ).mcp_input_properties()
    assert set(full) >= {"signals", "facts", "edges", "file", "type", "limit"}
    assert full["limit"] == {"type": "integer"}

    lean = kinds_mod.QueryKindSpec(
        kind="facts",
        handler=lambda **_: [],
        requires_signals=False,
        requires_facts=True,
    ).mcp_input_properties()
    assert "signals" not in lean
    assert "facts" in lean
    assert "edges" not in lean


# --- scanning/spring.py -----------------------------------------------------


def test_detect_build_command_prefers_gradlew(tmp_path: Path) -> None:
    (tmp_path / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "gradlew" in cmd
    assert "compileJava" in cmd


def test_detect_build_command_maven_wrapper(tmp_path: Path) -> None:
    (tmp_path / "mvnw").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "mvnw" in cmd


def test_detect_build_command_gradle_on_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "build.gradle").write_text("plugins {}\n", encoding="utf-8")
    monkeypatch.setattr(spring_mod.shutil, "which", lambda name: f"/bin/{name}" if name == "gradle" else None)
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "gradle" in cmd


def test_detect_build_command_maven_on_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "pom.xml").write_text("<project/>\n", encoding="utf-8")
    monkeypatch.setattr(spring_mod.shutil, "which", lambda name: f"/bin/{name}" if name == "mvn" else None)
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "mvn" in cmd


def test_detect_build_command_returns_none_without_markers(tmp_path: Path) -> None:
    assert spring_mod.detect_build_command(str(tmp_path)) is None


def test_prepare_codeql_build_skips_when_codeql_absent(tmp_path: Path) -> None:
    assert (
        spring_mod._prepare_codeql_build_command(["filesystem"], str(tmp_path), "gradlew build")
        == "gradlew build"
    )


def test_prepare_codeql_build_detects_or_raises(tmp_path: Path) -> None:
    with pytest.raises(spring_mod.CodeQLScannerError, match="Could not detect"):
        spring_mod._prepare_codeql_build_command(["codeql"], str(tmp_path), None)
    (tmp_path / "gradlew").write_text("x", encoding="utf-8")
    cmd = spring_mod._prepare_codeql_build_command(["codeql"], str(tmp_path), None)
    assert "gradlew" in cmd


def test_prepare_codeql_build_wraps_validation_error(tmp_path: Path) -> None:
    with pytest.raises(spring_mod.CodeQLScannerError):
        spring_mod._prepare_codeql_build_command(
            ["codeql"], str(tmp_path), "bash -c 'evil'"
        )


def test_reraise_scan_error_mapping() -> None:
    from doc_engine.scanning._orchestrator import CoveringProofError
    from doc_engine.scanning.support._codeql_runner import CodeQLError, CodeQLNotFoundError

    def _from_except(exc: BaseException) -> None:
        try:
            raise exc
        except BaseException as caught:
            spring_mod._reraise_scan_error(caught)

    with pytest.raises(CoveringProofError):
        _from_except(CoveringProofError("proof"))
    with pytest.raises(CodeQLNotFoundError):
        _from_except(CodeQLNotFoundError("missing"))
    with pytest.raises(spring_mod.CodeQLScannerError):
        _from_except(CodeQLError("boom"))
    with pytest.raises(spring_mod.CodeQLScannerError):
        _from_except(PermissionError("denied"))
    with pytest.raises(RuntimeError, match="passthrough"):
        _from_except(RuntimeError("passthrough"))


def test_spring_scan_kwargs_include_context_when_set() -> None:
    ctx = object()
    kwargs = spring_mod._spring_scan_kwargs(
        sql_dialect="ansi",
        respect_gitignore=True,
        build_command="gradlew",
        db_path=None,
        scan_context=ctx,
    )
    assert kwargs["scan_context"] is ctx
    assert kwargs["respect_gitignore"] is True


def test_combined_hash_and_scanner_version_stable() -> None:
    scanners = [
        SimpleNamespace(name="a", version_hash=lambda: "1111"),
        SimpleNamespace(name="b", version_hash=lambda: "2222"),
    ]
    digest = spring_mod._combined_hash(scanners)
    assert len(digest) == 16
    assert digest == spring_mod._combined_hash(scanners)


def test_run_spring_scan_wraps_codeql_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from doc_engine.scanning.support._codeql_runner import CodeQLError

    monkeypatch.setattr(
        spring_mod,
        "run_scan",
        lambda *a, **k: (_ for _ in ()).throw(CodeQLError("fail")),
    )
    with pytest.raises(spring_mod.CodeQLScannerError, match="fail"):
        spring_mod._run_spring_scan(
            "/tmp/repo",
            [],
            sql_dialect="ansi",
            respect_gitignore=False,
            build_command=None,
            db_path=None,
            scan_context=None,
        )


# --- scanning/_scanner_codeql.py --------------------------------------------


def test_codeql_backend_name_and_version_hash(tmp_path: Path, monkeypatch) -> None:
    backend = CodeQLBackend()
    assert backend.name == "codeql"
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// query\n", encoding="utf-8")
    monkeypatch.setattr(
        "doc_engine.scanning._scanner_codeql.codeql_pack_dir",
        lambda: pack,
    )
    digest = backend.version_hash()
    assert len(digest) == 16
    # Unreadable path should be skipped without failing the hash.
    monkeypatch.setattr(
        CodeQLBackend,
        "_version_hash_paths",
        staticmethod(lambda: [str(tmp_path / "missing.bin")]),
    )
    assert len(backend.version_hash()) == 16


def test_codeql_scan_requires_build_command() -> None:
    with pytest.raises(runner.CodeQLError, match="build command"):
        CodeQLBackend().scan("/tmp/repo")


def test_codeql_scan_buckets_rows(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    java = repo / "A.java"
    java.write_text("@Entity class A {}\n", encoding="utf-8")
    backend = CodeQLBackend()
    monkeypatch.setattr(backend, "version_hash", lambda: "abcd1234efgh5678")
    monkeypatch.setattr(
        "doc_engine.scanning._scanner_codeql.scan_with_codeql",
        lambda *a, **k: [
            {
                "file": str(java),
                "line": 1,
                "rule_id": "persistence__entity",
                "class_name": "A",
                "table_name": "a",
            },
            {
                "file": str(java),
                "line": 1,
                "rule_id": "api_surface__controller",
            },
        ],
    )
    monkeypatch.setattr(
        backend,
        "_covering_receipt_for_scan",
        lambda _ctx: {"status": "complete"},
    )
    result = backend.scan(str(repo), build_command="gradlew compileJava")
    assert "persistence" in result["evidence"]
    assert "api_surface" in result["evidence"]
    assert result["entity_table_map_candidates"]


def test_ingest_skips_rows_outside_java_scope(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    backend = CodeQLBackend()
    evidence: dict = {}
    entities: dict = {}
    ctx_rels = {"B.java"}
    backend._ingest_codeql_row(
        repo_path=str(repo),
        row={"file": "A.java", "line": 1, "rule_id": "api_surface__x"},
        java_rels=ctx_rels,
        evidence=evidence,
        entity_candidates=entities,
    )
    assert evidence == {}


def test_ingest_entity_row_without_extractable_class(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    rel = "Empty.java"
    (repo / rel).write_text("// empty\n", encoding="utf-8")
    monkeypatch.setattr(
        "doc_engine.scanning._scanner_codeql.extract_entity",
        lambda *a, **k: None,
    )
    backend = CodeQLBackend()
    evidence: dict = {}
    entities: dict = {}
    backend._ingest_entity_row(
        repo_path=str(repo),
        rel=rel,
        row={"line": 1, "class_name": ""},
        match_text="// empty",
        rule_id="persistence__entity",
        entity_candidates=entities,
        evidence=evidence,
    )
    assert entities == {}
    assert evidence == {}


def test_explicit_table_preserves_package() -> None:
    entry = CodeQLBackend._explicit_table_map_entry(
        rel="p/A.java",
        class_name="A",
        codeql_table="tbl",
        map_entry={"package": "com.ex", "fqcn": "com.ex.A"},
    )
    assert entry["package"] == "com.ex"
    assert entry["fqcn"] == "com.ex.A"
    assert entry["table"] == "tbl"


# --- codeql runner edge paths -----------------------------------------------


def test_find_codeql_rejects_missing_env_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DOC_ENGINE_CODEQL", str(Path("/no/such/codeql-binary")))
    with pytest.raises(runner.CodeQLNotFoundError, match="not an existing file"):
        runner.find_codeql()


def test_resolve_codeql_exe_rejects_directory(tmp_path: Path) -> None:
    d = tmp_path / "not-a-file"
    d.mkdir()
    with pytest.raises(runner.CodeQLError, match="not a file"):
        runner._resolve_codeql_exe(d)


def test_reject_unsafe_option_empty() -> None:
    with pytest.raises(runner.CodeQLError, match="non-empty"):
        runner._reject_unsafe_option("")


def test_invoke_codeql_timeout_wraps(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")

    def _raise(*_a, **_k):
        raise subprocess.TimeoutExpired(cmd="codeql", timeout=1)

    monkeypatch.setattr(runner.subprocess, "run", _raise)
    with pytest.raises(runner.CodeQLError, match="timed out"):
        runner._invoke_codeql(fake, ("--version",), timeout=1)


def test_codeql_version_nonzero_and_success(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=1, stdout="", stderr="boom"),
    )
    with pytest.raises(runner.CodeQLError, match="--version failed"):
        runner.codeql_version(fake)
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(
            returncode=0,
            stdout="CodeQL command-line toolchain release 2.20.0.\n",
            stderr="",
        ),
    )
    assert runner.codeql_version(fake) == "2.20.0"


def test_version_token_no_digit_after_release() -> None:
    assert runner._version_token_from_line("release only words") is None


def test_cache_base_dir_xdg_and_fallback(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    assert runner._cache_base_dir() == tmp_path / "xdg"
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(runner.sys, "platform", "linux")
    monkeypatch.setattr(runner.Path, "home", classmethod(lambda cls: tmp_path / "home"))
    assert runner._cache_base_dir() == tmp_path / "home" / ".cache"


def test_hash_one_walk_file_skips_outside_and_oserror(
    tmp_path: Path, monkeypatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    inside = repo / "A.java"
    inside.write_text("class A {}", encoding="utf-8")
    h = MagicMock()
    runner._hash_one_walk_file(
        h, repo, str(repo.resolve()), inside, lambda *_: False
    )
    h.update.assert_not_called()

    def _boom(_self=None):
        raise OSError("io")

    monkeypatch.setattr(Path, "read_bytes", _boom)
    runner._hash_one_walk_file(
        h, repo, str(repo.resolve()), inside, lambda *_: True
    )


def test_cache_metadata_and_validity(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    db = tmp_path / "db"
    db.mkdir()
    assert runner._cache_metadata(db) is None
    runner._write_cache_metadata(db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert runner._cache_is_valid(db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert not runner._cache_is_valid(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.1"
    )
    bad = db / "spring_signal_scan_cache.json"
    bad.write_text("{not-json", encoding="utf-8")
    assert runner._cache_metadata(db) is None


def test_results_cache_roundtrip_and_corrupt(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    rows = [{"file": "A.java", "line": 1}]
    runner._save_results_cache(
        repo, pack, "gradlew compileJava", "sv1", rows, codeql_cli_version="2.0"
    )
    loaded = runner._load_results_cache(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    assert loaded == rows
    path = runner._results_cache_path(
        repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
    )
    path.write_text("[]not-json", encoding="utf-8")
    assert (
        runner._load_results_cache(
            repo, pack, "gradlew compileJava", "sv1", codeql_cli_version="2.0"
        )
        is None
    )


def test_create_database_and_install_pack_failures(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=2, stdout="out", stderr="err"),
    )
    with pytest.raises(runner.CodeQLError, match="database create failed"):
        runner.create_database(
            fake, tmp_path / "repo", tmp_path / "db", "gradlew compileJava"
        )
    with pytest.raises(runner.CodeQLError, match="pack install failed"):
        runner.install_pack(fake, tmp_path / "pack")


def test_run_query_and_decode_failures(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=3, stdout="", stderr="bad"),
    )
    with pytest.raises(runner.CodeQLError, match="query run failed"):
        runner.run_query(fake, tmp_path / "db", tmp_path / "q.ql", tmp_path / "out.bqrs")
    with pytest.raises(runner.CodeQLError, match="bqrs decode failed"):
        runner.decode_bqrs(fake, tmp_path / "out.bqrs")


def test_decode_bqrs_success(tmp_path: Path, monkeypatch) -> None:
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    payload = {
        "#select": {
            "columns": [{"name": "file"}, {"kind": "String"}],
            "tuples": [["a.java", "x"]],
        }
    }
    monkeypatch.setattr(
        runner,
        "_invoke_codeql",
        lambda *a, **k: MagicMock(returncode=0, stdout=json.dumps(payload), stderr=""),
    )
    rows = runner.decode_bqrs(fake, tmp_path / "out.bqrs")
    assert rows == [{"file": "a.java", "col_1": "x"}]


def test_run_all_queries_empty_and_merge(tmp_path: Path, monkeypatch) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    with pytest.raises(runner.CodeQLError, match="no .ql queries"):
        runner.run_all_queries(tmp_path / "codeql", tmp_path / "db", pack, tmp_path)
    (pack / "one.ql").write_text("// q", encoding="utf-8")
    monkeypatch.setattr(runner, "run_query", lambda *a, **k: None)
    monkeypatch.setattr(
        runner, "decode_bqrs", lambda *a, **k: [{"file": "a.java"}]
    )
    rows = runner.run_all_queries(tmp_path / "codeql", tmp_path / "db", pack, tmp_path)
    assert rows[0]["_query_file"] == "one.ql"


def test_prepare_scan_targets_and_reuse(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    resolved, db, using_cache, keep = runner._prepare_scan_targets(
        repo, "gradlew compileJava", pack, None, False, None, "2.0"
    )
    assert using_cache is True
    assert keep is True
    assert resolved == pack
    assert db.parent.name == "codeql-cache"

    with pytest.raises(runner.CodeQLError, match="query pack not found"):
        runner._prepare_scan_targets(
            repo, "gradlew compileJava", tmp_path / "missing", None, False, None, "2.0"
        )

    created = []

    def _create(*a, **k):
        created.append(True)
        db.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(runner, "create_database", _create)
    monkeypatch.setattr(runner, "_cache_is_valid", lambda *a, **k: False)
    runner._reuse_or_rebuild_cached_db(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        scan_context=None,
        cli_version="2.0",
    )
    assert created
    # Caller-provided keep path trusts existing DB.
    created.clear()
    runner._reuse_or_rebuild_cached_db(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=False,
        scan_context=None,
        cli_version="2.0",
    )
    assert not created


def test_ensure_database_create_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    calls = []
    monkeypatch.setattr(
        runner, "create_database", lambda *a, **k: calls.append("create")
    )
    monkeypatch.setattr(
        runner, "_write_cache_metadata", lambda *a, **k: calls.append("meta")
    )
    db = tmp_path / "fresh-db"
    runner._ensure_codeql_database(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=db,
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        keep_database=True,
        scan_context=None,
        cli_version="2.0",
    )
    assert calls == ["create", "meta"]


def test_run_queries_and_cleanup(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    monkeypatch.setattr(runner, "run_all_queries", lambda *a, **k: [{"file": "A.java"}])
    saved = []
    monkeypatch.setattr(
        runner, "_save_results_cache", lambda *a, **k: saved.append(True)
    )
    rows = runner._run_queries_and_maybe_cache(
        codeql_path=tmp_path / "codeql",
        repo_path=repo,
        db_path=tmp_path / "db",
        pack_dir=pack,
        build_command="gradlew compileJava",
        using_cache=True,
        scanner_version="sv",
        scan_context=None,
        cli_version="2.0",
        tmp=tmp_path,
    )
    assert rows and saved
    db = tmp_path / "dbdir"
    db.mkdir()
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    runner._cleanup_scan_temps(db, str(tmp), keep_database=False)
    assert not db.exists()
    assert not tmp.exists()


def test_scan_with_codeql_uses_results_cache(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    fake = tmp_path / "codeql"
    fake.write_text("", encoding="utf-8")
    monkeypatch.setattr(runner, "find_codeql", lambda: fake)
    monkeypatch.setattr(runner, "codeql_version", lambda _p: "2.0")
    monkeypatch.setattr(
        runner,
        "_load_cached_scan_rows",
        lambda **k: [{"file": "A.java", "cached": True}],
    )
    rows = runner.scan_with_codeql(
        repo,
        "gradlew compileJava",
        pack_dir=pack,
        scanner_version="sv",
    )
    assert rows[0]["cached"] is True


# --- local_runner_phases/support.py -----------------------------------------


def test_gate_and_subprocess_status_helpers() -> None:
    assert phase_support._gate_status_from_runner_status("OK") == "ok"
    assert phase_support._gate_status_from_runner_status("SKIPPED") == "skipped"
    assert phase_support._gate_status_from_runner_status("FAIL") == "fail"
    assert phase_support._classify_subprocess_status(0, gate=True) == "OK"
    assert phase_support._classify_subprocess_status(1, gate=True) == "FAIL"
    assert phase_support._classify_subprocess_status(1, gate=False) == "NONZERO"


def test_reconfigure_stdio_handles_missing_and_errors(monkeypatch) -> None:
    class _NoReconfigure:
        pass

    class _Boom:
        def reconfigure(self, **_kwargs):
            raise OSError("nope")

    monkeypatch.setattr(sys, "stdout", _NoReconfigure())
    monkeypatch.setattr(sys, "stderr", _Boom())
    phase_support._reconfigure_stdio_utf8()


def test_runner_record_gate_and_abort(tmp_path: Path) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=False)
        runner_obj._record_gate("g1", "label", "OK", "detail")
        assert runner_obj.gate_records[0].status == "ok"
        runner_obj._mark_critical_abort("stage0")
        assert runner_obj.aborted is True
        runner_obj.aborted = False
        runner_obj._abort_on_critical_spawn_failure(critical=True)
        assert runner_obj.aborted is True
    finally:
        log.close()


def test_runner_spawn_error_and_timeout(tmp_path: Path, monkeypatch) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=False)
        runner_obj._handle_spawn_exception(
            "step",
            started=0.0,
            timeout=1.0,
            exc=subprocess.TimeoutExpired(cmd="x", timeout=1),
            gate=True,
            gate_id="g1",
            critical=True,
        )
        assert runner_obj.results[-1][1] == "ERROR"
        assert runner_obj.aborted is True

        runner_obj.aborted = False
        monkeypatch.setattr(
            runner_obj,
            "_spawn_step_process",
            lambda *a, **k: MagicMock(returncode=1, stdout="o", stderr="e"),
        )
        proc = runner_obj.run("fail-crit", ["false"], gate=True, gate_id="g2", critical=True)
        assert proc is not None
        assert runner_obj.aborted is True

        runner_obj.aborted = True
        assert runner_obj.run("skipped", ["true"]) is None
        assert runner_obj.results[-1][1] == "SKIPPED"
    finally:
        log.close()


def test_runner_mock_success_and_error(tmp_path: Path) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=False)
        assert runner_obj.mock("m1", lambda: "ok-detail") == "ok-detail"
        assert runner_obj.results[-1][1] == "MOCK"
        assert runner_obj.mock("m2", lambda: (_ for _ in ()).throw(ValueError("x"))) is None
        assert runner_obj.aborted is True
        assert runner_obj.mock("m3", lambda: "never") is None
    finally:
        log.close()


def test_spawn_step_process_file_not_found(tmp_path: Path, monkeypatch) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=True)

        def _raise(*_a, **_k):
            raise FileNotFoundError("missing")

        monkeypatch.setattr(phase_support.subprocess, "run", _raise)
        monkeypatch.setattr(phase_support, "tool_timeout_seconds", lambda: 5)
        assert (
            runner_obj._spawn_step_process(
                "x",
                ["nope"],
                cwd=None,
                env=None,
                started=0.0,
                gate=False,
                gate_id=None,
                critical=False,
            )
            is None
        )
        assert runner_obj.results[-1][1] == "ERROR"
    finally:
        log.close()


def test_record_pipeline_stage_results() -> None:
    runner_obj = SimpleNamespace(results=[], aborted=False)

    def _record(label, status, seconds, detail=""):
        runner_obj.results.append((label, status, seconds, detail))

    runner_obj.record = _record
    ok = SimpleNamespace(success=True, detail="d", error=None)
    bad = SimpleNamespace(success=False, detail="", error="e")
    phase_support._record_pipeline_stage_results(
        runner_obj, [("s1", ok), ("s2", bad)], ok_status="OK"
    )
    assert runner_obj.results[0][1] == "OK"
    assert runner_obj.results[1][1] == "FAIL"
    assert runner_obj.aborted is True


def test_certification_helpers(tmp_path: Path, monkeypatch) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=True)
        runner_obj.record("pipeline:a", "FAIL", 0.1, "x")
        runner_obj._record_gate("g1", "gate", "FAIL", "bad")
        report = SimpleNamespace(
            certified=False,
            stages=[SimpleNamespace(name="a", status="fail")],
        )
        assert "stages:" in phase_support._certification_failure_summary(runner_obj, report)
        phase_support._emit_certification_outcome(log, runner_obj, report, None, None)
        good = SimpleNamespace(certified=True, stages=[])
        phase_support._emit_certification_outcome(
            log, runner_obj, good, ["RESULT: ok"], ["note"]
        )
    finally:
        log.close()


def test_run_drift_check_skip_and_default(tmp_path: Path, monkeypatch) -> None:
    log = phase_support.Log(tmp_path / "run.log")
    try:
        runner_obj = phase_support.Runner(log, keep_going=True)
        args = SimpleNamespace(skip_drift=True, prior_signals=None)
        phase_support._run_drift_check(
            log, runner_obj, str(tmp_path), "m.json", str(tmp_path), args, "sig.json"
        )
        assert runner_obj.results == []

        calls = []
        monkeypatch.setattr(
            runner_obj, "run", lambda *a, **k: calls.append(a[0]) or MagicMock()
        )
        args = SimpleNamespace(skip_drift=False, prior_signals=None)
        phase_support._run_drift_check(
            log, runner_obj, str(tmp_path), "m.json", str(tmp_path), args, "sig.json"
        )
        assert calls == ["spring_drift_check"]
    finally:
        log.close()


def test_quote_and_py_mod() -> None:
    assert phase_support._quote("a b") == '"a b"'
    assert phase_support._quote("ab") == "ab"
    assert phase_support._py_mod("pkg.mod", "--flag")[1:3] == ["-m", "pkg.mod"]


def test_artifact_inventory(tmp_path: Path) -> None:
    out = tmp_path / "out"
    out.mkdir()
    (out / "a.txt").write_text("hi", encoding="utf-8")
    log = phase_support.Log(tmp_path / "run.log")
    try:
        phase_support._artifact_inventory(log, str(out))
    finally:
        log.close()
