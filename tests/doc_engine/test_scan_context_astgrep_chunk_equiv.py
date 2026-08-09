"""Ast-grep chunk equivalence — LEG8 monkeypatch on façade."""

from __future__ import annotations

import json
from unittest import mock

import pytest

from doc_engine.core.context import FileEntry
from doc_engine.scanning import _scanner_astgrep as facade
from doc_engine.scanning._scanner_astgrep import AstGrepBackend
from doc_engine.scanning.spring import AstGrepError
from tests.conftest import FIXTURE_DIR

pytestmark = pytest.mark.domain_stage0


class TestAstGrepScanContextChunkEquiv:
    def test_chunked_matches_equivalent_to_single_invocation(self, monkeypatch):
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

        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade, "_PATH_LIST_CHAR_LIMIT", 2**31)
        one_mock = mock.Mock(side_effect=_stdout_for_cmd)
        monkeypatch.setattr(facade.subprocess, "run", one_mock)
        single, _ = backend._run_ast_grep(
            "/repo", java_files=entries, file_signatures=sigs,
        )

        monkeypatch.setattr(facade, "_PATH_LIST_CHAR_LIMIT", 40)
        many_mock = mock.Mock(side_effect=_stdout_for_cmd)
        monkeypatch.setattr(facade.subprocess, "run", many_mock)
        chunked, _ = backend._run_ast_grep(
            "/repo", java_files=entries, file_signatures=sigs,
        )

        assert one_mock.call_count == 1
        assert many_mock.call_count > 1
        assert single == chunked
        assert [m["file"] for m in single] == [e.full_path for e in entries]

    def test_run_ast_grep_none_inventory_fails_closed(self, monkeypatch):
        backend = AstGrepBackend()
        run_mock = mock.Mock(return_value=mock.Mock(returncode=0, stdout="[]", stderr=""))
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade.subprocess, "run", run_mock)
        with pytest.raises(AstGrepError) as ctx:
            backend._run_ast_grep(str(FIXTURE_DIR), java_files=None)
        assert "inventory not supplied" in str(ctx.value)

    def test_run_ast_grep_bisects_on_winerror_206(self, monkeypatch):
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

        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        run_mock = mock.Mock(side_effect=_run)
        monkeypatch.setattr(facade.subprocess, "run", run_mock)
        matches, receipt = backend._run_ast_grep(
            "/repo", java_files=entries, file_signatures=sigs,
        )

        assert run_mock.call_count == 3
        assert len(matches) == 2
        assert receipt["status"] == "complete"
        assert receipt.get("winerror_206_bisects", 0) >= 1
        for call in run_mock.call_args_list:
            cmd = call[0][0]
            assert any(str(p).endswith(".java") for p in cmd)
            assert cmd[-1] != "/repo"

    def test_mid_batch_nonzero_exit_fails_closed(self, monkeypatch):
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
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(facade, "_PATH_LIST_CHAR_LIMIT", 40)
        run_mock = mock.Mock(
            return_value=mock.Mock(returncode=1, stdout="", stderr="boom"),
        )
        monkeypatch.setattr(facade.subprocess, "run", run_mock)
        with pytest.raises(AstGrepError) as ctx:
            backend._run_ast_grep(
                "/repo", java_files=entries, file_signatures=sigs,
            )
        assert "exited with status 1" in str(ctx.value)
