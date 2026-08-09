"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: Ch06PartitioningTest."""

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

class Ch06PartitioningTest(unittest.TestCase):

    def setUp(self):
        self.groups = _STATE["groups"]
        self.max_tokens = self.groups["max_tokens_per_group"]

    def _membership(self):
        where = {}
        for g in self.groups["groups"]:
            for f in g["files"]:
                where.setdefault(f, set()).add(g["id"])
        return where

    def test_overlap_never_spans_more_than_two_groups(self):
        """Overlap must stay between adjacent groups only — no cascade into three."""
        for f, ids in self._membership().items():
            if len(ids) > 1:
                with self.subTest(file=f):
                    self.assertEqual(ids, {min(ids), min(ids) + 1})

    def test_every_file_lands_in_at_least_one_group(self):
        """The invariant that must hold regardless of the cascade above:
        overlap may duplicate, but it must never drop."""
        skipped = {s["file"] for s in self.groups["skipped"]}
        repo = _STATE["repo"]
        # dfs_file_list yields absolute paths; groups.json carries them
        # relative and forward-slashed. docs/ is excluded because the run
        # wrote it *after* partitioning.
        walked = {os.path.relpath(w, repo).replace(os.sep, "/")
                  for w in partition_repo.dfs_file_list(
                      repo, DEFAULT_EXCLUDED_DIRS,
                      partition_repo.DEFAULT_EXCLUDED_EXTS,
                      partition_repo.DEFAULT_EXCLUDED_FILES)}
        walked = {w for w in walked if not w.startswith("docs/")}
        self.assertEqual(walked - set(self._membership()) - skipped, set())

    def test_build_groups_terminates_across_a_range_of_budgets(self):
        """REGRESSION — build_groups used to hang outright.

        The zero-progress guard only re-checked the hard cap, so a carry that
        was itself large enough to re-trip the *soft target* looped forever:
        the same file was re-evaluated against an identical group, `i` never
        advanced, and the group list grew without bound. Reproduced with a
        2916-token file at --max-tokens 3000 (target_per_group 2901): 2927
        groups and climbing before the probe was killed.

        Run in a subprocess with a hard timeout, because the failure mode is a
        hang — an in-process assertion would take the whole suite down with it
        rather than reporting.
        """
        # noqa UP031: the %-formatting here is deliberate and not a style
        # holdover. This string is *source code* for a subprocess, and %r
        # renders the path as a valid Python literal with quoting and
        # backslash escaping already correct -- which matters on Windows,
        # where an f-string would interpolate C:\Users\... raw and produce a
        # probe that fails to parse.
        probe = (  # noqa: UP031
            "import os\n"
            "from doc_engine.tools import partition_repo as pr\n"
            "from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS as D\n"
            "repo = %r\n"
            "files = list(pr.dfs_file_list(repo, D, pr.DEFAULT_EXCLUDED_EXTS,"
            " pr.DEFAULT_EXCLUDED_FILES))\n"
            "ft = []\n"
            "for rel in files:\n"
            "    t, r = pr.estimate_tokens(os.path.join(repo, rel.replace('/', os.sep)),"
            " 2000000)\n"
            "    if r is None: ft.append((rel, t))\n"
            "for mt in (1000, 2000, 3000, 4000, 5000, 8000, 120000):\n"
            "    g = pr.build_groups(ft, mt, 0.10)\n"
            "    seen = {f for grp in g for f, _ in grp}\n"
            "    assert seen == {f for f, _ in ft}, mt\n"
            "print('OK')\n"
        ) % (_STATE["repo"],)
        try:
            proc = subprocess.run([PY, "-c", probe], capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            self.fail("build_groups did not terminate — the zero-progress guard "
                      "regressed (see this test's docstring)")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_group_token_counts_are_internally_consistent(self):
        for g in self.groups["groups"]:
            with self.subTest(group=g["id"]):
                total = 0
                for rel in g["files"]:
                    tokens, reason = partition_repo.estimate_tokens(
                        os.path.join(_STATE["repo"], rel.replace("/", os.sep)), 2_000_000)
                    self.assertIsNone(reason)
                    total += tokens
                self.assertEqual(g["est_tokens"], total)

    def test_a_hot_spot_gets_its_own_group_rather_than_inflating_a_shared_one(self):
        for g in self.groups["groups"]:
            if g["est_tokens"] > self.max_tokens:
                with self.subTest(group=g["id"]):
                    self.assertEqual(len(g["files"]), 1)

    def test_skew_is_actually_present(self):
        """Guards the guard: if the fixture stopped being lopsided, the
        hot-spot test above would pass vacuously."""
        sizes = [g["est_tokens"] for g in self.groups["groups"]]
        self.assertGreater(len(sizes), 1)
        self.assertGreater(max(sizes), 2 * (sum(sizes) / len(sizes)))

    def test_no_excluded_directory_is_scanned_grouped_or_cited(self):
        """Segment-wise, not substring — 'out' must not match
        'outbound/Client.java'. This is also the first assertion anywhere in
        this repo that excluded dirs stay out of groups.json."""
        grouped = _grouped(self.groups)
        cited = set(_evidence_files(_STATE["signals"]))
        signed = set(_STATE["signals"]["file_signatures"])
        entities = {v["file"] for v in _STATE["signals"]["entity_table_map"].values()}
        for d in PLANTED_EXCLUDED_DIRS:
            for collection, label in ((grouped, "groups"), (cited, "evidence"),
                                      (signed, "file_signatures"),
                                      (entities, "entity_table_map")):
                with self.subTest(excluded=d, where=label):
                    self.assertEqual([f for f in collection if _has_segment(f, d)], [])

    def test_group_file_lists_are_dfs_preorder_not_sorted(self):
        """A deliberate inverse assertion. dfs_file_list emits a directory's
        own files before recursing into its subdirectories, so a root-level
        file precedes everything nested regardless of lexicographic order.
        Asserting sortedness here would assert a falsehood; this documents the
        contract and fails loudly if someone "fixes" the ordering."""
        unsorted = [g["id"] for g in self.groups["groups"]
                    if g["files"] != sorted(g["files"])]
        self.assertTrue(unsorted, "no group was DFS-ordered — fixture shape changed")
