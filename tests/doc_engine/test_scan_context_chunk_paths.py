"""Cohesive suite from tests/doc_engine/test_scan_context_wiring.py: ChunkPathsForArgvTest."""

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

class ChunkPathsForArgvTest(unittest.TestCase):
    def test_single_chunk_when_under_budget(self):
        base = ["ast-grep", "scan"]
        paths = ["a.java", "b.java"]
        chunks = chunk_paths_for_argv(base, paths, limit=10_000)
        self.assertEqual(chunks, [paths])

    def test_splits_when_over_budget(self):
        base = ["ast-grep"]  # len 8 + 1 = 9
        # Each path costs len+1; budget after base ≈ 20 → one short path per chunk.
        paths = ["abcdefghij.java", "klmnopqrst.java", "uvwxyz0123.java"]
        chunks = chunk_paths_for_argv(base, paths, limit=30)
        self.assertEqual(len(chunks), 3)
        self.assertEqual([p for chunk in chunks for p in chunk], paths)

    def test_oversized_solo_path_still_emitted(self):
        base = ["ast-grep"]
        huge = "x" * 100
        chunks = chunk_paths_for_argv(base, [huge, "ok.java"], limit=20)
        self.assertEqual(chunks[0], [huge])
        self.assertIn(["ok.java"], chunks)
