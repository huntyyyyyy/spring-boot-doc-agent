"""Coverage climb: ast-grep scanner helper + covering receipt edges."""

from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

from doc_engine.scanning import _scanner_astgrep as ag
from doc_engine.scanning.spring import AstGrepError, AstGrepNotFoundError

pytestmark = pytest.mark.domain_climb_sensor


def test_chunk_paths_empty_and_parse_stdout() -> None:
    assert ag.chunk_paths_for_argv(["ast-grep"], [], 100) == []
    assert ag._parse_ast_grep_stdout("") == []
    assert ag._parse_ast_grep_stdout("[]") == []
    with pytest.raises(AstGrepError):
        ag._parse_ast_grep_stdout("{not-json")


def test_windows_cmdline_and_enrich_query() -> None:
    assert ag._is_windows_cmdline_too_long(OSError("x")) is False
    exc = OSError("too long")
    exc.winerror = 206
    assert ag._is_windows_cmdline_too_long(exc) is True

    entry: dict = {}
    ag._enrich_query_entry(
        entry,
        {"metaVariables": {"multi": {"ARGS": [{"text": '"select 1"'}]}}},
    )
    assert "query_kind" in entry


def test_backend_require_and_version_hash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    backend = ag.AstGrepBackend()
    assert backend.name == "ast-grep"
    monkeypatch.setattr(backend, "_find_ast_grep", lambda: None)
    with pytest.raises(AstGrepNotFoundError):
        backend._require_ast_grep_ready()

    monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/usr/bin/ast-grep")
    monkeypatch.setattr(ag, "RULE_FILE", tmp_path / "missing.yml")
    with pytest.raises(AstGrepNotFoundError, match="rule file"):
        backend._require_ast_grep_ready()

    digest = backend.version_hash()
    assert len(digest) == 16


def test_invoke_oserror_and_scan_chunk_bisect(monkeypatch: pytest.MonkeyPatch) -> None:
    backend = ag.AstGrepBackend()

    def boom_run(*_a, **_k):
        raise OSError("spawn failed")

    monkeypatch.setattr(ag.subprocess, "run", boom_run)
    with pytest.raises(AstGrepError, match="failed to start"):
        backend._invoke_ast_grep(["ast-grep", "scan"])

    win = OSError("cmdline")
    win.winerror = 206

    def win_run(*_a, **_k):
        raise win

    monkeypatch.setattr(ag.subprocess, "run", win_run)
    with pytest.raises(OSError):
        backend._invoke_ast_grep(["ast-grep"])

    other = OSError("other")
    monkeypatch.setattr(
        backend,
        "_invoke_ast_grep",
        lambda cmd: (_ for _ in ()).throw(other),
    )
    with pytest.raises(OSError):
        backend._scan_one_chunk(["base"], ["a.java"], 100)


def test_covering_receipt_and_ingest_gitignore(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    backend = ag.AstGrepBackend()
    monkeypatch.setattr(backend, "version_hash", lambda: "abcd" * 4)
    with pytest.raises(AstGrepError, match="acked"):
        backend._covering_receipt(
            expected_root="abc",
            acked_root="def",
            covered_count=0,
            batches=1,
        )

    ok = backend._covering_receipt(
        expected_root="abc",
        acked_root="abc",
        covered_count=2,
        batches=1,
    )
    assert ok["status"] == "complete"

    evidence: dict = {}
    entities: dict = {}
    seen: set = set()

    class Spec:
        def match_file(self, rel: str) -> bool:
            return rel.endswith("Skip.java")

    backend._ingest_ast_grep_match(
        match={"file": str(tmp_path / "Skip.java"), "range": {"start": {"line": 0}}},
        repo_path=str(tmp_path),
        gitignore_spec=Spec(),
        evidence=evidence,
        entity_table_map_candidates=entities,
        seen=seen,
    )
    assert evidence == {}

    with pytest.raises(AstGrepError, match="no matching evidence bucket"):
        backend._record_bucket_match(
            match={},
            rel="A.java",
            line=1,
            text="@X",
            match_str="@X",
            rule_id="unknownbucket__x",
            evidence=evidence,
        )

    monkeypatch.setattr(
        ag,
        "extract_entity",
        lambda *_a, **_k: None,
    )
    monkeypatch.setattr(ag, "read_source_lines", lambda *_a, **_k: None)
    with pytest.raises(AstGrepError, match="extract_entity"):
        backend._record_entity_match(
            repo_path=str(tmp_path),
            rel="E.java",
            line=1,
            text="@Entity class E {}",
            match_str="@Entity",
            rule_id="persistence__entity",
            evidence=evidence,
            entity_table_map_candidates=entities,
        )


def test_inventory_root_empty_helper() -> None:
    assert isinstance(ag.inventory_root_empty(), str)
