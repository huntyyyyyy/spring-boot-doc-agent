"""Kitchen-sink Ch10 command chain.

Stage-0 in this chapter uses ``filesystem,ast-grep`` only — CodeQL is
intentionally out of kitchen-sink scope (optional CLI / live opt-in). Covering
receipts and ABSENCE/UNPROVEN facts must not claim a CodeQL recall arm.
"""

from __future__ import annotations

import json
import os
import tempfile

import pytest

from doc_engine.scanning.covering import verify_covering_proof
from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES
from tests.support.kitchen_sink.constants import PY, SCRIPT_DIR
from tests.support.kitchen_sink.harness import _grouped, _run
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch10CommandChainTest(KitchenBoundTestCase):

    def test_every_chain_step_exited_zero(self):
        failures = {
            n: (p.returncode, (p.stdout or "") + (p.stderr or ""))
            for n, p in self.kitchen.steps.items()
            if p.returncode != 0
        }
        self.assertEqual(failures, {}, f"non-zero steps: {list(failures)}")

    def test_the_gate_passed_on_a_clean_run(self):
        gate = self.kitchen.steps["gate"]
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        self.assertIn("OK: all 14 docs present", gate.stdout)

    def test_all_fourteen_docs_written(self):
        present = {
            os.path.splitext(n)[0]
            for n in os.listdir(self.kitchen.docs)
            if n.endswith(".md")
        }
        self.assertEqual(present, set(VALID_DOC_FILES))

    def test_every_expected_artifact_exists_and_is_non_empty(self):
        out = self.kitchen.out
        for name in (
            "spring_signals.json",
            "covering_proof.json",
            "facts.jsonl",
            "groups.json",
            "cross_group_edges.json",
            "capacity_preflight_report.json",
            "run_manifest.json",
            "summaries.json",
            "architecture_merged.md",
            "gap_questions.json",
            "interview_answers.json",
            "drift_report.json",
        ):
            with self.subTest(artifact=name):
                path = os.path.join(out, name)
                self.assertTrue(os.path.isfile(path), f"{name} missing")
                self.assertGreater(os.path.getsize(path), 0)

    def test_covering_proof_verifies_against_path_a_inventory(self):
        """Deviation: chain greens without a verifiable covering_proof sibling."""
        signals = self.kitchen.signals
        proof = self.kitchen.covering_proof
        self.assertNotIn("_covering_proof", signals)
        self.assertNotIn("_scan_partials_meta", signals)
        ok, why = verify_covering_proof(
            proof,
            file_signatures=signals["file_signatures"],
            scanner_version=signals["scanner_version"],
        )
        self.assertTrue(ok, why)
        scanners = {r["scanner"] for r in proof["receipts"]}
        self.assertEqual(scanners, {"filesystem", "ast-grep"})
        self.assertNotIn("codeql", scanners)
        self.assertTrue(all(r["status"] == "complete" for r in proof["receipts"]))

    def test_facts_ledger_has_absence_or_unproven_stamps(self):
        """Deviation: dual-emit facts omit ABSENCE/UNPROVEN covering writers."""
        predicates = {row.get("predicate") for row in self.kitchen.facts}
        self.assertTrue(
            predicates & {"ABSENCE", "UNPROVEN"},
            f"expected ABSENCE/UNPROVEN in facts; got {sorted(predicates)}",
        )
        # Default filesystem,ast-grep profile must not claim entity recall.
        self.assertNotIn("RECALL_MISS", predicates)

    def test_signal_scan_stderr_emits_covering_event(self):
        """Deviation: covering_proof written silently with no covering_emit telemetry."""
        err = self.kitchen.steps["signal_scan"].stderr or ""
        compact = err.replace(" ", "")
        self.assertIn('"event":"covering_emit"', compact, err[-2000:])
        self.assertIn("inventory_root", err)

    def test_summaries_cover_every_grouped_file(self):
        with open(
            os.path.join(self.kitchen.out, "summaries.json"), encoding="utf-8"
        ) as f:
            summarized = {e["file"] for e in json.load(f)}
        self.assertEqual(_grouped(self.kitchen.groups) - summarized, set())

    def test_a_derived_view_is_not_stale_against_its_own_input(self):
        """Integrity catches corruption; drift catches staleness. Against the
        very scan the docs were derived from, nothing can be stale."""
        with open(
            os.path.join(self.kitchen.out, "drift_report.json"), encoding="utf-8"
        ) as f:
            report = json.load(f)
        self.assertEqual({r["status"] for r in report["results"]}, {"unchanged"})

    def test_run_pipeline_local_driver_runs_end_to_end(self):
        """The driver's first test. It is the packaged form of this same
        series, exercised against the small checked-in fixture rather than
        paying for a second enterprise-scale scan."""
        from tests.support.kitchen_sink.local_runner_assert import (
            assert_covering_proof_matches_signals,
            assert_local_runner_exit_and_banner,
            assert_mock_certification,
        )

        with tempfile.TemporaryDirectory() as d:
            run_dir = os.path.join(d, "run")
            proc = _run(
                [
                    PY,
                    "-m",
                    "doc_engine.pipeline.local_runner",
                    os.path.join(SCRIPT_DIR, "fixtures", "spring_signals"),
                    "--out-dir",
                    run_dir,
                    "--skip-drift",
                    "--allow-mock",
                ]
            )
            assert_local_runner_exit_and_banner(self, proc)
            assert_mock_certification(self, run_dir)
            assert_covering_proof_matches_signals(self, run_dir)
