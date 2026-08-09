"""Cohesive suite from tests/doc_engine/test_scan_context_wiring.py: AstGrepScanContextChunkEquivTest."""

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

class AstGrepScanContextChunkEquivTest(unittest.TestCase):
    def test_chunked_matches_equivalent_to_single_invocation(self):
            """Path-list vs artificially-budgeted batches: same concatenated matches."""
            backend = AstGrepBackend()
            entries = [
                FileEntry(
                    full_path=f"/repo/F{i}.java",
                    rel_path=f"F{i}.java",
                    name=f"F{i}.java",
                    ext=".java",
                )
                for i in range(4)
            ]
            sigs = {e.rel_path: f"sig{i}" for i, e in enumerate(entries)}

            def _stdout_for_cmd(cmd, **_kwargs):
                files = [p for p in cmd if str(p).endswith(".java")]
                payload = [{"file": f, "ruleId": "persistence__entity"} for f in files]
                return mock.Mock(returncode=0, stdout=json.dumps(payload), stderr="")

            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch(
                    "doc_engine.scanning._scanner_astgrep._PATH_LIST_CHAR_LIMIT", 2**31,
                ):
                    with mock.patch("subprocess.run", side_effect=_stdout_for_cmd) as one_mock:
                        single, _ = backend._run_ast_grep(
                            "/repo", java_files=entries, file_signatures=sigs,
                        )
                with mock.patch(
                    "doc_engine.scanning._scanner_astgrep._PATH_LIST_CHAR_LIMIT", 40,
                ):
                    with mock.patch("subprocess.run", side_effect=_stdout_for_cmd) as many_mock:
                        chunked, _ = backend._run_ast_grep(
                            "/repo", java_files=entries, file_signatures=sigs,
                        )

            self.assertEqual(one_mock.call_count, 1)
            self.assertGreater(many_mock.call_count, 1)
            self.assertEqual(single, chunked)
            self.assertEqual([m["file"] for m in single], [e.full_path for e in entries])

    def test_run_ast_grep_none_inventory_fails_closed(self):
            """Legacy path: java_files is None cannot prove covering — raises."""
            from doc_engine.scanning.spring import AstGrepError

            backend = AstGrepBackend()
            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch("subprocess.run") as run_mock:
                    run_mock.return_value = mock.Mock(returncode=0, stdout="[]", stderr="")
                    with self.assertRaises(AstGrepError) as ctx:
                        backend._run_ast_grep(str(FIXTURE_DIR), java_files=None)
            self.assertIn("inventory not supplied", str(ctx.exception))

    def test_run_ast_grep_bisects_on_winerror_206(self):
            backend = AstGrepBackend()
            entries = [
                FileEntry(
                    full_path=f"/repo/A{i}.java",
                    rel_path=f"A{i}.java",
                    name=f"A{i}.java",
                    ext=".java",
                )
                for i in range(4)
            ]
            sigs = {e.rel_path: f"sig{i}" for i, e in enumerate(entries)}
            win_exc = OSError(22, "filename or extension is too long")
            win_exc.winerror = 206

            # First call: whole inventory hits WinError 206; subsequent halves succeed.
            responses = [
                win_exc,
                mock.Mock(returncode=0, stdout='[{"file":"/repo/A0.java"}]', stderr=""),
                mock.Mock(returncode=0, stdout='[{"file":"/repo/A2.java"}]', stderr=""),
            ]

            def _run(cmd, **_kwargs):
                item = responses.pop(0)
                if isinstance(item, OSError):
                    raise item
                return item

            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch("subprocess.run", side_effect=_run) as run_mock:
                    matches, receipt = backend._run_ast_grep(
                        "/repo", java_files=entries, file_signatures=sigs,
                    )

            self.assertEqual(run_mock.call_count, 3)
            self.assertEqual(len(matches), 2)
            self.assertEqual(receipt["status"], "complete")
            self.assertGreaterEqual(receipt.get("winerror_206_bisects", 0), 1)
            for call in run_mock.call_args_list:
                cmd = call[0][0]
                # Inventory paths only — never a bare repo-root argv.
                self.assertTrue(any(str(p).endswith(".java") for p in cmd))
                self.assertNotEqual(cmd[-1], "/repo")

    def test_mid_batch_nonzero_exit_fails_closed(self):
            from doc_engine.scanning.spring import AstGrepError

            backend = AstGrepBackend()
            entries = [
                FileEntry(
                    full_path=f"/repo/B{i}.java",
                    rel_path=f"B{i}.java",
                    name=f"B{i}.java",
                    ext=".java",
                )
                for i in range(2)
            ]
            sigs = {e.rel_path: "x" for e in entries}
            with mock.patch.object(backend, "_find_ast_grep", return_value="/bin/ast-grep"):
                with mock.patch(
                    "doc_engine.scanning._scanner_astgrep._PATH_LIST_CHAR_LIMIT", 40,
                ):
                    with mock.patch("subprocess.run") as run_mock:
                        run_mock.return_value = mock.Mock(
                            returncode=1, stdout="", stderr="boom",
                        )
                        with self.assertRaises(AstGrepError) as ctx:
                            backend._run_ast_grep(
                                "/repo", java_files=entries, file_signatures=sigs,
                            )
            self.assertIn("exited with status 1", str(ctx.exception))
