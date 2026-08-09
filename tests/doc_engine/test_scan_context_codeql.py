"""Cohesive suite from tests/doc_engine/test_scan_context_wiring.py: CodeQLScanContextWiringTest."""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path
from unittest import mock
from doc_engine.core.context import FileEntry, ScanContext
from doc_engine.scanning._scanner_astgrep import (
    AstGrepBackend,
    chunk_paths_for_argv,
)
from doc_engine.scanning.support._codeql_runner import (
    DEFAULT_PACK_DIR,
    _cache_key,
    _repo_content_hash,
)
from tests.conftest import FIXTURE_DIR

class CodeQLScanContextWiringTest(unittest.TestCase):
    def test_repo_content_hash_uses_context_signatures(self):
        repo = Path(FIXTURE_DIR)
        ctx = ScanContext.build(str(repo))
        with_hash = _repo_content_hash(repo, scan_context=ctx)
        without_hash = _repo_content_hash(repo, scan_context=None)
        self.assertNotEqual(with_hash, without_hash)

    def test_cache_key_changes_when_context_signature_changes(self):
        repo = Path(FIXTURE_DIR)
        ctx = ScanContext.build(str(repo))
        build_command = "gradlew clean compileJava"
        key_before = _cache_key(repo, DEFAULT_PACK_DIR, build_command, scan_context=ctx)

        if not ctx.java_files:
            self.skipTest("fixture has no java files")
        rel = ctx.java_files[0].rel_path
        ctx.file_signatures[rel] = "mutated-signature"

        key_after = _cache_key(repo, DEFAULT_PACK_DIR, build_command, scan_context=ctx)
        self.assertNotEqual(key_before, key_after)

    def test_cache_key_includes_build_command(self):
        repo = Path(FIXTURE_DIR)
        ctx = ScanContext.build(str(repo))
        key_compile = _cache_key(repo, DEFAULT_PACK_DIR, "gradlew compileJava", scan_context=ctx)
        key_test = _cache_key(repo, DEFAULT_PACK_DIR, "gradlew compileTestJava", scan_context=ctx)
        self.assertNotEqual(key_compile, key_test)
