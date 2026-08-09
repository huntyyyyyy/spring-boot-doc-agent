"""Cohesive suite from tests/doc_engine/test_covering_hard_stops.py: DestructiveFailClosedTest, FixtureCliCoveringSmokeTest."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pytest

from doc_engine.core.context import FileEntry, ScanContext
from doc_engine.scanning import _scanner_astgrep as facade
from doc_engine.scanning._orchestrator import CoveringProofError
from doc_engine.scanning._scanner_astgrep import AstGrepBackend
from doc_engine.scanning.covering import (
    build_covering_proof,
    verify_covering_proof,
    write_covering_proof,
)
from doc_engine.scanning.facts import (
    facts_from_signals,
)
from doc_engine.scanning.gap_probe import (
    _astgrep_receipt_complete,
    load_and_verify_covering,
)
from doc_engine.scanning.spring import AstGrepError, scan
from tests.conftest import FIXTURE_DIR, REPO_ROOT
from tests.support.covering_hard_stops.fixtures import (
    _assert_absence_stamps_match_writer,
    _complete_receipt,
    shutil_which,
)

pytestmark = pytest.mark.domain_stage0

class TestDestructiveFailClosed:
    def test_winerror_206_solo_path_raises(self, monkeypatch):
        """Deviation: single-path WinError 206 soft-skipped as empty matches."""
        backend = AstGrepBackend()
        entry = FileEntry(
            full_path="/repo/" + ("x" * 200) + ".java",
            rel_path=("x" * 200) + ".java",
            name=("x" * 200) + ".java",
            ext=".java",
        )
        sigs = {entry.rel_path: "sig"}
        win_exc = OSError(22, "filename or extension is too long")
        win_exc.winerror = 206
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        monkeypatch.setattr(
            facade.subprocess, "run", mock.Mock(side_effect=win_exc)
        )
        with pytest.raises(AstGrepError) as ctx:
            backend._run_ast_grep(
                "/repo", java_files=[entry], file_signatures=sigs,
            )
        assert "incomplete inventory" in str(ctx.value)

    def test_empty_java_list_with_java_signatures_fails(self, monkeypatch):
        """Deviation: java_files=[] while signatures list .java still greens."""
        backend = AstGrepBackend()
        monkeypatch.setattr(backend, "_find_ast_grep", lambda: "/bin/ast-grep")
        with pytest.raises(AstGrepError) as ctx:
            backend._run_ast_grep(
                "/repo",
                java_files=[],
                file_signatures={"StillThere.java": "abc"},
            )
        assert "empty java_files" in str(ctx.value)

    def test_mid_batch_fail_propagates_through_scan(self, monkeypatch):
        """Deviation: mid-batch ast-grep failure soft-continues into Path A."""
        ctx = ScanContext.build(str(FIXTURE_DIR))
        if len(ctx.java_files) < 1:
            pytest.skip("fixture needs java files")
        monkeypatch.setattr(
            "doc_engine.scanning._scanner_astgrep.AstGrepBackend._invoke_ast_grep",
            mock.Mock(side_effect=AstGrepError("exited with status 1: boom")),
        )
        with pytest.raises((AstGrepError, CoveringProofError)):
            scan(str(FIXTURE_DIR), scanners=["filesystem", "ast-grep"])

    def test_load_and_verify_covering_rejects_scanner_version_drift(self):
        """Deviation: covering_proof with drifted scanner_version still verifies."""
        sigs = {"a.java": "1"}
        proof = build_covering_proof(
            file_signatures=sigs,
            scanner_version="old",
            receipts=[_complete_receipt("filesystem", sigs)],
        )
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "covering_proof.json"
            write_covering_proof(path, proof)
            signals = {"file_signatures": sigs, "scanner_version": "new"}
            _, ok, why = load_and_verify_covering(
                signals, covering_path=path,
            )
        assert ok is False
        assert "scanner_version" in why


class FixtureCliCoveringSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil_which("ast-grep"):
            raise unittest.SkipTest("ast-grep not on PATH")

    def test_cli_writes_covering_and_strips_internal_keys(self):
        """Deviation: CLI greens Path A without covering sibling or with internal keys."""
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td)
            signals_out = out_dir / "spring_signals.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "doc_engine.tools.spring_signal_scan",
                    str(FIXTURE_DIR),
                    "--out",
                    str(signals_out),
                    "--scanners",
                    "filesystem,ast-grep",
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            covering = out_dir / "covering_proof.json"
            facts = out_dir / "facts.jsonl"
            self.assertTrue(covering.is_file(), "covering_proof.json missing")
            self.assertTrue(facts.is_file(), "facts.jsonl missing")
            path_a = json.loads(signals_out.read_text(encoding="utf-8"))
            self.assertNotIn("_covering_proof", path_a)
            self.assertNotIn("_scan_partials_meta", path_a)
            proof = json.loads(covering.read_text(encoding="utf-8"))
            ok, why = verify_covering_proof(
                proof,
                file_signatures=path_a["file_signatures"],
                scanner_version=path_a["scanner_version"],
            )
            self.assertTrue(ok, why)
            self.assertIn("covering_emit", proc.stderr)
            fact_rows = [
                json.loads(line)
                for line in facts.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            _assert_absence_stamps_match_writer(
                self,
                path_a,
                covering_ok=ok,
                covering_root=proof.get("inventory_root"),
                scanner_version=path_a.get("scanner_version"),
                astgrep_receipt_complete=_astgrep_receipt_complete(proof),
                actual_rows=fact_rows,
            )

    def test_in_process_scan_attaches_covering_proof(self):
        """Deviation: in-process scan() returns Path A without covering attachment."""
        result = scan(str(FIXTURE_DIR), scanners=["filesystem", "ast-grep"])
        self.assertIn("_covering_proof", result)
        self.assertIn("_scan_partials_meta", result)
        ok, why = verify_covering_proof(
            result["_covering_proof"],
            file_signatures=result["file_signatures"],
            scanner_version=result["scanner_version"],
        )
        self.assertTrue(ok, why)
        facts = facts_from_signals(result)
        _assert_absence_stamps_match_writer(
            self,
            result,
            covering_ok=ok,
            covering_root=result["_covering_proof"].get("inventory_root"),
            scanner_version=result.get("scanner_version"),
            astgrep_receipt_complete=_astgrep_receipt_complete(
                result["_covering_proof"]
            ),
            actual_rows=facts,
        )
