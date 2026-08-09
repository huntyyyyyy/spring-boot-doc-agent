"""Cohesive suite from tests/doc_engine/test_spring_drift_check.py: SpringDriftManifestCliTest."""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import spring_drift_check, spring_signal_scan

import pytest

pytestmark = pytest.mark.domain_stage0

SCRIPT_DIR = SCRIPTS_DIR
FIXTURE_JAVA_PREFIX = "src/main/java/com/example/billing/"
DRIFT_CHECK_CMD = [sys.executable, "-m", "doc_engine.tools.spring_drift_check"]
FAST_MODE = os.environ.get("SPRING_DRIFT_FAST_MODE", "").lower() in ("1", "true", "yes")
from tests.support.spring_drift.scratch import _by_source, _edit, _fixture_build_command, _make_scratch_copy

class SpringDriftManifestCliTest(unittest.TestCase):
    def setUpClass(cls):
            # One baseline scan of the committed fixture, reused by every test.
            # Each test still gets its own scratch copy to mutate in isolation.
            cls._baseline_signals = spring_signal_scan.scan(
                FIXTURE_DIR,
                build_command=_fixture_build_command(),
                scanners=["filesystem", "ast-grep"],
            )

    def setUp(self):
            self.repo = _make_scratch_copy()
            self.baseline = copy.deepcopy(self._baseline_signals)
            self.baseline["repo_path"] = self.repo
            # Sanity: every test depends on the baseline carrying the
            # drift-detection fields introduced in schema_version 2
            # (file_signatures, rule_id) — not on the exact version number,
            # which moves independently of this file for unrelated reasons
            # (e.g. the SQL lineage field added in schema_version 3). Asserting
            # ">=" rather than "==" here means the next unrelated version bump
            # won't break this whole suite the way this one did. If this ever
            # fails, it means spring_signal_scan.py regressed, not
            # spring_drift_check.py.
            self.assertGreaterEqual(self.baseline["schema_version"], 2)
            self.assertIn("file_signatures", self.baseline)

    def tearDown(self):
            shutil.rmtree(os.path.dirname(self.repo), ignore_errors=True)

    def _drift(self):
            return spring_drift_check.check_drift(self.repo, self.baseline)

    def _raw_query_result(self, report, file_rel, query_kind):
            """Look up a raw_queries__query drift result by (file, query_kind),
            via the baseline's own line number — drift_result() doesn't carry
            query_kind/query text, only file/line/match, and src/main/java/com/example/billing/InvoiceRepository.java
            has both a jpql and a native citation whose `match` text is
            indistinguishable (both start "@Query(")."""
            baseline_entry = next(
                e for e in self.baseline["evidence"]["raw_queries"]
                if e["file"] == file_rel and e["query_kind"] == query_kind
            )
            return next(
                r for r in report["results"]
                if r["file"] == file_rel and r["line"] == baseline_entry["line"]
            )

    def test_no_manifest_baseline_source_is_spring_signals(self):
            report = self._drift()
            self.assertEqual(report["file_signatures_baseline"], {"source": "spring_signals.json"})

    def test_manifest_baseline_used_for_tier1_instead_of_signals(self):
            # A manifest whose file_signatures already reflects the edit below
            # (i.e. it was "taken after" the edit) must see the file as
            # unchanged even though spring_signals.json's own baseline predates
            # the edit and would otherwise flag it.
            _edit(
                os.path.join(self.repo, "src/main/java/com/example/billing/LegacyAudit.java"),
                "@Entity\npublic class LegacyAudit {",
                '@Entity\n@Table(name = "legacy_audit_v2")\npublic class LegacyAudit {',
            )
            post_edit_scan = spring_signal_scan.scan(self.repo, scanners=["filesystem", "ast-grep"])
            manifest = {
                "run_id": "2026-07-25T00:00:00Z-deadbeef",
                "target_repo": {"path": self.repo, "commit_hash": "deadbeef", "dirty": False},
                "file_signatures": post_edit_scan["file_signatures"],
            }

            report = spring_drift_check.check_drift(self.repo, self.baseline, manifest=manifest)

            self.assertNotIn("src/main/java/com/example/billing/LegacyAudit.java", report["file_summary"]["changed"])
            self.assertEqual(
                report["file_signatures_baseline"],
                {"source": "run_manifest.json", "run_id": "2026-07-25T00:00:00Z-deadbeef",
                 "repo_path": self.repo, "commit_hash": "deadbeef", "dirty": False},
            )

    def test_manifest_still_requires_signals_for_tier2_evidence(self):
            # Even with a manifest supplying the tier-1 baseline, tier-2 citation
            # content (entity/table mapping etc.) must still come from signals —
            # a manifest alone has no evidence/entity_table_map to check against.
            manifest = {
                "run_id": "x", "target_repo": {"commit_hash": None, "dirty": None},
                "file_signatures": self.baseline["file_signatures"],
            }
            report = spring_drift_check.check_drift(self.repo, self.baseline, manifest=manifest)
            entity_citation = _by_source(report, "entity_table_map.LegacyAudit")
            self.assertIsNotNone(entity_citation, "tier-2 citations must still come from signals, manifest or no manifest")

    def test_load_manifest_rejects_file_with_no_file_signatures(self):
            with tempfile.TemporaryDirectory() as d:
                bad_path = os.path.join(d, "bad_manifest.json")
                with open(bad_path, "w") as f:
                    json.dump({"run_id": "x"}, f)
                with self.assertRaises(SystemExit):
                    spring_drift_check.load_manifest(bad_path)

    def test_load_manifest_rejects_still_running_manifest(self):
            # build_init_manifest()'s status stays "running" until finalize is
            # ever called at all -- a manifest at that point always has an empty
            # file_signatures placeholder and must not be usable as a baseline.
            with tempfile.TemporaryDirectory() as d:
                path = os.path.join(d, "run_manifest.json")
                with open(path, "w") as f:
                    json.dump({
                        "run_id": "x", "status": "running",
                        "target_repo": {"commit_hash": "abc", "dirty": False},
                        "file_signatures": {},
                    }, f)
                with self.assertRaises(SystemExit):
                    spring_drift_check.load_manifest(path)

    def test_load_manifest_rejects_finalized_manifest_with_empty_file_signatures(self):
            # finalize_manifest() only overwrites file_signatures if it was
            # actually given some (e.g. no --signals-file and no repo to
            # re-hash) -- a "complete" manifest can still have an empty map.
            # No target_repo.path here, so there's nothing to re-check against --
            # must be treated as the broken-finalize case, not the empty-repo one.
            with tempfile.TemporaryDirectory() as d:
                path = os.path.join(d, "run_manifest.json")
                with open(path, "w") as f:
                    json.dump({
                        "run_id": "x", "status": "complete",
                        "target_repo": {"commit_hash": "abc", "dirty": False},
                        "file_signatures": {},
                    }, f)
                with self.assertRaises(SystemExit):
                    spring_drift_check.load_manifest(path)

    def test_load_manifest_accepts_empty_file_signatures_for_a_genuinely_empty_repo(self):
            # An empty file_signatures map isn't always the broken-finalize case --
            # a repo with zero trackable files at scan time finalizes with an
            # empty map too, and "everything is newly added" is the correct
            # report for that, not a misreport. target_repo.path is re-walked
            # live to tell the two cases apart.
            with tempfile.TemporaryDirectory() as empty_repo:
                with tempfile.TemporaryDirectory() as d:
                    path = os.path.join(d, "run_manifest.json")
                    with open(path, "w") as f:
                        json.dump({
                            "run_id": "x", "status": "complete",
                            "target_repo": {"path": empty_repo, "commit_hash": "abc", "dirty": False},
                            "file_signatures": {},
                        }, f)
                    data = spring_drift_check.load_manifest(path)
                    self.assertEqual(data["file_signatures"], {})

    def test_cli_accepts_manifest_flag_and_reports_its_source(self):
            with tempfile.TemporaryDirectory() as d:
                signals_path = os.path.join(d, "spring_signals.json")
                with open(signals_path, "w") as f:
                    json.dump(self.baseline, f)
                manifest_path = os.path.join(d, "run_manifest.json")
                with open(manifest_path, "w") as f:
                    json.dump({
                        "run_id": "cli-test", "target_repo": {"commit_hash": "cafef00d", "dirty": True},
                        "file_signatures": self.baseline["file_signatures"],
                    }, f)
                out_path = os.path.join(d, "drift_report.json")

                result = subprocess.run(
                    [*DRIFT_CHECK_CMD, self.repo, signals_path,
                     "--manifest", manifest_path, "--out", out_path],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("run_manifest.json", result.stdout)

                with open(out_path) as f:
                    report = json.load(f)
                self.assertEqual(report["file_signatures_baseline"]["source"], "run_manifest.json")
                self.assertEqual(report["file_signatures_baseline"]["run_id"], "cli-test")
