"""SQL lineage extraction via ``extract_sql_lineage`` (unit shapes)."""

from __future__ import annotations

import unittest

import pytest

from doc_engine.tools import spring_signal_scan

pytestmark = pytest.mark.domain_stage0


class SqlLineageExtractionTest(unittest.TestCase):
    """Direct ``extract_sql_lineage`` shapes outside the fixture scan path."""

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
        result = spring_signal_scan.extract_sql_lineage(
            "SELECT * FROM billing_invoice WHERE tenant_id = :#{#tenant}"
        )
        self.assertFalse(result["available"])
        self.assertIn("reason", result)

    def test_dialect_override_is_honored(self):
        query = "SELECT * FROM `billing_invoice` WHERE status = ?"
        ansi_result = spring_signal_scan.extract_sql_lineage(query, dialect="ansi")
        mysql_result = spring_signal_scan.extract_sql_lineage(query, dialect="mysql")
        self.assertFalse(ansi_result["available"])
        self.assertTrue(mysql_result["available"], mysql_result.get("reason"))
        self.assertEqual(mysql_result["source_tables"], ["billing_invoice"])

    def test_unavailable_when_sqllineage_not_installed(self):
        import doc_engine.scanning._resolve_lineage as resolve_lineage

        original = resolve_lineage._SQLLINEAGE_AVAILABLE
        resolve_lineage._SQLLINEAGE_AVAILABLE = False
        try:
            result = spring_signal_scan.extract_sql_lineage(
                "SELECT * FROM billing_invoice WHERE status = :status"
            )
        finally:
            resolve_lineage._SQLLINEAGE_AVAILABLE = original
        self.assertEqual(
            result, {"available": False, "reason": "sqllineage not installed"}
        )
