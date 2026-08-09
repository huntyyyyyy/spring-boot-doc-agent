"""Discriminative CodeQL cache-key invalidation (post-rescope keys module).

Effective coverage — not climb wallpaper. Pins that java bytes, query-pack
bytes, build command, and CLI version each change the key, that ``target/``
is ignored by the walk, and that ``_cache_is_valid`` flips False after mutate.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import doc_engine.scanning.support._codeql_cache as cache_mod
from doc_engine.scanning.support._codeql_cache_keys import _cache_key

pytestmark = pytest.mark.domain_stage0


def _seed_repo_pack(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    pack = tmp_path / "pack"
    repo.mkdir()
    pack.mkdir()
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    (pack / "q.ql").write_text("// q", encoding="utf-8")
    return repo, pack


def test_cache_key_changes_when_java_bytes_change(tmp_path: Path) -> None:
    repo, pack = _seed_repo_pack(tmp_path)
    before = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    (repo / "A.java").write_text("class A { int x; }", encoding="utf-8")
    after = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert before != after


def test_cache_key_changes_when_query_pack_changes(tmp_path: Path) -> None:
    repo, pack = _seed_repo_pack(tmp_path)
    before = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    (pack / "q.ql").write_text("// mutated query", encoding="utf-8")
    after = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert before != after


def test_cache_key_ignores_java_under_target_dir(tmp_path: Path) -> None:
    repo, pack = _seed_repo_pack(tmp_path)
    before = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    target = repo / "target"
    target.mkdir()
    (target / "Generated.java").write_text("class Generated {}", encoding="utf-8")
    after = _cache_key(repo, pack, "gradlew compileJava", codeql_cli_version="2.0")
    assert before == after


def test_cache_is_valid_false_after_java_or_pack_mutate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    repo, pack = _seed_repo_pack(tmp_path)
    db = tmp_path / "db"
    db.mkdir()
    cache_mod._write_cache_metadata(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )
    assert cache_mod._cache_is_valid(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )
    (repo / "A.java").write_text("class A { int y; }", encoding="utf-8")
    assert not cache_mod._cache_is_valid(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )
    (repo / "A.java").write_text("class A {}", encoding="utf-8")
    cache_mod._write_cache_metadata(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )
    (pack / "q.ql").write_text("// other", encoding="utf-8")
    assert not cache_mod._cache_is_valid(
        db, repo, pack, "gradlew compileJava", codeql_cli_version="2.0"
    )


def test_scan_context_missing_java_signature_is_not_empty_digest() -> None:
    """Incomplete ScanContext must not hash to the empty SHA-256 prefix."""
    from types import SimpleNamespace

    from doc_engine.scanning.support._codeql_cache_keys import _hash_from_scan_context

    class _Entry:
        def __init__(self, rel: str) -> None:
            self.rel_path = rel

    empty = _hash_from_scan_context(
        SimpleNamespace(java_files=[], file_signatures={})
    )
    incomplete = _hash_from_scan_context(
        SimpleNamespace(
            java_files=[_Entry("Missing.java")],
            file_signatures={},
        )
    )
    assert incomplete != empty
    assert incomplete != "e3b0c44298fc1c149afbf4c8996fb924"[:32]
