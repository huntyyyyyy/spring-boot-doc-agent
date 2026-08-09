"""Cohesive suite from tests/doc_engine/test_pipeline_stages.py: TagFormatTest, EvidencedCitationResolutionTest."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools.doc_tag_utils import (
    VALID_DOC_FILES,
    count_tags_by_kind,
    find_malformed_tags,
    resolve_evidenced_citations,
)
from doc_engine.tools.pipeline_validators import (
    FILE_SUMMARY_REQUIRED_KEYS,
    VALID_SPRING_ROLES,
    find_untraceable_nodes,
    run_stage5_gate,
    validate_architecture_testing_review_findings,
    validate_file_summarizer_entries,
    validate_gap_analyzer_questions,
)
SCRIPT_DIR = SCRIPTS_DIR

class TagFormatTest(unittest.TestCase):
    def test_all_five_forms_recognized_and_not_flagged_malformed(self):
        text = (
            "Uses PostgreSQL [Evidenced — build.gradle]. "
            "Endpoint requires BILLING_READ [Evidenced — InvoiceController.java:11]. "
            "Deploy cadence is weekly [Confirmed — interview, 2026-07-23]. "
            "Retry policy [Unknown — not evidenced in code, not covered in interview]. "
            "Owning team is Billing [Per existing docs — README.md, unverified against code]. "
            "Config binds env vars [Evidenced — Invoice.java:6; inference avoided beyond this]."
        )
        self.assertEqual(find_malformed_tags(text), [])
        counts = count_tags_by_kind(text)
        self.assertEqual(counts["evidenced"], 3)
        self.assertEqual(counts["confirmed"], 1)
        self.assertEqual(counts["unknown"], 1)
        self.assertEqual(counts["per_existing_docs"], 1)

    def test_wrong_dash_flagged_malformed(self):
        # Regression: a hyphen instead of an em dash is a real, easy-to-miss
        # LLM substitution that reads fine to a human skim but fails the
        # "exact wording" rule doc-taxonomy.md requires.
        text = "Owned by Billing team [Evidenced - build.gradle]."
        self.assertEqual(find_malformed_tags(text), ["[Evidenced - build.gradle]"])

    def test_missing_citation_flagged_malformed(self):
        # An Evidenced tag with no actual path/citation after the dash is
        # exactly the "guess dressed up as a tag" doc-taxonomy.md warns
        # against — it must not silently pass as well-formed.
        text = "Something is true [Evidenced —]."
        self.assertEqual(find_malformed_tags(text), ["[Evidenced —]"])

    def test_lowercase_tag_word_flagged_malformed(self):
        text = "Something is true [evidenced — build.gradle]."
        # Lowercase doesn't match TAG_WORD_SPAN at all (by design — this
        # documents the limit: a fully different casing isn't caught as
        # "malformed," it's simply invisible to a grep-shaped check. Confirm
        # that limit explicitly rather than silently relying on it.
        self.assertEqual(find_malformed_tags(text), [])
        self.assertEqual(count_tags_by_kind(text)["evidenced"], 0)


class EvidencedCitationResolutionTest(unittest.TestCase):
    def test_real_file_and_line_resolves(self):
        text = (
            "Requires BILLING_READ "
            "[Evidenced — src/main/java/com/example/billing/InvoiceController.java:11]."
        )
        self.assertEqual(resolve_evidenced_citations(text, FIXTURE_DIR), [])

    def test_whole_file_citation_resolves(self):
        text = (
            "Maps to table billing_invoice "
            "[Evidenced — src/main/java/com/example/billing/Invoice.java]."
        )
        self.assertEqual(resolve_evidenced_citations(text, FIXTURE_DIR), [])

    def test_nonexistent_file_fails_resolution(self):
        text = "Something [Evidenced — NoSuchController.java:5]."
        failures = resolve_evidenced_citations(text, FIXTURE_DIR)
        self.assertEqual(len(failures), 1)
        self.assertIn("does not exist", failures[0][1])

    def test_line_number_past_end_of_file_fails_resolution(self):
        text = (
            "Something "
            "[Evidenced — src/main/java/com/example/billing/Invoice.java:9999]."
        )
        failures = resolve_evidenced_citations(text, FIXTURE_DIR)
        self.assertEqual(len(failures), 1)
        self.assertIn("past the end", failures[0][1])
