"""Cohesive suite from tests/ci/test_run_manifest.py: AtomicWriteTest, GitHelpersTest, InitManifestTest, StageLifecycleTest, FinalizeStatusTest."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import run_manifest, spring_signal_scan

import pytest

pytestmark = pytest.mark.domain_ci_meta

SCRIPT_DIR = SCRIPTS_DIR
RUN_MANIFEST_CMD = [sys.executable, "-m", "doc_engine.tools.run_manifest"]
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "schemas", "run_manifest.schema.json")
from tests.support.run_manifest.harness import (
    _fake_completed,
    validate_manifest_shape,
)

class AtomicWriteTest(unittest.TestCase):
    def test_write_and_read_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "run_manifest.json")
            run_manifest._write_json_atomic(path, {"a": 1})
            self.assertEqual(run_manifest._read_json(path), {"a": 1})
            # No leftover temp files after a successful write.
            leftovers = [f for f in os.listdir(d) if f != "run_manifest.json"]
            self.assertEqual(leftovers, [])

    def test_interrupted_write_leaves_prior_file_intact(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "run_manifest.json")
            run_manifest._write_json_atomic(path, {"version": 1})

            with mock.patch.object(run_manifest.os, "replace", side_effect=OSError("simulated interruption")):
                with self.assertRaises(OSError):
                    run_manifest._write_json_atomic(path, {"version": 2})

            # The prior valid file must survive an interrupted second write.
            self.assertEqual(run_manifest._read_json(path), {"version": 1})
            leftovers = [f for f in os.listdir(d) if f != "run_manifest.json"]
            self.assertEqual(leftovers, [], "the failed temp file should have been cleaned up")

class GitHelpersTest(unittest.TestCase):
    def test_commit_hash_success(self):
        with mock.patch.object(run_manifest.subprocess, "run",
                                return_value=_fake_completed(stdout="abc123\n")):
            self.assertEqual(run_manifest.git_commit_hash("/fake/repo"), "abc123")

    def test_commit_hash_git_not_on_path(self):
        with mock.patch.object(run_manifest.subprocess, "run", side_effect=FileNotFoundError("no git")):
            self.assertIsNone(run_manifest.git_commit_hash("/fake/repo"))

    def test_commit_hash_nonzero_returncode_not_a_repo(self):
        with mock.patch.object(run_manifest.subprocess, "run",
                                return_value=_fake_completed(returncode=128, stderr="not a git repository")):
            self.assertIsNone(run_manifest.git_commit_hash("/fake/repo"))

    def test_dirty_true_when_porcelain_nonempty(self):
        with mock.patch.object(run_manifest.subprocess, "run",
                                return_value=_fake_completed(stdout=" M some/file.java\n")):
            self.assertTrue(run_manifest.git_is_dirty("/fake/repo"))

    def test_dirty_false_when_porcelain_empty(self):
        with mock.patch.object(run_manifest.subprocess, "run", return_value=_fake_completed(stdout="")):
            self.assertFalse(run_manifest.git_is_dirty("/fake/repo"))

    def test_dirty_none_on_failure(self):
        with mock.patch.object(run_manifest.subprocess, "run", side_effect=FileNotFoundError("no git")):
            self.assertIsNone(run_manifest.git_is_dirty("/fake/repo"))

class InitManifestTest(unittest.TestCase):
    def test_shape_and_defaults(self):
        with mock.patch.object(run_manifest, "git_commit_hash", return_value="deadbeef"), \
             mock.patch.object(run_manifest, "git_is_dirty", return_value=False):
            manifest = run_manifest.build_init_manifest("/fake/repo", now_ms=1_700_000_000_000)
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["status"], "running")
        self.assertEqual(manifest["stages"], [])
        self.assertEqual(manifest["target_repo"]["commit_hash"], "deadbeef")
        self.assertFalse(manifest["target_repo"]["dirty"])
        self.assertTrue(manifest["run_id"].startswith("2023-11-14T22:13:20Z-"))
        self.assertEqual(validate_manifest_shape(manifest), [])

class StageLifecycleTest(unittest.TestCase):
    def _blank_manifest(self):
        return {"stages": []}

    def test_start_then_end_records_duration(self):
        m = self._blank_manifest()
        run_manifest.start_stage(m, "signal_scan", now_ms=1000)
        run_manifest.end_stage(m, "signal_scan", "complete", now_ms=1500)
        stage = m["stages"][0]
        self.assertEqual(stage["status"], "complete")
        self.assertEqual(stage["start_time_ms"], 1000)
        self.assertEqual(stage["end_time_ms"], 1500)
        self.assertEqual(stage["duration_ms"], 500)
        self.assertIsNone(stage["error"])

    def test_end_stage_records_error(self):
        m = self._blank_manifest()
        run_manifest.start_stage(m, "doc_writer", now_ms=0)
        run_manifest.end_stage(m, "doc_writer", "failed", error="subagent timeout", now_ms=10)
        self.assertEqual(m["stages"][0]["error"], "subagent timeout")

    def test_end_stage_unknown_name_raises(self):
        m = self._blank_manifest()
        with self.assertRaises(ValueError):
            run_manifest.end_stage(m, "nonexistent", "complete", now_ms=10)

    def test_end_stage_invalid_status_raises(self):
        m = self._blank_manifest()
        run_manifest.start_stage(m, "architect", now_ms=0)
        with self.assertRaises(ValueError):
            run_manifest.end_stage(m, "architect", "running", now_ms=10)

    def test_retry_case_resolves_in_append_order(self):
        # A stage that failed, then was retried: two start/end pairs for
        # the same name. end-stage must resolve each call against its own
        # immediately-preceding still-running entry, not an earlier,
        # already-ended one.
        m = self._blank_manifest()
        run_manifest.start_stage(m, "file_summarize", fanout=3, now_ms=0)
        run_manifest.end_stage(m, "file_summarize", "failed", error="ast-grep crashed", now_ms=100)
        run_manifest.start_stage(m, "file_summarize", fanout=3, now_ms=200)
        run_manifest.end_stage(m, "file_summarize", "complete", now_ms=400)

        self.assertEqual(len(m["stages"]), 2)
        first, second = m["stages"]
        self.assertEqual(first["status"], "failed")
        self.assertEqual(first["duration_ms"], 100)
        self.assertEqual(second["status"], "complete")
        self.assertEqual(second["start_time_ms"], 200)
        self.assertEqual(second["duration_ms"], 200)

class FinalizeStatusTest(unittest.TestCase):
    def _manifest_with_stages(self, *statuses):
        stages = []
        for i, status in enumerate(statuses):
            stages.append({
                "name": f"stage{i}", "status": status,
                "start_time_ms": 0, "end_time_ms": 100 if status != "running" else None,
                "duration_ms": 100 if status != "running" else None, "error": None, "actual_fanout": None,
            })
        return {"stages": stages, "timestamp_start": "2026-01-01T00:00:00Z"}

    def test_infer_complete_when_all_stages_complete(self):
        m = self._manifest_with_stages("complete", "complete")
        m, warnings = run_manifest.finalize_manifest(m, now_ms=1000)
        self.assertEqual(m["status"], "complete")
        self.assertEqual(warnings, [])

    def test_infer_failed_takes_priority(self):
        m = self._manifest_with_stages("complete", "failed", "canceled")
        m, _ = run_manifest.finalize_manifest(m, now_ms=1000)
        self.assertEqual(m["status"], "failed")

    def test_stage_left_running_is_auto_canceled_and_status_partial(self):
        m = self._manifest_with_stages("complete", "running")
        m, warnings = run_manifest.finalize_manifest(m, now_ms=1000)
        self.assertEqual(m["stages"][1]["status"], "canceled")
        self.assertIsNotNone(m["stages"][1]["error"])
        self.assertEqual(m["stages"][1]["end_time_ms"], 1000)
        self.assertEqual(m["status"], "partial")
        self.assertEqual(len(warnings), 1)

    def test_explicit_status_override_wins(self):
        m = self._manifest_with_stages("complete", "complete")
        m, _ = run_manifest.finalize_manifest(m, status="failed", now_ms=1000)
        self.assertEqual(m["status"], "failed")
