"""Cohesive suite from tests/doc_engine/test_citation_coverage.py: TestWeakAnchors, TestCheckDocsAndExit."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import citation_coverage as cc

import pytest

pytestmark = pytest.mark.domain_pipeline

class TestWeakAnchors(unittest.TestCase):

    SRC = """package com.example;

import org.springframework.stereotype.Controller;

@Controller
class OwnerController {
    private final OwnerRepository owners;

    public String processFindForm() {
        return "redirect:/owners/";
    }
}
"""

    def setUp(self):
        self.repo = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.repo, "src"))
        with open(os.path.join(self.repo, "src", "OwnerController.java"), "w",
                  encoding="utf-8") as f:
            f.write(self.SRC)

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def test_symbol_absent_from_file_is_flagged(self):
        text = ("The SecurityFilterChain bean is declared "
                "[Evidenced — src/OwnerController.java:5].\n")
        findings = cc.find_weak_anchors(text, self.repo)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["kind"], "symbol_absent_from_file")

    def test_symbol_outside_window_is_flagged(self):
        """The real observed failure: a fact that exists in the file, cited at
        a line nowhere near it."""
        text = ("The processFindForm() method redirects after a search "
                "[Evidenced — src/OwnerController.java:1].\n")
        findings = cc.find_weak_anchors(text, self.repo, window=2)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["kind"], "symbol_outside_window")
        self.assertIn("processFindForm", findings[0]["found_elsewhere_in_file"])

    def test_accurate_citation_is_not_flagged(self):
        text = ("The processFindForm() method redirects after a search "
                "[Evidenced — src/OwnerController.java:9].\n")
        self.assertEqual(cc.find_weak_anchors(text, self.repo), [])

    def test_whole_file_citation_has_no_anchor_to_check(self):
        text = "Dependencies are declared [Evidenced — build.gradle].\n"
        self.assertEqual(cc.find_weak_anchors(text, self.repo), [])

    def test_unresolvable_citation_is_left_to_the_other_checker(self):
        """resolve_evidenced_citations() owns 'this path does not exist'.
        Reporting it here too would file one defect twice."""
        text = "The Ghost class does things [Evidenced — src/Ghost.java:3].\n"
        self.assertEqual(cc.find_weak_anchors(text, self.repo), [])

    def test_citation_past_end_of_file_is_left_to_the_other_checker(self):
        text = "The OwnerRepository is injected [Evidenced — src/OwnerController.java:999].\n"
        self.assertEqual(cc.find_weak_anchors(text, self.repo), [])

    def test_claim_naming_only_the_cited_file_is_not_evidence(self):
        """A claim about OwnerController citing OwnerController.java tells us
        nothing about whether that *line* supports it, so there is nothing to
        check and nothing to flag."""
        text = "The OwnerController exists [Evidenced — src/OwnerController.java:1].\n"
        self.assertEqual(cc.find_weak_anchors(text, self.repo), [])

    def test_window_is_configurable(self):
        text = ("The processFindForm() method redirects "
                "[Evidenced — src/OwnerController.java:1].\n")
        self.assertEqual(len(cc.find_weak_anchors(text, self.repo, window=2)), 1)
        self.assertEqual(cc.find_weak_anchors(text, self.repo, window=20), [])

class TestCheckDocsAndExit(unittest.TestCase):

    def setUp(self):
        self.docs = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.docs, ignore_errors=True)

    def _write(self, name, text):
        with open(os.path.join(self.docs, name), "w", encoding="utf-8") as f:
            f.write(text)

    def test_check_docs_reports_per_file(self):
        self._write("a.md", "The OwnerController handles lookups.\n")
        self._write("b.md", "Everything here is plain narrative prose.\n")
        report = cc.check_docs(self.docs, None)
        self.assertEqual(len(report["a.md"]["untagged_claims"]), 1)
        self.assertEqual(report["b.md"]["untagged_claims"], [])
        self.assertEqual(cc.total_findings(report), 1)

    def test_weak_anchor_check_skipped_without_target_repo_is_stated_not_silent(self):
        """check_pipeline_output.py's equivalent returns clean and says nothing
        when no target repo is given. This one says so out loud."""
        self._write("a.md", "Lookups happen [Evidenced — src/OwnerController.java:9].\n")
        report = cc.check_docs(self.docs, None)
        self.assertEqual(report["a.md"]["weak_anchors"], [])
        self.assertIn("did not run", cc.format_report(report, None))

    def test_non_markdown_files_ignored(self):
        self._write("notes.txt", "The OwnerController handles lookups.\n")
        self.assertEqual(cc.check_docs(self.docs, None), {})
