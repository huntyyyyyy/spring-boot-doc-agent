"""Kitchen-sink Ch10 command chain."""

from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS
from doc_engine.pipeline.mock_stages import (
    find_existing_readme,
    load_citations,
    mock_architecture,
    mock_docs,
    mock_file_summaries,
    mock_gap_and_interview,
    sweep_todos,
)
from doc_engine.tools import partition_repo, run_manifest, spring_signal_scan
from doc_engine.tools.doc_tag_utils import VALID_DOC_FILES
from doc_engine.scanning.covering import verify_covering_proof
SCRIPT_DIR = SCRIPTS_DIR
PY = sys.executable
MAX_TOKENS = "2000"
SMALL_FILE_BYTES = "4096"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
BILLING = "services/billing-service/src/main/java/com/acme/billing"
LEDGER = "services/ledger-service/src/main/java/com/acme/ledger"
LEGACY = "services/legacy-batch/src/main/java/com/acme/legacy"
RES = "services/billing-service/src/main/resources"
TWO_ENTITIES = f"{BILLING}/TwoEntities.java"
MIXED_ENTITIES = f"{BILLING}/MixedEntities.java"
NESTED_ENTITY = f"{BILLING}/NestedEntity.java"
DUP_BILLING = f"{BILLING}/Invoice.java"
DUP_LEDGER = f"{LEDGER}/Invoice.java"
UNICODE_QUERY = f"{LEDGER}/LedgerRepository.java"
HUGE_JAVA = f"{LEGACY}/Huge.java"
EMPTY_JAVA = f"{LEGACY}/Empty.java"
LATIN1_JAVA = f"{LEGACY}/Latin1.java"
NUL_JAVA = f"{LEGACY}/NulInside.java"
CRLF_JAVA = f"{LEGACY}/Crlf.java"
BOM_YML = f"{RES}/application-prod.yml"
NOBOM_YML = f"{RES}/application-nobom.yml"
PLACEHOLDER_YML = f"{RES}/application.yml"
SECRETS_YML = f"{RES}/application-secrets.yml"
MULTI_SEG_YML = f"{RES}/application-dev-local.yml"
CRLF_PROPS = f"{RES}/application-legacy.properties"
LF_PROPS = f"{RES}/application-lfprops.properties"
EMPTY_YML = f"{RES}/application-empty.yml"
SPACE_PATH = "docs and notes/guide.md"
UNICODE_DIR_JAVA = "módulo-común/src/main/java/com/acme/uni/UniController.java"
DEEP_JAVA = "deep/" + "/".join(f"l{i:02d}" for i in range(30)) + "/Leaf.java"
GITIGNORED_DIR = "generated"
PLANTED_EXCLUDED_DIRS = ["target", "build", "node_modules", "vendor", "venv",
                         "dist", "out", "coverage"]
from tests.support.kitchen_sink.writers import (
    _controller,
    _entity,
    _service,
    _w,
    _wb,
)
from tests.support.kitchen_sink.repo_builder import build_enterprise_repo
from tests.support.kitchen_sink.constants import _STATE
from tests.support.kitchen_sink.harness import (
    _copy_docs,
    _evidence_files,
    _grouped,
    _has_segment,
    _kitchen_sink_real_repo,
    _miscase_first_tag,
    _git,
    _run,
    run_chain,
    setUpModule,
    tearDownModule,
)

