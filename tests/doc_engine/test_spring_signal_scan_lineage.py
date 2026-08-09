"""SQL/JPQL lineage extraction and resolution suites."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.scanning._resolve_lineage import _SQLLINEAGE_AVAILABLE
from doc_engine.scanning.facts import facts_from_signals
from doc_engine.tools import spring_signal_scan

import pytest

pytestmark = pytest.mark.domain_stage0

SCRIPT_DIR = SCRIPTS_DIR
USE_SNAPSHOT = os.environ.get("SPRING_SIGNAL_USE_SNAPSHOT", "").lower() in ("1", "true", "yes")
SNAPSHOT_SCANNERS = ["filesystem", "ast-grep"]

class SqlLineageExtractionTest(unittest.TestCase):
    """Unit-level tests against extract_sql_lineage() directly, rather than
    through a full scan() — same real sqllineage dependency, no mocking,
    just exercising query shapes the fixture repo doesn't happen to cover
    (positional params, UPDATE/INSERT target-table detection, genuinely
    malformed input, and the soft-degradation path when sqllineage is
    unavailable)."""

    def test_positional_param_query_extracts_source_table(self):
        result = spring_signal_scan.extract_sql_lineage(
            "SELECT * FROM billing_invoice WHERE id = ?1 AND status = ?2"
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["billing_invoice"])

    def test_update_query_extracts_target_table(self):
        result = spring_signal_scan.extract_sql_lineage(
            "UPDATE billing_invoice SET status = :status WHERE id = :id"
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["target_tables"], ["billing_invoice"])

    def test_insert_query_extracts_target_table(self):
        result = spring_signal_scan.extract_sql_lineage(
            "INSERT INTO audit_log (event, ts) VALUES (:event, :ts)"
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["target_tables"], ["audit_log"])

    def test_join_query_extracts_both_source_tables(self):
        result = spring_signal_scan.extract_sql_lineage(
            "SELECT i.id FROM billing_invoice i "
            "JOIN customer c ON i.customer_id = c.id WHERE i.status = ?"
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["billing_invoice", "customer"])

    def test_time_literal_survives_param_normalization(self):
        # Regression guard for the negative-lookbehind in NAMED_PARAM_RE:
        # a time literal's colons must not be mistaken for bind parameters
        # (each one is preceded by a digit, never by whitespace/operator/
        # '('/',' the way a real ":status"-style parameter always is).
        result = spring_signal_scan.extract_sql_lineage(
            "SELECT * FROM billing_invoice WHERE created_at > '2024-01-01 12:00:00'"
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["billing_invoice"])

    def test_malformed_sql_degrades_gracefully(self):
        result = spring_signal_scan.extract_sql_lineage("this is not sql at all !!! @#$%")
        self.assertFalse(result["available"])
        self.assertIn("reason", result)

    def test_spel_expression_degrades_gracefully_not_raises(self):
        # A Spring SpEL expression like :#{#tenant} is real, fairly common
        # (multi-tenant native queries) Spring syntax, but it is not real
        # bind-parameter syntax NAMED_PARAM_RE normalizes, and it isn't
        # valid SQL either. This must degrade, not raise all the way up
        # through scan().
        result = spring_signal_scan.extract_sql_lineage(
            "SELECT * FROM billing_invoice WHERE tenant_id = :#{#tenant}"
        )
        self.assertFalse(result["available"])
        self.assertIn("reason", result)

    def test_dialect_override_is_honored(self):
        # mysql-specific backtick-quoted identifiers fail to parse under
        # plain ansi but succeed once the real dialect is passed — proof
        # the --sql-dialect flag actually reaches sqllineage, not just that
        # the default works.
        query = "SELECT * FROM `billing_invoice` WHERE status = ?"
        ansi_result = spring_signal_scan.extract_sql_lineage(query, dialect="ansi")
        mysql_result = spring_signal_scan.extract_sql_lineage(query, dialect="mysql")
        self.assertFalse(ansi_result["available"])
        self.assertTrue(mysql_result["available"], mysql_result.get("reason"))
        self.assertEqual(mysql_result["source_tables"], ["billing_invoice"])

    def test_unavailable_when_sqllineage_not_installed(self):
        # Simulates the "package genuinely not installed" branch by
        # flipping _resolve_lineage's availability flag — this exercises our
        # soft-degradation code path, not sqllineage's parsing behavior
        # (which every other test in this class already covers for real).
        import doc_engine.scanning._resolve_lineage as _resolve_lineage
        original = _resolve_lineage._SQLLINEAGE_AVAILABLE
        _resolve_lineage._SQLLINEAGE_AVAILABLE = False
        try:
            result = spring_signal_scan.extract_sql_lineage(
                "SELECT * FROM billing_invoice WHERE status = :status"
            )
        finally:
            _resolve_lineage._SQLLINEAGE_AVAILABLE = original
        self.assertEqual(result, {"available": False, "reason": "sqllineage not installed"})

class JpqlLineageResolutionTest(unittest.TestCase):
    """Unit-level tests against resolve_jpql_to_lineage() directly, with a
    synthetic entity_table_map — covers the bounded resolver's happy path
    plus each explicitly-out-of-scope case named in its own docstring
    (multi-entity FROM, association traversal, JPQL-only functions, an
    unresolved entity name). SpringSignalScanTest.test_jpql_query_resolves_
    lineage_via_entity_table_map covers the same happy path through the
    real scan()/entity_table_map integration; these are the narrower unit
    cases that don't need a fixture repo."""

    ENTITY_TABLE_MAP = {
        "Invoice": {"table": "billing_invoice", "table_name_source": "explicit"},
        "Customer": {"table": "customer", "table_name_source": "inferred-default-naming"},
    }

    def test_single_entity_query_resolves(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.status = :status", self.ENTITY_TABLE_MAP
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["billing_invoice"])

    def test_resolved_lineage_records_which_entity_it_used(self):
        # Drift-check needs this to detect a cross-file dependency: a JPQL
        # citation's lineage can go stale because the *entity's* file
        # changed (e.g. @Table renamed), not the query's own file — see
        # spring_drift_check.py's _reverify_jpql_lineage_provenance().
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.status = :status", self.ENTITY_TABLE_MAP
        )
        self.assertEqual(result["resolved_via_entity"], "Invoice")

    def test_unresolved_lineage_has_no_resolved_via_entity(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i JOIN i.customer c WHERE c.active = true", self.ENTITY_TABLE_MAP
        )
        self.assertNotIn("resolved_via_entity", result)

    def test_query_with_as_keyword_resolves(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT c FROM Customer AS c WHERE c.active = true", self.ENTITY_TABLE_MAP
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["customer"])

    def test_multi_entity_from_clause_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i, Customer c WHERE i.customerId = c.id", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
        self.assertIn("out of scope", result["reason"])

    def test_join_clause_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i JOIN i.customer c WHERE c.active = true", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
        self.assertIn("out of scope", result["reason"])

    def test_association_traversal_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.customer.name = :name", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
        self.assertIn("association-traversal", result["reason"])

    def test_jpql_only_function_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE SIZE(i.lineItems) > 0", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
        self.assertIn("JPQL-only", result["reason"])

    def test_unresolved_entity_name_out_of_scope(self):
        # Not in entity_table_map at all — e.g. an @Entity(name=...) override
        # this scanner doesn't currently extract, or a genuinely unscanned
        # entity. Must degrade, not KeyError.
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT p FROM Payment p WHERE p.status = :status", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
        self.assertIn("not found in entity_table_map", result["reason"])

    def test_contested_entity_name_refuses_lineage(self):
        contested_map = {
            "Invoice": {
                "file": "a/Invoice.java",
                "table": "a_invoice",
                "table_name_source": "explicit",
                "status": "contested",
                "candidates": [
                    {"file": "a/Invoice.java", "table": "a_invoice",
                     "table_name_source": "explicit"},
                    {"file": "b/Invoice.java", "table": "b_invoice",
                     "table_name_source": "explicit"},
                ],
            }
        }
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.status = :status", contested_map
        )
        self.assertFalse(result["available"])
        self.assertIn("contested", result["reason"])
        self.assertIn("2 candidates", result["reason"])

    def test_no_from_clause_out_of_scope(self):
        # JPQL bulk UPDATE/DELETE don't use FROM at all — the resolver
        # should degrade cleanly, not assume a SELECT-shaped query.
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "UPDATE Invoice i SET i.status = :status WHERE i.id = :id", self.ENTITY_TABLE_MAP
        )
        self.assertFalse(result["available"])
