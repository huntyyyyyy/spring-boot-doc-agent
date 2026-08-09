"""Kitchen-sink Ch06 partitioning."""

from __future__ import annotations

import os
import subprocess

import pytest

from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS
from doc_engine.tools import partition_repo
from tests.support.kitchen_sink.constants import PLANTED_EXCLUDED_DIRS, PY
from tests.support.kitchen_sink.harness import _evidence_files, _grouped, _has_segment
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch06PartitioningTest(KitchenBoundTestCase):

    def setUp(self):
        self.groups = self.kitchen.groups
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
        repo = self.kitchen.repo
        # dfs_file_list yields absolute paths; groups.json carries them
        # relative and forward-slashed. docs/ is excluded because the run
        # wrote it *after* partitioning.
        walked = {
            os.path.relpath(w, repo).replace(os.sep, "/")
            for w in partition_repo.dfs_file_list(
                repo,
                DEFAULT_EXCLUDED_DIRS,
                partition_repo.DEFAULT_EXCLUDED_EXTS,
                partition_repo.DEFAULT_EXCLUDED_FILES,
            )
        }
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
        ) % (self.kitchen.repo,)
        try:
            proc = subprocess.run(
                [PY, "-c", probe],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            self.fail(
                "build_groups did not terminate — the zero-progress guard "
                "regressed (see this test's docstring)"
            )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("OK", proc.stdout)

    def test_group_token_counts_are_internally_consistent(self):
        for g in self.groups["groups"]:
            with self.subTest(group=g["id"]):
                total = 0
                for rel in g["files"]:
                    tokens, reason = partition_repo.estimate_tokens(
                        os.path.join(
                            self.kitchen.repo, rel.replace("/", os.sep)
                        ),
                        2_000_000,
                    )
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
        cited = set(_evidence_files(self.kitchen.signals))
        signed = set(self.kitchen.signals["file_signatures"])
        entities = {
            v["file"] for v in self.kitchen.signals["entity_table_map"].values()
        }
        for d in PLANTED_EXCLUDED_DIRS:
            for collection, label in (
                (grouped, "groups"),
                (cited, "evidence"),
                (signed, "file_signatures"),
                (entities, "entity_table_map"),
            ):
                with self.subTest(excluded=d, where=label):
                    self.assertEqual(
                        [f for f in collection if _has_segment(f, d)], []
                    )

    def test_group_file_lists_are_dfs_preorder_not_sorted(self):
        """A deliberate inverse assertion. dfs_file_list emits a directory's
        own files before recursing into its subdirectories, so a root-level
        file precedes everything nested regardless of lexicographic order.
        Asserting sortedness here would assert a falsehood; this documents the
        contract and fails loudly if someone "fixes" the ordering."""
        unsorted = [
            g["id"]
            for g in self.groups["groups"]
            if g["files"] != sorted(g["files"])
        ]
        self.assertTrue(unsorted, "no group was DFS-ordered — fixture shape changed")
