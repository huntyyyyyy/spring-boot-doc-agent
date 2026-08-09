"""Cohesive suite from tests/doc_engine/test_semantic_eval_helpers.py: RunEndToEndTest."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import semantic_eval_helpers

import pytest

pytestmark = pytest.mark.domain_pipeline

SCRIPT_DIR = SCRIPTS_DIR
ANSWERED_ENTRY = {
    "blocks_file": "database", "topic": "write ownership: billing_invoice",
    "question": "Is InvoiceService.markPaid the only writer of billing_invoice?",
    "status": "answered", "answer": "Yes, InvoiceService is the only writer of billing_invoice.",
    "date": "2026-07-23",
}
SKIPPED_ENTRY = {
    "blocks_file": "authorization", "topic": "endpoint intent",
    "question": "Is this endpoint intentionally public?",
    "status": "skipped", "date": "2026-07-23",
}

class RunEndToEndTest(unittest.TestCase):
    def test_run_against_synthetic_artifacts_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs_dir = os.path.join(tmp, "docs")
            os.makedirs(docs_dir)

            with open(os.path.join(tmp, "interview_answers.json"), "w", encoding="utf-8") as f:
                json.dump([ANSWERED_ENTRY], f)

            with open(os.path.join(docs_dir, "database.md"), "w", encoding="utf-8") as f:
                f.write("InvoiceService is the only writer of billing_invoice "
                        "[Confirmed — interview, 2026-07-23].\n"
                        "The service deploys nightly at 2am UTC "
                        "[Confirmed — interview, 2026-07-23].\n")

            with open(os.path.join(docs_dir, "architecture.md"), "w", encoding="utf-8") as f:
                f.write("# Architecture\n\n```mermaid\nflowchart TB\n"
                         '  A["Invoice.java" --> B["InvoiceRepository.java"]\n```\n')

            report = semantic_eval_helpers.run(tmp)

            self.assertIn("database.md", report["unmatched_confirmed_tags_by_file"])
            self.assertEqual(len(report["unmatched_confirmed_tags_by_file"]["database.md"]), 1)
            self.assertTrue(len(report["mermaid_syntax_findings"]) >= 1)

    def test_run_with_no_interview_answers_file_treats_all_confirmed_as_unmatched(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs_dir = os.path.join(tmp, "docs")
            os.makedirs(docs_dir)
            with open(os.path.join(docs_dir, "readme.md"), "w", encoding="utf-8") as f:
                f.write("Deploy cadence is weekly [Confirmed — interview, 2026-07-23].\n")

            report = semantic_eval_helpers.run(tmp)
            self.assertIn("readme.md", report["unmatched_confirmed_tags_by_file"])

    def test_run_with_no_docs_dir_returns_empty_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = semantic_eval_helpers.run(tmp)
            self.assertEqual(report["unmatched_confirmed_tags_by_file"], {})
            self.assertEqual(report["mermaid_syntax_findings"], [])
