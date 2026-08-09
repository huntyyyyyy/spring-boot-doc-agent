"""Spring drift entity/table core cases."""

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

class SpringDriftEntityLineageTest(unittest.TestCase):
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

    def test_no_changes_everything_unchanged(self):
                report = self._drift()
                self.assertEqual(report["file_summary"]["changed"], [])
                self.assertEqual(report["file_summary"]["deleted"], [])
                self.assertEqual(report["file_summary"]["added"], [])
                statuses = {r["status"] for r in report["results"]}
                self.assertEqual(statuses, {spring_drift_check.STATUS_UNCHANGED})

    def test_unrelated_comment_edit_does_not_drift_the_entity_citation(self):
                # This is the exact scenario from the design brief: a comment fix
                # nowhere near the cited annotation must not read as drift.
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/SLARule.java"),
                    "private Long id;",
                    "private Long id; // unrelated comment, nothing structural changed",
                )
                report = self._drift()
                self.assertIn("src/main/java/com/example/billing/SLARule.java", report["file_summary"]["changed"])

                entity_citation = _by_source(report, "entity_table_map.SLARule")
                bucket_citation = next(
                    r for r in report["results"]
                    if r["file"] == "src/main/java/com/example/billing/SLARule.java" and r["source"] == "evidence.persistence"
                )
                self.assertEqual(entity_citation["status"], spring_drift_check.STATUS_CONFIRMED)
                self.assertEqual(entity_citation["tier"], 2)
                self.assertEqual(bucket_citation["status"], spring_drift_check.STATUS_CONFIRMED)

    def test_table_mapping_change_is_drift_but_existence_entry_is_not(self):
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/LegacyAudit.java"),
                    "@Entity\npublic class LegacyAudit {",
                    '@Entity\n@Table(name = "legacy_audit_v2")\npublic class LegacyAudit {',
                )
                report = self._drift()

                entity_citation = _by_source(report, "entity_table_map.LegacyAudit")
                self.assertEqual(entity_citation["status"], spring_drift_check.STATUS_DRIFTED)
                self.assertIn("legacy_audit", entity_citation["detail"])
                self.assertIn("legacy_audit_v2", entity_citation["detail"])

                # The parallel persistence-bucket entry only claims "this class is
                # still @Entity-annotated" — which remains true — so it must NOT
                # drift just because the table mapping did.
                bucket_citation = next(
                    r for r in report["results"]
                    if r["file"] == "src/main/java/com/example/billing/LegacyAudit.java" and r["source"] == "evidence.persistence"
                )
                self.assertEqual(bucket_citation["status"], spring_drift_check.STATUS_CONFIRMED)

    def test_entity_class_removed_entirely_is_drift(self):
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/LegacyAudit.java"),
                    "@Entity\npublic class LegacyAudit {",
                    "public class LegacyAudit {",  # @Entity annotation removed
                )
                report = self._drift()
                entity_citation = _by_source(report, "entity_table_map.LegacyAudit")
                self.assertEqual(entity_citation["status"], spring_drift_check.STATUS_DRIFTED)
                bucket_citation = next(
                    r for r in report["results"]
                    if r["file"] == "src/main/java/com/example/billing/LegacyAudit.java" and r["source"] == "evidence.persistence"
                )
                self.assertEqual(bucket_citation["status"], spring_drift_check.STATUS_DRIFTED)
