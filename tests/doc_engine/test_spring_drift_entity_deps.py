"""Spring drift dependent JPQL lineage cases."""

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
SCRIPT_DIR = SCRIPTS_DIR
FIXTURE_JAVA_PREFIX = "src/main/java/com/example/billing/"
DRIFT_CHECK_CMD = [sys.executable, "-m", "doc_engine.tools.spring_drift_check"]
FAST_MODE = os.environ.get("SPRING_DRIFT_FAST_MODE", "").lower() in ("1", "true", "yes")
from tests.support.spring_drift.scratch import _by_source, _edit, _fixture_build_command, _make_scratch_copy

class SpringDriftEntityLineageTestContinued(unittest.TestCase):
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

    def test_entity_table_rename_drifts_dependent_jpql_citation_even_though_query_file_is_untouched(self):
                # src/main/java/com/example/billing/InvoiceRepository.java's JPQL query resolves its lineage through
                # src/main/java/com/example/billing/Invoice.java's entity mapping. If src/main/java/com/example/billing/Invoice.java's @Table renames,
                # src/main/java/com/example/billing/InvoiceRepository.java itself never changes — tier 1 alone would
                # call its JPQL citation unchanged even though the lineage it
                # carries is now stale.
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/Invoice.java"),
                    '@Table(name = "billing_invoice")',
                    '@Table(name = "invoices")',
                )
                report = self._drift()

                entity_citation = _by_source(report, "entity_table_map.Invoice")
                self.assertEqual(entity_citation["status"], spring_drift_check.STATUS_DRIFTED)

                jpql_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "jpql")
                self.assertEqual(jpql_result["status"], spring_drift_check.STATUS_DRIFTED)
                self.assertEqual(jpql_result["tier"], 2)
                self.assertIn("Invoice", jpql_result["detail"])
                self.assertIn("billing_invoice", jpql_result["detail"])
                self.assertIn("invoices", jpql_result["detail"])

                # The native query's lineage was extracted directly from real SQL
                # text, no entity_table_map dependency at all — it must NOT be
                # swept up just because a sibling citation in the same file was.
                native_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "native")
                self.assertEqual(native_result["status"], spring_drift_check.STATUS_UNCHANGED)

    def test_entity_file_changed_but_table_mapping_unchanged_confirms_jpql_lineage(self):
                # The core false-positive this whole tool exists to avoid, applied
                # to the new provenance check: src/main/java/com/example/billing/Invoice.java's hash changes (an
                # unrelated comment), but @Table itself doesn't move, so the JPQL
                # lineage resolved through it is still accurate. Must read as
                # CONFIRMED (tier 2 — actually re-verified), not left at the tier-1
                # STATUS_UNCHANGED default (which would mean "never actually
                # checked"), and definitely not DRIFTED.
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/Invoice.java"),
                    "private Long id;",
                    "private Long id; // unrelated comment, nothing structural changed",
                )
                report = self._drift()

                jpql_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "jpql")
                self.assertEqual(jpql_result["status"], spring_drift_check.STATUS_CONFIRMED)
                self.assertEqual(jpql_result["tier"], 2)

    def test_dependent_status_does_not_override_a_citation_with_its_own_real_tier2_result(self):
                # If the query's own file ALSO changed, tier 2 already produced a
                # real, more specific verdict for it (a genuine text mismatch) — the
                # provenance re-check must not clobber that with a different DRIFTED
                # detail about the entity instead.
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/Invoice.java"),
                    '@Table(name = "billing_invoice")',
                    '@Table(name = "invoices")',
                )
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/InvoiceRepository.java"),
                    "SELECT i FROM Invoice i WHERE i.status = :status",
                    "SELECT i FROM Invoice i WHERE i.status = :status AND i.archived = false",
                )
                report = self._drift()

                jpql_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "jpql")
                self.assertEqual(jpql_result["status"], spring_drift_check.STATUS_DRIFTED)
                self.assertIn("no fresh @Query match", jpql_result["detail"])

    def test_entity_table_rename_drifts_jpql_even_when_query_file_also_changed_but_text_intact(self):
                # audit Claim 1, end-to-end: both src/main/java/com/example/billing/Invoice.java (table rename) AND
                # src/main/java/com/example/billing/InvoiceRepository.java change in the same interval, but the JPQL
                # query STRING is untouched — so its own-file tier-2 recheck yields
                # CONFIRMED (text still present). The provenance pass must still
                # upgrade it to DRIFTED because the entity's table moved; the
                # pre-fix guard (skip anything not STATUS_UNCHANGED) reported this as
                # confirmed_still_present over now-stale lineage.
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/Invoice.java"),
                    '@Table(name = "billing_invoice")',
                    '@Table(name = "invoices")',
                )
                _edit(
                    os.path.join(self.repo, "src/main/java/com/example/billing/InvoiceRepository.java"),
                    "Invoice findByStatus(String status);",
                    "Invoice findByStatus(String status); // unrelated non-query edit",
                )
                report = self._drift()

                # Guard: the query file really did change (so its own-file verdict is
                # tier-2 CONFIRMED, not tier-1 UNCHANGED) — otherwise this test would
                # silently reduce to the already-covered query-file-untouched case.
                self.assertIn("src/main/java/com/example/billing/InvoiceRepository.java", report["file_summary"]["changed"])

                jpql_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "jpql")
                self.assertEqual(jpql_result["status"], spring_drift_check.STATUS_DRIFTED)
                self.assertEqual(jpql_result["tier"], 2)
                self.assertIn("billing_invoice", jpql_result["detail"])
                self.assertIn("invoices", jpql_result["detail"])

    def test_deleting_entity_file_drifts_dependent_jpql_citation(self):
                # audit finding #2, end-to-end: src/main/java/com/example/billing/Invoice.java is deleted while
                # src/main/java/com/example/billing/InvoiceRepository.java is untouched. The JPQL citation's second
                # provenance input is gone, so it must read DRIFTED (with a
                # delete-specific detail), not the tier-1 STATUS_UNCHANGED its own
                # untouched file would otherwise leave it at.
                os.remove(os.path.join(self.repo, "src/main/java/com/example/billing/Invoice.java"))
                report = self._drift()
                self.assertIn("src/main/java/com/example/billing/Invoice.java", report["file_summary"]["deleted"])

                jpql_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "jpql")
                self.assertEqual(jpql_result["status"], spring_drift_check.STATUS_DRIFTED)
                self.assertEqual(jpql_result["tier"], 2)
                self.assertIn("deleted", jpql_result["detail"])

                # The native query in the same file has no entity_table_map dependency,
                # so deleting src/main/java/com/example/billing/Invoice.java must not sweep it up.
                native_result = self._raw_query_result(report, "src/main/java/com/example/billing/InvoiceRepository.java", "native")
                self.assertEqual(native_result["status"], spring_drift_check.STATUS_UNCHANGED)
