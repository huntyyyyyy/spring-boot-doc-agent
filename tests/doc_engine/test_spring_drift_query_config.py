"""Cohesive suite from tests/doc_engine/test_spring_drift_check.py: SpringDriftQueryConfigTest."""

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

class SpringDriftQueryConfigTest(unittest.TestCase):
    @classmethod
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

    def test_repository_type_args_change_is_drift(self):
            _edit(
                os.path.join(self.repo, "src/main/java/com/example/billing/InvoiceRepository.java"),
                "JpaRepository<Invoice, Long>",
                "JpaRepository<Invoice, String>",
            )
            report = self._drift()
            citation = next(
                r for r in report["results"]
                if r["file"] == "src/main/java/com/example/billing/InvoiceRepository.java" and r["rule_id"] == "persistence__repository"
            )
            self.assertEqual(citation["status"], spring_drift_check.STATUS_DRIFTED)

    def test_single_mapping_change_does_not_flag_sibling_citations(self):
            _edit(
                os.path.join(self.repo, "src/main/java/com/example/billing/InvoiceController.java"),
                "@PostMapping\n    public String createInvoice()",
                '@PostMapping("/new")\n    public String createInvoice()',
            )
            report = self._drift()

            # The @PostMapping citation (originally bare) is the one that changed shape.
            drifted = [r for r in report["results"]
                       if r["file"] == "src/main/java/com/example/billing/InvoiceController.java" and r["status"] == spring_drift_check.STATUS_DRIFTED]
            self.assertEqual(len(drifted), 1)
            self.assertEqual(drifted[0]["match"], "@PostMapping")

            # Everything else in the same file must still confirm: @RestController,
            # @RequestMapping, @GetMapping, @PreAuthorize (api_surface/security),
            # plus the package declaration and two imports (references) — 7 total.
            confirmed = [r for r in report["results"]
                         if r["file"] == "src/main/java/com/example/billing/InvoiceController.java" and r["status"] == spring_drift_check.STATUS_CONFIRMED]
            self.assertEqual(len(confirmed), 7)

    def test_query_text_change_is_drift(self):
            # src/main/java/com/example/billing/InvoiceRepository.java carries two @Query citations (one jpql, one
            # native) — edit only the jpql one's string and confirm just that
            # citation drifts while its sibling (unedited) still confirms. The
            # `match` field always reflects the *original* stored text (drift_result
            # never overwrites it with the fresh match), so both citations are
            # still distinguishable after the edit by their original wording.
            _edit(
                os.path.join(self.repo, "src/main/java/com/example/billing/InvoiceRepository.java"),
                "SELECT i FROM Invoice i WHERE i.status = :status",
                "SELECT i FROM Invoice i WHERE i.status = :status AND i.archived = false",
            )
            report = self._drift()
            query_citations = [
                r for r in report["results"]
                if r["file"] == "src/main/java/com/example/billing/InvoiceRepository.java" and r["rule_id"] == "raw_queries__query"
            ]
            self.assertEqual(len(query_citations), 2)

            jpql_citation = next(r for r in query_citations if "i.status" in (r.get("match") or ""))
            native_citation = next(r for r in query_citations if "i.status" not in (r.get("match") or ""))
            self.assertEqual(jpql_citation["status"], spring_drift_check.STATUS_DRIFTED)
            self.assertEqual(native_citation["status"], spring_drift_check.STATUS_CONFIRMED)

    def test_deleted_file_flags_every_citation_as_file_deleted(self):
            os.remove(os.path.join(self.repo, "src/main/java/com/example/billing/Misc.java"))
            report = self._drift()
            self.assertIn("src/main/java/com/example/billing/Misc.java", report["file_summary"]["deleted"])
            misc_results = [r for r in report["results"] if r["file"] == "src/main/java/com/example/billing/Misc.java"]
            self.assertTrue(misc_results, "src/main/java/com/example/billing/Misc.java had evidence in the baseline; expected citations in the report")
            self.assertTrue(all(r["status"] == spring_drift_check.STATUS_FILE_DELETED for r in misc_results))

    def test_new_file_is_informational_only(self):
            with open(os.path.join(self.repo, "NewThing.java"), "w") as f:
                f.write("package com.example.billing;\n\npublic class NewThing {\n}\n")
            report = self._drift()
            self.assertIn("NewThing.java", report["file_summary"]["added"])
            self.assertFalse(any(r["file"] == "NewThing.java" for r in report["results"]))

    def test_filename_based_evidence_falls_back_to_tier1_only(self):
            with open(os.path.join(self.repo, "db", "migration", "V1__init.sql"), "a") as f:
                f.write("\n-- an appended, unrelated comment\n")
            report = self._drift()
            citation = next(r for r in report["results"] if r["file"] == "db/migration/V1__init.sql")
            self.assertIsNone(citation["rule_id"])
            self.assertEqual(citation["status"], spring_drift_check.STATUS_NO_RULE_FALLBACK)
            self.assertEqual(citation["tier"], 1)

    def test_config_value_changed_under_unchanged_key_is_flagged_for_review(self):
            _edit(os.path.join(self.repo, "application-local.yml"), "port: 8080", "port: 9090")
            report = self._drift()
            citation = next(r for r in report["results"] if r["file"] == "application-local.yml")
            self.assertEqual(citation["status"], spring_drift_check.STATUS_CONFIG_VALUES_ONLY_CHANGED)
            self.assertEqual(citation["tier"], 1)

    def test_config_key_added_is_structural_not_flagged_for_review(self):
            with open(os.path.join(self.repo, "application-local.yml"), "a") as f:
                f.write("  extra-new-key: added\n")
            report = self._drift()
            citation = next(r for r in report["results"] if r["file"] == "application-local.yml")
            self.assertEqual(citation["status"], spring_drift_check.STATUS_CONFIG_STRUCTURE_CHANGED)
            self.assertIn("extra-new-key", citation["detail"])

    def test_stale_schema_version_is_rejected_not_crashed(self):
            stale = dict(self.baseline)
            del stale["schema_version"]
            del stale["file_signatures"]
            stale_path = os.path.join(os.path.dirname(self.repo), "stale_signals.json")
            with open(stale_path, "w") as f:
                json.dump(stale, f)
            with self.assertRaises(SystemExit):
                spring_drift_check.load_signals(stale_path)

    def test_citation_with_no_prior_signature_is_unknown_not_guessed(self):
            baseline_missing_sig = json.loads(json.dumps(self.baseline))  # deep copy
            baseline_missing_sig["file_signatures"].pop("Dockerfile", None)
            report = spring_drift_check.check_drift(self.repo, baseline_missing_sig)
            citation = next(r for r in report["results"] if r["file"] == "Dockerfile")
            self.assertEqual(citation["status"], spring_drift_check.STATUS_UNKNOWN_NO_SIGNATURE)
