"""Cohesive suite from tests/doc_engine/test_pipeline_stages.py: ArchitectureTestingReviewShapeTest, Stage5ArchitectureTestingReviewGateTest, ArchitectureTraceabilityTest, RealArtifactsOptInTest."""

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

class ArchitectureTestingReviewShapeTest(unittest.TestCase):
    def test_valid_finding_passes(self):
        findings = [{
            "lens": "ddia", "concept": "DDIA ch.6 — no version field",
            "claim": "InvoiceLedger has no @Version field.",
            "evidence": [{"file": "InvoiceLedger.java", "line": 22, "what": "@Entity with no @Version"}],
            "external_research": None, "severity": "worth-flagging",
        }]
        self.assertEqual(validate_architecture_testing_review_findings(findings), [])

    def test_missing_evidence_flagged(self):
        findings = [{"lens": "testing", "concept": "c", "claim": "x", "evidence": [], "severity": "informational"}]
        problems = validate_architecture_testing_review_findings(findings)
        self.assertTrue(any("non-empty array" in p[1] for p in problems))

    def test_invalid_lens_flagged(self):
        findings = [{"lens": "security", "concept": "c", "claim": "x",
                     "evidence": [{"line": 1, "what": "w"}], "severity": "informational"}]
        problems = validate_architecture_testing_review_findings(findings)
        self.assertTrue(any("not one of" in p[1] and "lens" in str(p) for p in problems) or
                        any("security" in p[1] for p in problems))

    def test_tier_c_only_external_research_flagged(self):
        """Regression for claude/steering-prompts/10-review-persona-and-standards.md
        §2's "Tier C may never appear as a citation" — a finding whose
        external_research rests entirely on deepwiki.com (Tier C) with no
        Tier A/B backing must be caught, not silently accepted."""
        findings = [{
            "lens": "ddia", "concept": "c", "claim": "x",
            "evidence": [{"line": 1, "what": "w"}], "severity": "informational",
            "external_research": {
                "question": "q",
                "sources": [{"tier": "C", "identifier": "deepwiki.com/x/y"}],
                "verdict": "PLAUSIBLE",
            },
        }]
        problems = validate_architecture_testing_review_findings(findings)
        self.assertTrue(any("Tier C" in p[1] for p in problems))

    def test_tier_a_backed_external_research_passes(self):
        findings = [{
            "lens": "ddia", "concept": "c", "claim": "x",
            "evidence": [{"line": 1, "what": "w"}], "severity": "informational",
            "external_research": {
                "question": "q",
                "sources": [{"tier": "A", "identifier": "github.com/x/y"}],
                "verdict": "CONFIRMED",
            },
        }]
        self.assertEqual(validate_architecture_testing_review_findings(findings), [])

    def test_invalid_verdict_flagged(self):
        findings = [{
            "lens": "ddia", "concept": "c", "claim": "x",
            "evidence": [{"line": 1, "what": "w"}], "severity": "informational",
            "external_research": {"question": "q", "sources": [], "verdict": "MAYBE"},
        }]
        problems = validate_architecture_testing_review_findings(findings)
        self.assertTrue(any("verdict" in p[1] for p in problems))

    def test_padded_list_exceeds_sanity_ceiling(self):
        findings = [{"lens": "ddia", "concept": f"c{i}", "claim": f"x{i}",
                     "evidence": [{"line": i, "what": "w"}], "severity": "informational"}
                    for i in range(61)]
        problems = validate_architecture_testing_review_findings(findings, max_findings=60)
        self.assertTrue(any("sanity ceiling" in p[1] for p in problems))


class Stage5ArchitectureTestingReviewGateTest(unittest.TestCase):
    """B4 — malformed architecture_testing_review.json must fail run_stage5_gate."""

    def test_malformed_review_fails_stage5_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "architecture_testing_review.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump([{
                    "lens": "security",
                    "concept": "c",
                    "claim": "x",
                    "evidence": [{"line": 1, "what": "w"}],
                    "severity": "informational",
                }], fh)
            failures = run_stage5_gate(tmp, tmp)
            self.assertTrue(
                any("architecture_testing_review.json" in f for f in failures),
                failures,
            )

    def test_valid_review_passes_stage5_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "architecture_testing_review.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump([{
                    "lens": "ddia",
                    "concept": "c",
                    "claim": "x",
                    "evidence": [{"line": 1, "what": "w"}],
                    "severity": "informational",
                    "external_research": None,
                }], fh)
            self.assertEqual(run_stage5_gate(tmp, tmp), [])

    def test_non_array_review_fails_stage5_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "architecture_testing_review.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"findings": []}, fh)
            failures = run_stage5_gate(tmp, tmp)
            self.assertTrue(any("JSON array" in f for f in failures), failures)


