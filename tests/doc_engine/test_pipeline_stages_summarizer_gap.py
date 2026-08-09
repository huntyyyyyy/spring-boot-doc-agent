"""Cohesive suite from tests/doc_engine/test_pipeline_stages.py: FileSummarizerShapeTest, GapAnalyzerShapeTest."""

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

import pytest

pytestmark = pytest.mark.domain_pipeline

SCRIPT_DIR = SCRIPTS_DIR

class FileSummarizerShapeTest(unittest.TestCase):
    def test_valid_entries_pass(self):
        entries = [{
            "file": "InvoiceController.java", "cluster": ["Invoice.java"],
            "summary": "Handles invoice retrieval and creation.",
            "relationships": ["Invoice.java"], "cross_group_relationships": [],
            "group_function": "Invoice billing API", "spring_role": "controller",
            "evidence": [{"line": 42, "what": "creates invoices from the POST handler"}],
        }]
        self.assertEqual(validate_file_summarizer_entries(entries), [])

    def test_missing_key_flagged(self):
        entries = [{"file": "X.java", "cluster": [], "summary": "s",
                    "relationships": [], "group_function": "", "spring_role": "other",
                    "evidence": []}]
        problems = validate_file_summarizer_entries(entries)
        self.assertEqual(len(problems), 1)
        self.assertIn("cross_group_relationships", problems[0][1])

    def test_invalid_spring_role_flagged(self):
        entries = [{"file": "X.java", "cluster": [], "summary": "s", "relationships": [],
                    "cross_group_relationships": [], "group_function": "",
                    "spring_role": "controllerish", "evidence": []}]
        problems = validate_file_summarizer_entries(entries)
        self.assertEqual(len(problems), 1)
        self.assertIn("spring_role", problems[0][1])

    def _entry(self, **overrides):
        entry = {"file": "X.java", "cluster": [], "summary": "s", "relationships": [],
                 "cross_group_relationships": [], "group_function": "",
                 "spring_role": "other", "evidence": []}
        entry.update(overrides)
        return entry

    def test_missing_evidence_key_flagged(self):
        """The whole point of the field: a summarizer that silently stops
        emitting it drops every semantic line anchor in the run."""
        entry = self._entry()
        del entry["evidence"]
        problems = validate_file_summarizer_entries([entry])
        self.assertEqual(len(problems), 1)
        self.assertIn("evidence", problems[0][1])

    def test_empty_evidence_list_is_legitimate(self):
        """A genuinely whole-file summary has no single anchor. Requiring a
        non-empty list would just buy back invented line numbers."""
        self.assertEqual(validate_file_summarizer_entries([self._entry()]), [])

    def test_evidence_must_be_a_list(self):
        problems = validate_file_summarizer_entries([self._entry(evidence={"line": 1, "what": "x"})])
        self.assertTrue(any("must be a list" in p[1] for p in problems))

    def test_evidence_entry_missing_line_flagged(self):
        problems = validate_file_summarizer_entries([self._entry(evidence=[{"what": "x"}])])
        self.assertTrue(any("missing keys" in p[1] for p in problems))

    def test_evidence_line_must_be_an_int(self):
        problems = validate_file_summarizer_entries([self._entry(evidence=[{"line": "42", "what": "x"}])])
        self.assertTrue(any("must be an int" in p[1] for p in problems))

    def test_evidence_line_bool_rejected(self):
        """bool subclasses int; True is not a line number."""
        problems = validate_file_summarizer_entries([self._entry(evidence=[{"line": True, "what": "x"}])])
        self.assertTrue(any("must be an int" in p[1] for p in problems))

    def test_evidence_line_must_be_positive(self):
        problems = validate_file_summarizer_entries([self._entry(evidence=[{"line": 0, "what": "x"}])])
        self.assertTrue(any(">= 1" in p[1] for p in problems))

    def test_evidence_what_must_be_non_empty(self):
        problems = validate_file_summarizer_entries([self._entry(evidence=[{"line": 5, "what": "  "}])])
        self.assertTrue(any("non-empty string" in p[1] for p in problems))

