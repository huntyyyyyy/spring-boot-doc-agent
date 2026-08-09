"""Spring signal scan core fixture corpus assertions."""

from __future__ import annotations

import json
import os
import unittest

import pytest

from doc_engine.tools import spring_signal_scan
from tests.conftest import FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH, SCRIPTS_DIR

pytestmark = pytest.mark.domain_stage0

SCRIPT_DIR = SCRIPTS_DIR
USE_SNAPSHOT = os.environ.get("SPRING_SIGNAL_USE_SNAPSHOT", "").lower() in ("1", "true", "yes")
SNAPSHOT_SCANNERS = ["filesystem", "ast-grep"]

class SpringSignalScanTest(unittest.TestCase):
    @classmethod
    def _load_fixture_snapshot(cls):
        with open(FIXTURE_SNAPSHOT_PATH, encoding="utf-8") as f:
            snapshot = json.load(f)
        current_version = spring_signal_scan._scanner_version(SNAPSHOT_SCANNERS)
        if snapshot.get("scanner_version") != current_version:
            raise RuntimeError(
                f"fixture snapshot is stale: expected scanner_version={current_version}, "
                f"got {snapshot.get('scanner_version')}. Regenerate with:\n"
                f"  python3 scripts/fixtures/regenerate_fixture_snapshot.py --scanners filesystem,ast-grep"
            )
        return snapshot

    @classmethod
    def setUpClass(cls):
        if USE_SNAPSHOT:
            cls.result = cls._load_fixture_snapshot()
        else:
            cls.result = spring_signal_scan.scan(str(FIXTURE_DIR), scanners=SNAPSHOT_SCANNERS)
        cls.evidence = cls.result["evidence"]

    def _entries_for(self, bucket, filename):
        # Evidence file paths are relative to the repo root. Allow callers to
        # keep using the short basename for readability.
        return [e for e in self.evidence[bucket]
                if e["file"] == filename or os.path.basename(e["file"]) == filename]

    # ---- filename-based detection (unchanged from the regex-era scanner) ----

    def test_file_counts(self):
        fs = self.result["files_scanned"]
        self.assertEqual(fs["java"], 17, "target/generated-sources/ShouldBeExcluded.java must not be counted")
        self.assertEqual(fs["config"], 3)
        self.assertEqual(fs["deployment"], 3)
        self.assertEqual(fs["other_relevant"], 2)  # logback-spring.xml + db/migration/V1__init.sql

    def test_excluded_dirs_are_not_scanned(self):
        all_files = {e["file"] for entries in self.evidence.values() for e in entries}
        all_files |= set(self.result["entity_table_map"][k]["file"] for k in self.result["entity_table_map"])
        self.assertFalse(any("target" in f for f in all_files), "files under target/ leaked into evidence")

    def test_config_and_deployment_and_logging_and_migration(self):
        self.assertEqual(len(self._entries_for("configuration", "application-local.yml")), 1)
        self.assertEqual(len(self._entries_for("configuration", "bootstrap.yml")), 1)
        self.assertEqual(len(self._entries_for("deployment", "Dockerfile")), 1)
        self.assertEqual(len(self._entries_for("observability", "logback-spring.xml")), 1)
        self.assertEqual(len(self._entries_for("persistence", "db/migration/V1__init.sql")), 1)

    # ---- entity / table detection ----

    def test_entity_with_explicit_table(self):
        m = self.result["entity_table_map"]["Invoice"]
        self.assertEqual(m["table"], "billing_invoice")
        self.assertEqual(m["table_name_source"], "explicit")

    def test_entity_with_inferred_table(self):
        m = self.result["entity_table_map"]["LegacyAudit"]
        self.assertEqual(m["table"], "legacy_audit")
        self.assertEqual(m["table_name_source"], "inferred-default-naming")

    def test_acronym_bearing_entity_matches_real_hibernate_default(self):
        # Regression guard for the to_snake_case bug flagged (and deferred)
        # across every prior round: the old implementation inserted an
        # underscore before every capital letter, turning SLARule into
        # s_l_a_rule. The real Spring/Hibernate default naming strategy
        # produces "slarule" instead — see to_snake_case's docstring for the
        # verified source. This is deliberately NOT "sla_rule": that's the
        # "nicer" guess a naive acronym-aware fix would produce, and it's
        # just as wrong for this function's purpose as the old bug was.
        m = self.result["entity_table_map"]["SLARule"]
        self.assertEqual(m["table"], "slarule")
        self.assertEqual(m["table_name_source"], "inferred-default-naming")

    def test_entity_survives_stacked_annotations(self):
        # Regression guard: @Entity/@Table with @EntityListeners/@Cacheable
        # also present used to break a literal (non-relational) ast-grep
        # pattern entirely. See PaymentLedger.java.
        m = self.result["entity_table_map"]["PaymentLedger"]
        self.assertEqual(m["table"], "payment_ledger")
        self.assertEqual(m["table_name_source"], "explicit")

    def test_entityscan_is_not_a_false_positive_entity(self):
        # Regression guard for a REAL bug found by running the old scanner
        # against a production codebase's Application.java: it did
        # `"@Entity" in text`, a substring check that also matched
        # "@EntityScan(...)". Misc.java carries @EntityScan on a non-entity
        # class specifically to guard against that recurring.
        self.assertNotIn("SecurityConfig", self.result["entity_table_map"])

    def test_three_real_entities_and_no_more(self):
        # NOTE: SLARule.java is deliberately excluded from this count — it's
        # a dedicated fixture for test_acronym_bearing_entity_matches_real_
        # hibernate_default above and would make this assertion's name a lie.
        # It's still covered by test_excluded_dirs_are_not_scanned's file
        # sweep and by its own dedicated test.
        entities = set(self.result["entity_table_map"].keys()) - {"SLARule"}
        self.assertEqual(entities, {"Invoice", "LegacyAudit", "PaymentLedger"})

    # ---- repository detection ----

    def test_plain_repository(self):
        entries = self._entries_for("persistence", "InvoiceRepository.java")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["repository"], "InvoiceRepository")
        self.assertEqual(entries[0]["entity"], "Invoice")
        self.assertEqual(entries[0]["id_type"], "Long")

    def test_repository_survives_leading_annotation(self):
        # Regression guard: same annotation-adjacency issue as entities, for
        # "public interface $N extends JpaRepository<...> {$$$}". Most real
        # repository interfaces carry @Repository, which used to break this.
        entries = self._entries_for("persistence", "AnnotatedRepository.java")
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["repository"], "AnnotatedRepository")

    def test_non_repository_interface_is_not_matched(self):
        # Negative case: NotARepository.java sits in the same conceptual
        # role but extends nothing Spring-Data-shaped. Zero matches expected
        # — detection is structural, not filename/directory based.
        self.assertEqual(len(self._entries_for("persistence", "NotARepository.java")), 0)

    # ---- raw queries: jpql vs native, argument-order independence ----

    def test_jpql_query_extracted(self):
        entries = self._entries_for("raw_queries", "InvoiceRepository.java")
        jpql = [e for e in entries if e["query_kind"] == "jpql"]
        self.assertEqual(len(jpql), 1)
        self.assertEqual(jpql[0]["query"], "SELECT i FROM Invoice i WHERE i.status = :status")

    def test_native_query_extracted_regardless_of_argument_order(self):
        # nativeQuery=true appears AFTER the query string here — a fixed
        # this-line-or-next-line heuristic or an argument-order-sensitive
        # pattern both got this right only by accident.
        entries = self._entries_for("raw_queries", "InvoiceRepository.java")
        native = [e for e in entries if e["query_kind"] == "native"]
        self.assertEqual(len(native), 1)
        self.assertEqual(native[0]["query"], "SELECT * FROM billing_invoice WHERE status = :status")

    # ---- native-query SQL lineage (sqllineage integration) ----

    def test_native_query_lineage_extracts_source_table(self):
        # This is the real integration path: scan() -> extract_sql_lineage()
        # -> the actual sqllineage library, against the fixture's real
        # native query text (":status" named parameter and all).
        entries = self._entries_for("raw_queries", "InvoiceRepository.java")
        native = next(e for e in entries if e["query_kind"] == "native")
        self.assertIn("lineage", native)
        self.assertTrue(native["lineage"]["available"], native["lineage"].get("reason"))
        self.assertEqual(native["lineage"]["source_tables"], ["billing_invoice"])
        self.assertEqual(native["lineage"]["target_tables"], [])

    def test_jpql_query_resolves_lineage_via_entity_table_map(self):
        # The fixture's JPQL query ("SELECT i FROM Invoice i WHERE
        # i.status = :status") is exactly the bounded single-entity case
        # resolve_jpql_to_lineage() handles: Invoice -> billing_invoice via
        # entity_table_map (Invoice.java's @Table(name="billing_invoice")),
        # alias "i." stripped, then fed through the same extract_sql_lineage()
        # native queries use. Real integration path, not a mocked lookup.
        entries = self._entries_for("raw_queries", "InvoiceRepository.java")
        jpql = next(e for e in entries if e["query_kind"] == "jpql")
        self.assertIn("lineage", jpql)
        self.assertTrue(jpql["lineage"]["available"], jpql["lineage"].get("reason"))
        self.assertEqual(jpql["lineage"]["source_tables"], ["billing_invoice"])

    # ---- api_surface / security ----

    def test_controller_and_mappings(self):
        entries = self._entries_for("api_surface", "InvoiceController.java")
        self.assertEqual(len(entries), 4)  # @RestController, @RequestMapping, @GetMapping, @PostMapping

    def test_multiline_security_annotation_detected(self):
        entries = self._entries_for("security", "InvoiceController.java")
        self.assertEqual(len(entries), 1)

    # ---- dedup: two distinct AST matches on one line collapse to one entry ----

    def test_same_line_double_usage_is_deduped(self):
        # Misc.java has `RestTemplate restTemplate = new RestTemplate();` —
        # two real, distinct type_identifier matches on one line. The old
        # regex scanner reported at most one hit per line; this scanner
        # dedupes by (file, line, ruleId) to match that, rather than
        # reporting every AST node individually.
        entries = self._entries_for("outbound_clients", "Misc.java")
        self.assertEqual(len(entries), 2)  # one import entry + one deduped usage entry

    def test_evidence_is_sorted_for_determinism(self):
        for bucket, entries in self.evidence.items():
            keys = [(e["file"], e.get("line", 0)) for e in entries]
            self.assertEqual(keys, sorted(keys), f"evidence[{bucket}] is not sorted")

    def test_entity_table_map_is_sorted_for_determinism(self):
        # entity_table_map is built inside the same ast-grep match loop as the
        # evidence buckets above, and for a long time was the one structure in
        # scan()'s output that never got sorted on the way out.
        keys = list(self.result["entity_table_map"].keys())
        self.assertEqual(keys, sorted(keys), "entity_table_map keys are not sorted")
