"""Door-policy witnesses for JPQL lineage provenance (selector + actor).

Forged-badge cases: unavailable lineage that still carries a stale
``resolved_via_entity`` must not pass the selector or actor doors.
"""

from __future__ import annotations

import unittest

import pytest

from doc_engine.tools import spring_drift_check
from doc_engine.tools import spring_drift_jpql as jpql

pytestmark = pytest.mark.domain_stage0

_ENTITY_FILE = "src/main/java/com/example/billing/Invoice.java"
_QUERY_FILE = "src/main/java/com/example/billing/InvoiceRepository.java"


def _unavailable_with_stale_entity_signals():
    return {
        "entity_table_map": {
            "Invoice": {
                "file": _ENTITY_FILE,
                "table": "billing_invoice",
                "table_name_source": "explicit",
            },
        },
        "evidence": {
            "raw_queries": [
                {
                    "file": _QUERY_FILE,
                    "line": 9,
                    "query_kind": "jpql",
                    "query": "SELECT i FROM Invoice i",
                    "lineage": {
                        "available": False,
                        "reason": "out of scope",
                        "resolved_via_entity": "Invoice",
                    },
                },
            ],
        },
    }


class JpqlLineageDoorPolicyTest(unittest.TestCase):
    def test_selector_skips_unavailable_with_stale_entity_key(self):
        found = list(
            jpql._raw_query_entries_with_resolved_entity(
                _unavailable_with_stale_entity_signals()
            )
        )
        self.assertEqual(found, [])

    def test_actor_skips_unavailable_with_stale_entity_key(self):
        signals = _unavailable_with_stale_entity_signals()
        entry = signals["evidence"]["raw_queries"][0]
        results = [
            {
                "source": "evidence.raw_queries",
                "file": _QUERY_FILE,
                "line": 9,
                "status": spring_drift_check.STATUS_UNCHANGED,
                "tier": 1,
            }
        ]
        jpql._reverify_one_jpql_entry(
            entry,
            signals,
            fresh_entity_tables={"Invoice": {"table": "invoices"}},
            changed_set={_ENTITY_FILE},
            deleted_set=set(),
            results_by_file_line={(_QUERY_FILE, 9): results[0]},
        )
        self.assertEqual(results[0]["status"], spring_drift_check.STATUS_UNCHANGED)