class GapAnalyzerShapeTest(unittest.TestCase):
    def test_valid_bounded_list_passes(self):
        questions = [
            {"blocks_file": "database", "topic": "write ownership", "question": "q1", "evidence": "src/main/java/A.java:10 is the only writer"},
            {"blocks_file": "database", "topic": "write ownership 2", "question": "q2", "evidence": "src/main/java/B.java:20 has no guard"},
            {"blocks_file": "authorization", "topic": "endpoint", "question": "q3", "evidence": "src/main/java/C.java:30 is unmapped"},
        ]
        self.assertEqual(validate_gap_analyzer_questions(questions), [])

    def test_invalid_blocks_file_flagged(self):
        questions = [{"blocks_file": "faq", "topic": "t", "question": "q", "evidence": "src/main/java/A.java:10 is the only writer"}]
        problems = validate_gap_analyzer_questions(questions)
        self.assertEqual(len(problems), 1)
        self.assertIn("not one of the fourteen", problems[0][1])

    def test_non_contiguous_grouping_flagged(self):
        # Regression: gap-analyzer.md requires output "grouped by which file
        # they block" so the orchestrator can present them grouped. A
        # blocks_file that reappears after another file's questions have
        # already started is the mechanical signature of that rule breaking.
        questions = [
            {"blocks_file": "database", "topic": "t1", "question": "q1", "evidence": "src/main/java/A.java:10 is the only writer"},
            {"blocks_file": "authorization", "topic": "t2", "question": "q2", "evidence": "src/main/java/B.java:20 has no guard"},
            {"blocks_file": "database", "topic": "t3", "question": "q3", "evidence": "src/main/java/C.java:30 is unmapped"},
        ]
        problems = validate_gap_analyzer_questions(questions)
        self.assertEqual(len(problems), 1)
        self.assertIn("non-contiguously", problems[0][1])

    def test_elided_path_in_evidence_flagged(self):
        """gap-analyzer.md's own example used to ship `(src/.../Foo.java)`,
        so this malformed shape was actively modeled for the agent."""
        questions = [{"blocks_file": "database", "topic": "t", "question": "q",
                      "evidence": "InvoiceService.markPaid (src/.../InvoiceService.java) is the only writer"}]
        problems = validate_gap_analyzer_questions(questions)
        self.assertTrue(any("elided path" in p[1] for p in problems))

    def test_evidence_without_any_citation_flagged(self):
        """Unconstrained prose here leaves every downstream
        [Confirmed — interview, <date>] claim unanchored to any location."""
        questions = [{"blocks_file": "database", "topic": "t", "question": "q",
                      "evidence": "this table looks like it has one writer"}]
        problems = validate_gap_analyzer_questions(questions)
        self.assertTrue(any("no file citation" in p[1] for p in problems))

    def test_evidence_with_path_and_line_passes(self):
        questions = [{"blocks_file": "database", "topic": "t", "question": "q",
                      "evidence": "src/main/java/com/example/InvoiceService.java:88 is the only write path"}]
        self.assertEqual(validate_gap_analyzer_questions(questions), [])

    def test_evidence_with_bare_path_passes(self):
        """A path without a line is weaker but still resolvable; the taxonomy
        allows whole-file citations, so this is not the failure being caught."""
        questions = [{"blocks_file": "database", "topic": "t", "question": "q",
                      "evidence": "declared in src/main/resources/schema.sql"}]
        self.assertEqual(validate_gap_analyzer_questions(questions), [])

    def test_padded_list_exceeds_sanity_ceiling(self):
        questions = [{"blocks_file": "database", "topic": f"t{i}", "question": f"q{i}", "evidence": f"src/main/java/A{i}.java:10 is the only writer"}
                     for i in range(41)]
        problems = validate_gap_analyzer_questions(questions, max_questions=40)
        self.assertTrue(any("sanity ceiling" in p[1] for p in problems))
