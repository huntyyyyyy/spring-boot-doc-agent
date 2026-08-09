"""Cohesive suite from tests/doc_engine/test_spring_drift_check.py: JpqlLineageProvenanceTest."""

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

class JpqlLineageProvenanceTest(unittest.TestCase):
    """Unit-level tests against _raw_query_entries_with_resolved_entity()
    and _reverify_jpql_lineage_provenance() directly, with synthetic
    signals/results dicts — no CodeQL scan, no tempdir. Each function has one
    job (find the citations with a second provenance input; re-verify that
    input for citations whose provenance file changed) and is tested in
    isolation from the real-repo integration scenarios in
    SpringDriftCheckTest above, which cover the same behavior end-to-end."""

    def _signals(self, resolved_via_entity="Invoice", available=True):
        # Match resolve_jpql_to_lineage shapes: available True carries tables +
        # resolved_via_entity; unavailable is reason-only (no entity key).
        lineage = (
            {"available": False, "reason": "out of scope for the bounded JPQL resolver"}
            if not available
            else {
                "available": True,
                "source_tables": ["billing_invoice"],
                "target_tables": [],
            }
        )
        if available and resolved_via_entity is not None:
            lineage["resolved_via_entity"] = resolved_via_entity
        return {
            "entity_table_map": {
                "Invoice": {"file": "src/main/java/com/example/billing/Invoice.java", "table": "billing_invoice", "table_name_source": "explicit"},
            },
            "evidence": {
                "raw_queries": [
                    {
                        "file": "src/main/java/com/example/billing/InvoiceRepository.java", "line": 9, "query_kind": "jpql",
                        "query": "SELECT i FROM Invoice i WHERE i.status = :status",
                        "lineage": lineage,
                    },
                    {
                        "file": "src/main/java/com/example/billing/InvoiceRepository.java", "line": 17, "query_kind": "native",
                        "query": "SELECT * FROM billing_invoice WHERE status = :status",
                        "lineage": {"available": True, "source_tables": ["billing_invoice"], "target_tables": []},
                    },
                ],
            },
        }

    # ---- _raw_query_entries_with_resolved_entity ----

    def test_finds_the_jpql_entry_with_resolved_via_entity(self):
        found = list(spring_drift_check._raw_query_entries_with_resolved_entity(self._signals()))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["query_kind"], "jpql")

    def test_skips_native_entries_with_no_resolved_via_entity(self):
        signals = self._signals()
        del signals["evidence"]["raw_queries"][0]  # keep only the native entry
        found = list(spring_drift_check._raw_query_entries_with_resolved_entity(signals))
        self.assertEqual(found, [])

    def test_skips_unavailable_jpql_lineage(self):
        # Real unavailable shape is reason-only (no resolved_via_entity).
        signals = self._signals(available=False)
        found = list(spring_drift_check._raw_query_entries_with_resolved_entity(signals))
        self.assertEqual(found, [])

    def test_skips_unavailable_even_with_stale_resolved_via_entity(self):
        # Discriminative: corrupt/hand-edited signals may keep a stale
        # resolved_via_entity while available is false. Pre-fix filter
        # keyed only on the entity key would still select it for reverify.
        signals = self._signals(available=False)
        signals["evidence"]["raw_queries"][0]["lineage"]["resolved_via_entity"] = "Invoice"
        found = list(spring_drift_check._raw_query_entries_with_resolved_entity(signals))
        self.assertEqual(found, [])

    def test_empty_signals_yields_nothing(self):
        found = list(spring_drift_check._raw_query_entries_with_resolved_entity({}))
        self.assertEqual(found, [])

    # ---- _reverify_jpql_lineage_provenance ----

    def _base_result(self, status=spring_drift_check.STATUS_UNCHANGED, tier=1):
        return {
            "source": "evidence.raw_queries", "file": "src/main/java/com/example/billing/InvoiceRepository.java", "line": 9,
            "rule_id": "raw_queries__query", "match": "@Query(", "status": status, "tier": tier,
        }

    def test_entity_missing_from_entity_table_map_skips_defensively(self):
        # Shouldn't happen in practice — resolve_jpql_to_lineage() only
        # sets resolved_via_entity when the entity WAS found in
        # entity_table_map at scan time — but signals is arbitrary input
        # (a hand-edited JSON, a future format this code doesn't know
        # about), so this must degrade rather than KeyError.
        signals = self._signals()
        del signals["entity_table_map"]["Invoice"]
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, signals, fresh_entity_tables={}, changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_UNCHANGED)

    def test_entity_file_not_changed_leaves_result_untouched(self):
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={},
            changed_set=set(), deleted_set=set(),  # src/main/java/com/example/billing/Invoice.java in neither set
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_UNCHANGED)
        self.assertEqual(results[0]["tier"], 1)

    def test_entity_file_changed_table_unchanged_confirms(self):
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "billing_invoice"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_CONFIRMED)
        self.assertEqual(results[0]["tier"], 2)

    def test_entity_file_changed_table_renamed_drifts_with_old_and_new_names(self):
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "invoices"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_DRIFTED)
        self.assertEqual(results[0]["tier"], 2)
        self.assertIn("billing_invoice", results[0]["detail"])
        self.assertIn("invoices", results[0]["detail"])

    def test_entity_no_longer_matched_drifts_conservatively(self):
        # persistence__entity re-run against the changed file found no
        # match for this class at all (fresh_entity_tables has no entry for
        # it) — can't confirm the lineage is still accurate, so this must
        # NOT be silently left at STATUS_UNCHANGED.
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={}, changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_DRIFTED)
        self.assertIn("no longer matches", results[0]["detail"])

    def test_does_not_override_a_result_with_its_own_more_specific_verdict(self):
        # The query's own file also changed and already produced a real
        # tier-2 verdict (DRIFTED, from a text mismatch) — the provenance
        # pass must leave it exactly alone, not overwrite with a different
        # DRIFTED detail about the entity.
        results = [self._base_result(status=spring_drift_check.STATUS_DRIFTED, tier=2)]
        results[0]["detail"] = "no fresh @Query match with the same query text and kind found in this file"
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "invoices"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_DRIFTED)
        self.assertIn("no fresh @Query match", results[0]["detail"])

    def test_confirmed_own_file_verdict_still_gets_entity_provenance_rechecked(self):
        # THE regression case (audit Claim 1): the query's OWN file changed
        # in a way that left its text intact, so _recheck_queries() already
        # marked it STATUS_CONFIRMED — but "text still present" says nothing
        # about whether the lineage is still accurate. If the entity's table
        # renamed in the same interval, this CONFIRMED verdict must be
        # UPGRADED to DRIFTED, not skipped. The pre-fix guard (skip unless
        # STATUS_UNCHANGED) let this exact case through as confirmed-but-stale.
        results = [self._base_result(status=spring_drift_check.STATUS_CONFIRMED, tier=2)]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "invoices"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_DRIFTED)
        self.assertEqual(results[0]["tier"], 2)
        self.assertIn("billing_invoice", results[0]["detail"])
        self.assertIn("invoices", results[0]["detail"])

    def test_confirmed_own_file_verdict_with_unchanged_table_stays_confirmed(self):
        # The companion no-false-positive check for the case above: a
        # CONFIRMED query whose entity file changed but whose table mapping
        # did NOT must stay CONFIRMED — the upgrade fires on an actual table
        # change, not merely on the entity file being touched.
        results = [self._base_result(status=spring_drift_check.STATUS_CONFIRMED, tier=2)]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "billing_invoice"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_CONFIRMED)

    def test_deleted_entity_file_drifts_dependent_jpql_with_delete_specific_detail(self):
        # audit finding #2: the entity's file was DELETED (not just changed),
        # so it never got tier-2 rechecked and never appears in
        # fresh_entity_tables. The gate must still fire (via deleted_set), and
        # the fresh-is-None branch must report DRIFTED with a delete-specific
        # detail, not the "no longer matches in its file" wording that reads
        # wrong for a file that no longer exists.
        results = [self._base_result()]
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={},
            changed_set=set(), deleted_set={"src/main/java/com/example/billing/Invoice.java"},
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_DRIFTED)
        self.assertEqual(results[0]["tier"], 2)
        self.assertIn("deleted", results[0]["detail"])
        self.assertIn("src/main/java/com/example/billing/Invoice.java", results[0]["detail"])

    def test_no_matching_result_entry_does_not_crash(self):
        # Defensive: a citation with resolved_via_entity but no
        # corresponding (file, line) in results shouldn't happen in
        # practice (every citation gets exactly one result), but this pass
        # runs after the main loop on a separate data structure, so it must
        # degrade safely rather than KeyError if the two ever disagree.
        results = []
        spring_drift_check._reverify_jpql_lineage_provenance(
            results, self._signals(), fresh_entity_tables={"Invoice": {"table": "invoices"}},
            changed_set={"src/main/java/com/example/billing/Invoice.java"}, deleted_set=set(),
        )
        self.assertEqual(results, [])
