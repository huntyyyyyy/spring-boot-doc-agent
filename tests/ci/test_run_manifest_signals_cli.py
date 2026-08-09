"""Cohesive suite from tests/ci/test_run_manifest.py: FileSignaturesTest, EvidenceTagCountsTest, InterviewParseTest, CapacityPreflightTieInTest, CLIRoundTripTest."""

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

class FileSignaturesTest(unittest.TestCase):
    def test_reuse_from_signals_file(self):
        fake_sigs = {"src/Foo.java": "sha256:abc"}
        with tempfile.TemporaryDirectory() as d:
            signals_path = os.path.join(d, "spring_signals.json")
            with open(signals_path, "w", encoding="utf-8") as f:
                json.dump({"file_signatures": fake_sigs}, f)
            result = run_manifest.load_file_signatures(signals_file=signals_path)
        self.assertEqual(result, fake_sigs)

    def test_fresh_scan_matches_spring_signal_scan_directly(self):
        rel = "src/main/java/com/example/billing/Invoice.java"
        result = run_manifest.load_file_signatures(repo_path=FIXTURE_DIR)
        self.assertIn(rel, result)
        expected = spring_signal_scan.compute_file_signature(
            os.path.join(FIXTURE_DIR, rel.replace("/", os.sep)),
        )
        self.assertEqual(result[rel], expected)

    def test_no_signals_file_and_no_repo_path_returns_empty(self):
        self.assertEqual(run_manifest.load_file_signatures(), {})

class EvidenceTagCountsTest(unittest.TestCase):
    def test_counts_remapped_and_only_known_files_read(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "readme.md"), "w", encoding="utf-8") as f:
                f.write(
                    "Uses PostgreSQL [Evidenced — build.gradle]. "
                    "Deploy cadence is weekly [Confirmed — interview, 2026-07-23]. "
                    "Retry policy [Unknown — not evidenced in code, not covered in interview]."
                )
            # Not one of the fourteen — must be ignored.
            with open(os.path.join(d, "notes.md"), "w", encoding="utf-8") as f:
                f.write("[Evidenced — irrelevant.java:1]")

            result = run_manifest.compute_evidence_tag_counts(d)

        self.assertEqual(set(result.keys()), {"readme.md"})
        self.assertEqual(result["readme.md"], {"Evidenced": 1, "Confirmed": 1, "Unknown": 1, "PerExistingDocs": 0})

