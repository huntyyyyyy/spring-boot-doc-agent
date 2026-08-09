"""Cohesive suite from tests/doc_engine/test_scan_context_wiring.py: AstGrepScanContextBasicTest."""

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

import pytest

pytestmark = pytest.mark.domain_stage0

class AstGrepScanContextBasicTest(unittest.TestCase):
    def test_run_ast_grep_uses_java_files_from_context(self):
            backend = AstGrepBackend()
            ctx = ScanContext.build(str(FIXTURE_DIR))
            expected_paths = sorted(entry.full_path for entry in ctx.java_files)

            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch("subprocess.run") as run_mock:
                    run_mock.return_value = mock.Mock(returncode=0, stdout="[]", stderr="")
                    matches, receipt = backend._run_ast_grep(
                        str(FIXTURE_DIR),
                        java_files=ctx.java_files,
                        file_signatures=dict(ctx.file_signatures),
                    )

            self.assertEqual(matches, [])
            self.assertEqual(receipt["status"], "complete")
            cmd = run_mock.call_args[0][0]
            for path in expected_paths:
                self.assertIn(path, cmd)
            self.assertNotIn(str(FIXTURE_DIR), cmd)

    def test_run_ast_grep_empty_java_files_skips_subprocess(self):
            backend = AstGrepBackend()
            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch("subprocess.run") as run_mock:
                    matches, receipt = backend._run_ast_grep(
                        str(FIXTURE_DIR),
                        java_files=[],
                        file_signatures={},
                    )
            self.assertEqual(matches, [])
            self.assertEqual(receipt["status"], "complete")
            run_mock.assert_not_called()

    def test_run_ast_grep_chunks_paths_instead_of_repo_root_fallback(self):
            backend = AstGrepBackend()
            ctx = ScanContext.build(str(FIXTURE_DIR))
            if len(ctx.java_files) < 2:
                self.skipTest("fixture needs >=2 java files to observe chunking")

            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch(
                    "doc_engine.scanning._scanner_astgrep._PATH_LIST_CHAR_LIMIT", 10,
                ):
                    with mock.patch("subprocess.run") as run_mock:
                        run_mock.return_value = mock.Mock(returncode=0, stdout="[]", stderr="")
                        backend._run_ast_grep(
                            str(FIXTURE_DIR),
                            java_files=ctx.java_files,
                            file_signatures=dict(ctx.file_signatures),
                        )

            self.assertGreater(run_mock.call_count, 1)
            seen = []
            for call in run_mock.call_args_list:
                cmd = call[0][0]
                self.assertNotEqual(cmd[-1], str(FIXTURE_DIR))
                # Every argv after the base flags is an inventory path, not repo root.
                for entry in ctx.java_files:
                    if entry.full_path in cmd:
                        seen.append(entry.full_path)
            self.assertEqual(sorted(set(seen)), sorted(e.full_path for e in ctx.java_files))

    def test_chunking_warns_and_never_mentions_repo_root_fallback(self):
            backend = AstGrepBackend()
            ctx = ScanContext.build(str(FIXTURE_DIR))
            if len(ctx.java_files) < 2:
                self.skipTest("fixture needs >=2 java files to observe chunking")

            err = io.StringIO()
            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch(
                    "doc_engine.scanning._scanner_astgrep._PATH_LIST_CHAR_LIMIT", 10,
                ):
                    with mock.patch("subprocess.run") as run_mock:
                        run_mock.return_value = mock.Mock(returncode=0, stdout="[]", stderr="")
                        with contextlib.redirect_stderr(err):
                            backend._run_ast_grep(
                                str(FIXTURE_DIR),
                                java_files=ctx.java_files,
                                file_signatures=dict(ctx.file_signatures),
                            )

            text = err.getvalue()
            self.assertIn("preserve ScanContext inventory", text)
            self.assertNotIn("scanning repo root instead", text)