class Ch10CommandChainTest(unittest.TestCase):

    def test_every_chain_step_exited_zero(self):
        failures = {n: (p.returncode, (p.stdout or "") + (p.stderr or ""))
                    for n, p in _STATE["steps"].items() if p.returncode != 0}
        self.assertEqual(failures, {}, f"non-zero steps: {list(failures)}")

    def test_the_gate_passed_on_a_clean_run(self):
        gate = _STATE["steps"]["gate"]
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        self.assertIn("OK: all 14 docs present", gate.stdout)

    def test_all_fourteen_docs_written(self):
        present = {os.path.splitext(n)[0] for n in os.listdir(_STATE["docs"])
                   if n.endswith(".md")}
        self.assertEqual(present, set(VALID_DOC_FILES))

    def test_every_expected_artifact_exists_and_is_non_empty(self):
        out = _STATE["out"]
        for name in ("spring_signals.json", "covering_proof.json", "facts.jsonl",
                     "groups.json", "cross_group_edges.json",
                     "capacity_preflight_report.json", "run_manifest.json",
                     "summaries.json", "architecture_merged.md", "gap_questions.json",
                     "interview_answers.json", "drift_report.json"):
            with self.subTest(artifact=name):
                path = os.path.join(out, name)
                self.assertTrue(os.path.isfile(path), f"{name} missing")
                self.assertGreater(os.path.getsize(path), 0)

    def test_covering_proof_verifies_against_path_a_inventory(self):
        """Deviation: chain greens without a verifiable covering_proof sibling."""
        signals = _STATE["signals"]
        proof = _STATE["covering_proof"]
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
        self.assertTrue(all(r["status"] == "complete" for r in proof["receipts"]))

    def test_facts_ledger_has_absence_or_unproven_stamps(self):
        """Deviation: dual-emit facts omit ABSENCE/UNPROVEN covering writers."""
        predicates = {row.get("predicate") for row in _STATE["facts"]}
        self.assertTrue(
            predicates & {"ABSENCE", "UNPROVEN"},
            f"expected ABSENCE/UNPROVEN in facts; got {sorted(predicates)}",
        )
        # Default filesystem,ast-grep profile must not claim entity recall.
        self.assertNotIn("RECALL_MISS", predicates)

    def test_signal_scan_stderr_emits_covering_event(self):
        """Deviation: covering_proof written silently with no covering_emit telemetry."""
        err = _STATE["steps"]["signal_scan"].stderr or ""
        compact = err.replace(" ", "")
        self.assertIn('"event":"covering_emit"', compact, err[-2000:])
        self.assertIn("inventory_root", err)

    def test_summaries_cover_every_grouped_file(self):
        with open(os.path.join(_STATE["out"], "summaries.json"), encoding="utf-8") as f:
            summarized = {e["file"] for e in json.load(f)}
        self.assertEqual(_grouped(_STATE["groups"]) - summarized, set())

    def test_a_derived_view_is_not_stale_against_its_own_input(self):
        """Integrity catches corruption; drift catches staleness. Against the
        very scan the docs were derived from, nothing can be stale."""
        with open(os.path.join(_STATE["out"], "drift_report.json"), encoding="utf-8") as f:
            report = json.load(f)
        self.assertEqual({r["status"] for r in report["results"]}, {"unchanged"})

    def test_run_pipeline_local_driver_runs_end_to_end(self):
        """The driver's first test. It is the packaged form of this same
        series, exercised against the small checked-in fixture rather than
        paying for a second enterprise-scale scan."""
        with tempfile.TemporaryDirectory() as d:
            run_dir = os.path.join(d, "run")
            proc = _run([PY, "-m", "doc_engine.pipeline.local_runner",
                         os.path.join(SCRIPT_DIR, "fixtures", "spring_signals"),
                         "--out-dir", run_dir, "--skip-drift",
                         "--allow-mock"])
            self.assertEqual(proc.returncode, 0, proc.stdout[-4000:] + proc.stderr[-2000:])
            self.assertIn("RESULT: every gate passed", proc.stdout)
            cert_path = os.path.join(run_dir, "certification.json")
            self.assertTrue(os.path.isfile(cert_path))
            with open(cert_path, encoding="utf-8") as f:
                cert = json.load(f)
            self.assertTrue(
                cert.get("certified"),
                f"expected certified under --allow-mock; failures={cert.get('failures')}",
            )
            self.assertEqual(cert.get("generative_executor"), "mock")
            covering = os.path.join(run_dir, "covering_proof.json")
            signals_path = os.path.join(run_dir, "spring_signals.json")
            self.assertTrue(os.path.isfile(covering), "local_runner missing covering_proof.json")
            with open(signals_path, encoding="utf-8") as f:
                signals = json.load(f)
            with open(covering, encoding="utf-8") as f:
                proof = json.load(f)
            self.assertNotIn("_covering_proof", signals)
            ok, why = verify_covering_proof(
                proof,
                file_signatures=signals["file_signatures"],
                scanner_version=signals["scanner_version"],
            )
            self.assertTrue(ok, why)
