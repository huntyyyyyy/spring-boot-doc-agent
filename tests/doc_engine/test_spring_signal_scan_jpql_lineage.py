"""JPQL lineage resolution via ``resolve_jpql_to_lineage`` (bounded unit cases)."""

from __future__ import annotations

import unittest

import pytest

from doc_engine.tools import spring_signal_scan

pytestmark = pytest.mark.domain_stage0


class JpqlLineageResolutionTest(unittest.TestCase):
    """Synthetic entity_table_map cases for the bounded JPQL resolver."""

    ENTITY_TABLE_MAP = {
        "Invoice": {"table": "billing_invoice", "table_name_source": "explicit"},
        "Customer": {
            "table": "customer",
            "table_name_source": "inferred-default-naming",
        },
    }

    def test_single_entity_query_resolves(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.status = :status", self.ENTITY_TABLE_MAP
        )
        self.assertTrue(result["available"], result.get("reason"))
        self.assertEqual(result["source_tables"], ["billing_invoice"])

    def test_resolved_lineage_records_which_entity_it_used(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.status = :status", self.ENTITY_TABLE_MAP
        )
        self.assertEqual(result["resolved_via_entity"], "Invoice")

    def test_unresolved_lineage_has_no_resolved_via_entity(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i JOIN i.customer c WHERE c.active = true",
            self.ENTITY_TABLE_MAP,
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
            "SELECT i FROM Invoice i, Customer c WHERE i.customerId = c.id",
            self.ENTITY_TABLE_MAP,
        )
        self.assertFalse(result["available"])
        self.assertIn("out of scope", result["reason"])

    def test_join_clause_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i JOIN i.customer c WHERE c.active = true",
            self.ENTITY_TABLE_MAP,
        )
        self.assertFalse(result["available"])
        self.assertIn("out of scope", result["reason"])

    def test_association_traversal_out_of_scope(self):
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT i FROM Invoice i WHERE i.customer.name = :name",
            self.ENTITY_TABLE_MAP,
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
                    {
                        "file": "a/Invoice.java",
                        "table": "a_invoice",
                        "table_name_source": "explicit",
                    },
                    {
                        "file": "b/Invoice.java",
                        "table": "b_invoice",
                        "table_name_source": "explicit",
                    },
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
        result = spring_signal_scan.resolve_jpql_to_lineage(
            "UPDATE Invoice i SET i.status = :status WHERE i.id = :id",
            self.ENTITY_TABLE_MAP,
        )
        self.assertFalse(result["available"])
