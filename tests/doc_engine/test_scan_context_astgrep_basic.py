"""Ast-grep ScanContext basic covering — LEG8 monkeypatch on façade."""

from __future__ import annotations

import contextlib
import io
from unittest import mock

import pytest

from doc_engine.core.context import ScanContext
from doc_engine.scanning import _scanner_astgrep as facade
from doc_engine.scanning._scanner_astgrep import AstGrepBackend
from tests.conftest import FIXTURE_DIR

pytestmark = pytest.mark.domain_stage0


class TestAstGrepScanContextBasic:
    def test_run_ast_grep_uses_java_files_from_context(self, monkeypatch):
        backend = AstGrepBackend()
        ctx = ScanContext.build(str(FIXTURE_DIR))
        expected_paths = sorted(entry.full_path for entry in ctx.java_files)
        run_mock = mock.Mock(return_value=mock.Mock(returncode=0, stdout="[]", stderr=""))
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade.subprocess, "run", run_mock)

        matches, receipt = backend._run_ast_grep(
            str(FIXTURE_DIR),
            java_files=ctx.java_files,
            file_signatures=dict(ctx.file_signatures),
        )

        assert matches == []
        assert receipt["status"] == "complete"
        cmd = run_mock.call_args[0][0]
        for path in expected_paths:
            assert path in cmd
        assert str(FIXTURE_DIR) not in cmd

    def test_run_ast_grep_empty_java_files_skips_subprocess(self, monkeypatch):
        backend = AstGrepBackend()
        run_mock = mock.Mock()
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade.subprocess, "run", run_mock)

        matches, receipt = backend._run_ast_grep(
            str(FIXTURE_DIR),
            java_files=[],
            file_signatures={},
        )
        assert matches == []
        assert receipt["status"] == "complete"
        run_mock.assert_not_called()

    def test_run_ast_grep_chunks_paths_instead_of_repo_root_fallback(self, monkeypatch):
        backend = AstGrepBackend()
        ctx = ScanContext.build(str(FIXTURE_DIR))
        if len(ctx.java_files) < 2:
            pytest.skip("fixture needs >=2 java files to observe chunking")
        run_mock = mock.Mock(return_value=mock.Mock(returncode=0, stdout="[]", stderr=""))
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade, "_PATH_LIST_CHAR_LIMIT", 10)
        monkeypatch.setattr(facade.subprocess, "run", run_mock)

        backend._run_ast_grep(
            str(FIXTURE_DIR),
            java_files=ctx.java_files,
            file_signatures=dict(ctx.file_signatures),
        )

        assert run_mock.call_count > 1
        seen = []
        for call in run_mock.call_args_list:
            cmd = call[0][0]
            assert cmd[-1] != str(FIXTURE_DIR)
            for entry in ctx.java_files:
                if entry.full_path in cmd:
                    seen.append(entry.full_path)
        assert sorted(set(seen)) == sorted(e.full_path for e in ctx.java_files)

    def test_chunking_warns_and_never_mentions_repo_root_fallback(self, monkeypatch):
        backend = AstGrepBackend()
        ctx = ScanContext.build(str(FIXTURE_DIR))
        if len(ctx.java_files) < 2:
            pytest.skip("fixture needs >=2 java files to observe chunking")
        run_mock = mock.Mock(return_value=mock.Mock(returncode=0, stdout="[]", stderr=""))
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade, "_PATH_LIST_CHAR_LIMIT", 10)
        monkeypatch.setattr(facade.subprocess, "run", run_mock)

        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            backend._run_ast_grep(
                str(FIXTURE_DIR),
                java_files=ctx.java_files,
                file_signatures=dict(ctx.file_signatures),
            )
        text = err.getvalue()
        assert "preserve ScanContext inventory" in text
        assert "scanning repo root instead" not in text
