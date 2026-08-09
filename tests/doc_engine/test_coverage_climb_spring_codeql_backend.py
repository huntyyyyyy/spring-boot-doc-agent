"""Coverage climb: spring scan + CodeQL backend ingest."""

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
import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_cli as cli_mod
import doc_engine.scanning.support._codeql_database as db_mod
import doc_engine.scanning.support._codeql_queries as queries_mod

pytestmark = pytest.mark.domain_climb_sensor

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