class InterviewParseTest(unittest.TestCase):
    def test_well_formed_list(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "interview_answers.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump([
                    {"id": "a", "question": "q1", "status": "answered", "answer": "x", "date": "2026-07-24"},
                    {"id": "b", "question": "q2", "status": "skipped", "answer": None, "date": "2026-07-24"},
                ], f)
            result = run_manifest.parse_interview_file(path)
        self.assertEqual(result, {
            "asked": 2, "answered": 1, "skipped": 1,
            "questions": [{"id": "a", "status": "answered"}, {"id": "b", "status": "skipped"}],
        })

    def test_missing_file_returns_zeros(self):
        result = run_manifest.parse_interview_file("/nonexistent/interview_answers.json")
        self.assertEqual(result, {"asked": 0, "answered": 0, "skipped": 0, "questions": []})

    def test_malformed_not_a_list_returns_zeros(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "interview_answers.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"not": "a list"}, f)
            result = run_manifest.parse_interview_file(path)
        self.assertEqual(result["asked"], 0)

    def test_entry_missing_required_keys_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "interview_answers.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump([{"id": "a", "status": "answered"}, {"question": "no id or status"}], f)
            result = run_manifest.parse_interview_file(path)
        self.assertEqual(result["asked"], 1)
        self.assertEqual(result["answered"], 1)

class CapacityPreflightTieInTest(unittest.TestCase):
    def test_all_six_real_keys_map_and_architect_sums(self):
        # Shaped exactly like capacity_preflight.py's own compute_preflight()
        # return value (confirmed via direct read of capacity_preflight.py).
        report = {
            "stage_fanout": {
                "stage1_file_summarizer": 3,
                "stage2_architect_segment": 3,
                "stage2_architect_merge": 1,
                "stage3_gap_analyzer": 1,
                "stage3_software_architect_and_testing": 1,
                "stage4_doc_writer": 14,
            },
            "total_fanout": 23,
        }
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "capacity_preflight_report.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f)
            result = run_manifest.compute_capacity_preflight_tie_in(path)

        self.assertEqual(result["total_predicted_fanout"], 23)
        self.assertEqual(result["unmapped_preflight_keys"], [])
        self.assertEqual(result["predicted_fanout_by_manifest_stage"], {
            "file_summarize": 3,
            "architect": 4,  # segment (3) + merge (1)
            "gap_analysis_interview": 1,
            "architecture_testing_review": 1,
            "doc_writer": 14,
        })

    def test_unknown_key_recorded_and_warns_not_silently_dropped(self):
        report = {"stage_fanout": {"stage5_future_stage": 7}, "total_fanout": 7}
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "capacity_preflight_report.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = run_manifest.compute_capacity_preflight_tie_in(path)

        self.assertEqual(result["unmapped_preflight_keys"], ["stage5_future_stage"])
        self.assertEqual(result["predicted_fanout_by_manifest_stage"], {})
        self.assertIn("stage5_future_stage", stderr.getvalue())
        self.assertIn("no known mapping", stderr.getvalue())

class CLIRoundTripTest(unittest.TestCase):
    """Drives the actual script as a subprocess, since this is the surface
    SKILL.md's orchestrating thread actually calls — a pure-function test
    alone wouldn't catch an argparse wiring mistake."""

    def _run(self, *args):
        result = subprocess.run(
            [*RUN_MANIFEST_CMD, *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")
        return result

    def test_full_lifecycle_via_cli(self):
        with tempfile.TemporaryDirectory() as d:
            manifest_path = os.path.join(d, "run_manifest.json")
            signals_path = os.path.join(d, "spring_signals.json")
            with open(signals_path, "w", encoding="utf-8") as f:
                json.dump({"file_signatures": {"Foo.java": "sha256:abc"}}, f)

            self._run("init", FIXTURE_DIR, "--out", manifest_path, "--now-ms", "1000")
            self._run("start-stage", manifest_path, "signal_scan", "--now-ms", "1000")
            self._run("end-stage", manifest_path, "signal_scan", "--status", "complete", "--now-ms", "1500")
            self._run("start-stage", manifest_path, "partition", "--now-ms", "1500")
            self._run("end-stage", manifest_path, "partition", "--status", "complete", "--now-ms", "1800")
            self._run("finalize", manifest_path, "--signals-file", signals_path, "--now-ms", "2000")

            manifest = run_manifest._read_json(manifest_path)

        self.assertEqual(validate_manifest_shape(manifest), [])
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(len(manifest["stages"]), 2)
        self.assertEqual(manifest["stages"][0]["duration_ms"], 500)
        self.assertEqual(manifest["stages"][1]["duration_ms"], 300)
        self.assertEqual(manifest["file_signatures"], {"Foo.java": "sha256:abc"})

    def test_retry_case_via_cli(self):
        with tempfile.TemporaryDirectory() as d:
            manifest_path = os.path.join(d, "run_manifest.json")
            self._run("init", FIXTURE_DIR, "--out", manifest_path, "--now-ms", "0")
            self._run("start-stage", manifest_path, "doc_writer", "--now-ms", "0")
            self._run("end-stage", manifest_path, "doc_writer", "--status", "failed", "--now-ms", "100")
            self._run("start-stage", manifest_path, "doc_writer", "--now-ms", "200")
            self._run("end-stage", manifest_path, "doc_writer", "--status", "complete", "--now-ms", "500")
            manifest = run_manifest._read_json(manifest_path)

        stages = [s for s in manifest["stages"] if s["name"] == "doc_writer"]
        self.assertEqual(len(stages), 2)
        self.assertEqual(stages[0]["status"], "failed")
        self.assertEqual(stages[1]["status"], "complete")

    def test_partial_run_via_cli(self):
        with tempfile.TemporaryDirectory() as d:
            manifest_path = os.path.join(d, "run_manifest.json")
            self._run("init", FIXTURE_DIR, "--out", manifest_path, "--now-ms", "0")
            self._run("start-stage", manifest_path, "architect", "--now-ms", "0")
            # Deliberately no end-stage call — simulates a crashed session.
            self._run("finalize", manifest_path, "--now-ms", "500")
            manifest = run_manifest._read_json(manifest_path)

        self.assertEqual(manifest["status"], "partial")
        self.assertEqual(manifest["stages"][0]["status"], "canceled")