class ArchitectureTraceabilityTest(unittest.TestCase):
    def test_known_node_labels_trace(self):
        mermaid = (
            "flowchart TB\n"
            '  A["InvoiceController.java"] -->|calls| B["InvoiceRepository.java"]\n'
        )
        known_names = {"InvoiceController.java", "InvoiceRepository.java", "Invoice.java"}
        self.assertEqual(find_untraceable_nodes(mermaid, known_names), [])

    def test_fabricated_node_label_flagged(self):
        # Regression: architect-segment.md rule 3 explicitly forbids
        # inventing a "friendlier" label — this is the mechanical check for
        # that rule actually holding, since a human skim of a diagram won't
        # catch a plausible-sounding but nonexistent node name.
        mermaid = (
            "flowchart TB\n"
            '  A["Billing Orchestration Service"] --> B["InvoiceRepository.java"]\n'
        )
        known_names = {"InvoiceController.java", "InvoiceRepository.java", "Invoice.java"}
        untraceable = find_untraceable_nodes(mermaid, known_names)
        self.assertEqual(untraceable, ["Billing Orchestration Service"])


class RealArtifactsOptInTest(unittest.TestCase):
    """Opt-in pass against a real completed pipeline run's actual output,
    gated by PIPELINE_ARTIFACTS_DIR (same pattern as
    tests/doc_engine/test_partition_repo_real_world.py's PARTITION_REPO_REAL_FIXTURE_DIR).
    Expected directory layout: summaries.json (file-summarizer output),
    architecture.md (merged Mermaid + discrepancies), gap_questions.json
    (gap-analyzer output), and docs/*.md (the fourteen doc-writer outputs).
    Skipped entirely if the env var isn't set — this file's other test
    classes don't depend on it."""

    @classmethod
    def setUpClass(cls):
        cls.artifacts_dir = os.environ.get("PIPELINE_ARTIFACTS_DIR")
        if not cls.artifacts_dir:
            raise unittest.SkipTest("PIPELINE_ARTIFACTS_DIR not set — opt-in real-artifacts pass skipped")
        if not os.path.isdir(cls.artifacts_dir):
            raise unittest.SkipTest(f"PIPELINE_ARTIFACTS_DIR={cls.artifacts_dir!r} is not a directory")

    def test_summaries_json_shape(self):
        path = os.path.join(self.artifacts_dir, "summaries.json")
        if not os.path.isfile(path):
            self.skipTest("summaries.json not present in PIPELINE_ARTIFACTS_DIR")
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
        self.assertEqual(validate_file_summarizer_entries(entries), [])

    def test_gap_questions_shape(self):
        path = os.path.join(self.artifacts_dir, "gap_questions.json")
        if not os.path.isfile(path):
            self.skipTest("gap_questions.json not present in PIPELINE_ARTIFACTS_DIR")
        with open(path, encoding="utf-8") as f:
            questions = json.load(f)
        self.assertEqual(validate_gap_analyzer_questions(questions), [])

    def test_generated_docs_tags_well_formed_and_resolvable(self):
        docs_dir = os.path.join(self.artifacts_dir, "docs")
        target_repo_dir = os.environ.get("PIPELINE_ARTIFACTS_TARGET_REPO", self.artifacts_dir)
        if not os.path.isdir(docs_dir):
            self.skipTest("docs/ not present in PIPELINE_ARTIFACTS_DIR")
        for name in os.listdir(docs_dir):
            if not name.endswith(".md"):
                continue
            with open(os.path.join(docs_dir, name), encoding="utf-8") as f:
                text = f.read()
            with self.subTest(file=name):
                self.assertEqual(find_malformed_tags(text), [])
                unresolved = resolve_evidenced_citations(text, target_repo_dir)
                self.assertEqual(unresolved, [], f"unresolvable [Evidenced — ...] citations in {name}: {unresolved}")
