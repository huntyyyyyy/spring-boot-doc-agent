"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: RealEnterpriseRepoTest."""

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

class RealEnterpriseRepoTest(unittest.TestCase):
    """Only assertions that hold for *any* Spring repo.

    Content-specific expectations (planted secrets, known entity names, exact
    counts) stay in the synthetic classes, since an arbitrary repo cannot
    satisfy them. Same opt-in shape as tests/doc_engine/test_partition_repo_real_world.py, so
    CI stays hermetic. Deliberately outside the CI runtime budget.
    """

    @classmethod
    def setUpClass(cls):
        repo = os.path.abspath(_kitchen_sink_real_repo() or "")
        if not os.path.isdir(repo):
            raise unittest.SkipTest(f"real repo {repo!r} is not a directory")
        cls.repo = repo
        cls.scratch = tempfile.mkdtemp(prefix="ks_real_")
        cls.out = os.path.join(cls.scratch, "run")
        cls.proc = _run([PY, "-m", "doc_engine.pipeline.local_runner", repo,
                         "--out-dir", cls.out, "--skip-drift"])
        with open(os.path.join(cls.out, "spring_signals.json"), encoding="utf-8") as f:
            cls.signals = json.load(f)
        with open(os.path.join(cls.out, "groups.json"), encoding="utf-8") as f:
            cls.groups = json.load(f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.scratch, ignore_errors=True)

    def test_chain_completes_and_gates_pass(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout[-4000:])

    def test_evidence_buckets_are_sorted(self):
        for bucket, rows in (self.signals.get("evidence") or {}).items():
            with self.subTest(bucket=bucket):
                self.assertEqual(rows, sorted(rows, key=lambda e: (e["file"], e.get("line", 0))))

    def test_entity_index_keys_are_sorted(self):
        keys = list(self.signals["entity_table_map"])
        self.assertEqual(keys, sorted(keys))

    def test_no_excluded_directory_leaked(self):
        pool = _grouped(self.groups) | set(_evidence_files(self.signals))
        for d in DEFAULT_EXCLUDED_DIRS:
            with self.subTest(excluded=d):
                self.assertEqual([f for f in pool if _has_segment(f, d)], [])

    def test_overlap_is_adjacent_only(self):
        """Overlap must stay between adjacent groups on the opt-in mid-size lane.

        Regression for CONSTRAINTS.md §6: carry_forward skips paths that
        entered a group only via prior overlap (carried_in_paths). Requires
        KITCHEN_SINK_REPO (class skips otherwise).
        """
        where = {}
        for g in self.groups["groups"]:
            for f in g["files"]:
                where.setdefault(f, set()).add(g["id"])
        for f, ids in where.items():
            if len(ids) > 1:
                with self.subTest(file=f):
                    self.assertEqual(ids, {min(ids), min(ids) + 1})

    def test_contested_entity_keys_are_well_formed(self):
        """Every contested entity_table_map entry must carry candidates and
        refuse JPQL lineage rather than guessing a table. Vacuous-pass when
        the target repo has no simple-name collisions (observed on the
        in-tree mid-size service checkout: 0 contested / 53 entities)."""
        contested = {
            name: entry for name, entry in self.signals["entity_table_map"].items()
            if entry.get("status") == "contested"
        }
        for name, entry in contested.items():
            with self.subTest(entity=name):
                self.assertGreaterEqual(len(entry.get("candidates") or []), 2)
                tables = {c["table"] for c in entry["candidates"]}
                files = {c["file"] for c in entry["candidates"]}
                self.assertEqual(len(files), len(entry["candidates"]))
                lineage = spring_signal_scan.resolve_jpql_to_lineage(
                    f"SELECT x FROM {name} x", self.signals["entity_table_map"]
                )
                self.assertFalse(lineage["available"])
                self.assertIn("contested", lineage["reason"])
                # Citation-identity table must be one of the candidates, not
                # an invented third name.
                self.assertIn(entry["table"], tables)

    def test_multi_hyphen_application_profiles_reach_config_key_sets(self):
        """Every application*-*.yml/properties on disk with ≥2 hyphens in the
        filename must appear in config_key_sets (the CONSTRAINTS §7 fix).
        Vacuous when the checkout has none (observed: 0 multi-hyphen stems
        among 12 application* configs on the in-tree mid-size service)."""
        on_disk = []
        for dirpath, _dirnames, filenames in os.walk(self.repo):
            for name in filenames:
                lower = name.lower()
                if not (lower.startswith("application") and (
                        lower.endswith(".yml") or lower.endswith(".yaml")
                        or lower.endswith(".properties"))):
                    continue
                if name.count("-") >= 2:
                    rel = os.path.relpath(os.path.join(dirpath, name), self.repo)
                    on_disk.append(rel.replace("\\", "/"))
        keys = self.signals.get("config_key_sets") or {}
        for rel in on_disk:
            with self.subTest(file=rel):
                self.assertIn(rel, keys)

    def test_fault_injection_holds_on_real_output(self):
        """The most valuable part of the real lane: the gate topology proven
        against real-shaped documentation, not templated mock prose."""
        scratch = tempfile.mkdtemp(prefix="ks_real_docs_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        copy = os.path.join(scratch, "docs")
        shutil.copytree(os.path.join(self.out, "docs"), copy)
        os.remove(os.path.join(copy, "testing.md"))
        proc = _run([PY, "-m", "doc_engine.tools.check_pipeline_output", copy,
                     "--target-repo", self.repo, "--no-write-check"])
        self.assertEqual(proc.returncode, 1)
