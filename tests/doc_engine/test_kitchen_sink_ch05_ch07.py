"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: Ch05ConvergenceTest, Ch07LostUpdateTest."""

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

import pytest

pytestmark = pytest.mark.domain_integration

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

class Ch05ConvergenceTest(unittest.TestCase):
    """signals.file_signatures, groups.json's file union, manifest
    .file_signatures and cross_group_edges' node set are four derived copies
    of one fact — the repo's file set — produced by three different walk
    implementations. Where they must converge, assert it; where they provably
    diverge, pin the divergence so it is a known trade-off rather than a
    surprise."""

    def test_manifest_signatures_are_the_scan_signatures(self):
        self.assertEqual(_STATE["manifest"]["file_signatures"],
                         _STATE["signals"]["file_signatures"])

    def test_empty_file_hashes_to_the_known_empty_digest(self):
        self.assertEqual(_STATE["signals"]["file_signatures"][EMPTY_JAVA], EMPTY_SHA256)

    def test_edge_nodes_are_a_subset_of_grouped_files(self):
        grouped = _grouped(_STATE["groups"])
        referenced = set()
        for _gid, block in _STATE["edges"]["groups"].items():
            for arc in block.get("outbound", []) + block.get("inbound", []):
                for key in ("from", "to", "from_file", "to_file", "file"):
                    if isinstance(arc, dict) and isinstance(arc.get(key), str):
                        referenced.add(arc[key])
        self.assertEqual(referenced - grouped, set())

    def test_preflight_reuses_the_partition_rather_than_re_deriving_it(self):
        self.assertEqual(_STATE["preflight"]["num_groups"], _STATE["groups"]["num_groups"])

    def test_nul_file_diverges_between_the_two_walkers(self):
        """Deterministic disagreement: partition skips it as binary, the scan
        still hashes it."""
        self.assertNotIn(NUL_JAVA, _grouped(_STATE["groups"]))
        self.assertIn(NUL_JAVA, _STATE["signals"]["file_signatures"])

    def test_a_file_can_be_cited_as_evidence_yet_belong_to_no_group(self):
        """The sharpest divergence, and the first CLI-level exercise of
        --max-file-bytes. partition_repo.py enforces a size ceiling;
        spring_signal_scan.py has none. So above the ceiling a file is
        citable evidence in the final documentation that no Stage-1 subagent
        will ever summarize, and nothing in the pipeline reconciles that."""
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "groups.json")
            proc = _run([PY, "-m", "doc_engine.tools.partition_repo", _STATE["repo"],
                         "--max-tokens", MAX_TOKENS,
                         "--max-file-bytes", SMALL_FILE_BYTES, "--out", out])
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(out, encoding="utf-8") as f:
                small = json.load(f)
        skipped = {s["file"]: s["reason"] for s in small["skipped"]}
        self.assertIn(HUGE_JAVA, skipped)
        self.assertRegex(skipped[HUGE_JAVA], r"^too-large \(\d+ bytes\)$")
        self.assertNotIn(HUGE_JAVA, _grouped(small))
        self.assertIn(HUGE_JAVA, set(_evidence_files(_STATE["signals"])))

class Ch07LostUpdateTest(unittest.TestCase):

    def test_concurrent_read_modify_write_loses_an_update(self):
        """SKILL.md's concurrency contract — start-stage/end-stage exactly once
        per stage, orchestrating thread only — is load-bearing because this
        module has no locking, as its own docstring states. Demonstrated by
        replaying the forbidden interleaving deterministically rather than
        with threads: a racing test is a flaky test, and the interleaving is
        the point, not the race."""
        scratch = tempfile.mkdtemp(prefix="ks_lost_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "run_manifest.json")
        run_manifest._write_json_atomic(path, run_manifest.build_init_manifest(_STATE["repo"]))

        a = run_manifest._read_json(path)
        b = run_manifest._read_json(path)
        run_manifest.start_stage(a, "architect")
        run_manifest._write_json_atomic(path, a)
        run_manifest.start_stage(b, "doc_writer")
        run_manifest._write_json_atomic(path, b)

        names = [s["name"] for s in run_manifest._read_json(path)["stages"]]
        self.assertEqual(names, ["doc_writer"])
        self.assertNotIn("architect", names,
                         "if this now passes, run_manifest.py grew locking and "
                         "SKILL.md's concurrency contract can be relaxed")

    def test_a_failed_write_leaves_the_previous_manifest_intact(self):
        """Temp file plus os.replace, so a crash mid-write cannot leave a
        half-written manifest for the next stage's json.load(). Deterministic:
        the failure is injected, not waited for."""
        scratch = tempfile.mkdtemp(prefix="ks_atomic_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "run_manifest.json")
        run_manifest._write_json_atomic(path, run_manifest.build_init_manifest(_STATE["repo"]))
        before = open(path, "rb").read()

        with mock.patch.object(run_manifest.json, "dump",
                               side_effect=RuntimeError("disk full")):
            with self.assertRaises(RuntimeError):
                run_manifest._write_json_atomic(path, {"stages": [{"name": "x"}]})

        self.assertEqual(open(path, "rb").read(), before)
        json.loads(before.decode("utf-8"))
        leftovers = [n for n in os.listdir(scratch) if n != "run_manifest.json"]
        self.assertEqual(leftovers, [], f"temp file left behind: {leftovers}")

    def test_the_real_run_honored_the_once_per_stage_contract(self):
        names = [s["name"] for s in _STATE["manifest"]["stages"]]
        self.assertEqual(sorted(names), sorted([
            "architect", "doc_writer", "file_summarize",
            "gap_analysis_interview", "partition", "signal_scan"]))
        self.assertEqual(len(names), len(set(names)))
        for stage in _STATE["manifest"]["stages"]:
            with self.subTest(stage=stage["name"]):
                self.assertEqual(stage["status"], "complete")

    def test_manifest_is_never_observed_half_written(self):
        snapshots = _STATE["snapshots"]
        self.assertGreater(len(snapshots), 10)
        for name, data in snapshots:
            self.assertIn("stages", data, f"manifest malformed after {name}")
