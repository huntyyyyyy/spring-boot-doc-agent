"""Cohesive suite from tests/doc_engine/test_partition_repo.py: BuildGroupsTest."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.core.excludes import load_gitignore_spec
from doc_engine.tools import partition_repo
SCRIPT_DIR = SCRIPTS_DIR

class BuildGroupsTest(unittest.TestCase):
    def test_single_group_when_everything_fits(self):
        file_tokens = [("a.py", 10), ("b.py", 20), ("c.py", 30)]
        groups = partition_repo.build_groups(file_tokens, max_tokens=1000, overlap_ratio=0.10)
        self.assertEqual(len(groups), 1)
        self.assertEqual([f for f, _ in groups[0]], ["a.py", "b.py", "c.py"])

    def test_empty_input(self):
        self.assertEqual(partition_repo.build_groups([], max_tokens=1000, overlap_ratio=0.10), [])

    def test_final_group_no_longer_unbounded(self):
        # Regression test for the exact bug the original review flagged:
        # "is_last_group_being_filled suppresses the size ceiling for the
        # final group." Six small (20-token) files up front let the early
        # groups close cheaply; twelve medium (90-token) files in the tail
        # give whichever group is presumed "last" far more than its fair
        # share to absorb.
        #
        # Since this test's original assertions were written, build_groups()
        # was swapped from check-after-append to check-before-append
        # ("strict") semantics — see the module docstring and the strict
        # replacement's own docstring for why. Under strict mode this exact
        # scenario (the handoff's own "Scenario A") now produces 15 groups
        # sized [100,40,20,90,90,90,90,90,90,90,90,90,90,90,90] instead of
        # the old algorithm's 14 groups with a 180-token final group — a
        # different shape, but the same underlying invariant this test
        # exists to protect (the last group is never an outlier vs. the
        # rest of the distribution) still holds, now with an even tighter
        # bound (max_tokens itself, not 1.8x it).
        file_tokens = [(f"small{i}.txt", 20) for i in range(6)] + [(f"big{i}.txt", 90) for i in range(12)]
        max_tokens = 100

        groups = partition_repo.build_groups(file_tokens, max_tokens, overlap_ratio=0.10)
        group_sizes = [sum(t for _, t in g) for g in groups]

        self.assertEqual(group_sizes, [100, 40, 20, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90])
        self.assertEqual(max(group_sizes), max_tokens, "final group must not be an outlier vs. the rest of the distribution")
        self.assertNotEqual(max(group_sizes), 270, "this is the exact unbounded-last-group value the pre-strict-swap code produced")

    def test_single_oversized_file_forms_its_own_group(self):
        # Can't split a file's tokens across groups — a single file bigger
        # than max_tokens must still end up somewhere, alone if necessary.
        # (Pre-existing behavior, unrelated to the last-group fix; guarded
        # here so a future change to the closing condition doesn't quietly
        # break it.)
        file_tokens = [("normal.py", 10), ("huge_generated.py", 5000)]
        groups = partition_repo.build_groups(file_tokens, max_tokens=100, overlap_ratio=0.10)
        files_in_groups = [f for g in groups for f, _ in g]
        self.assertIn("huge_generated.py", files_in_groups)

    def test_overlap_carries_trailing_files_into_next_group(self):
        file_tokens = [(f"f{i}.py", 10) for i in range(20)]
        groups = partition_repo.build_groups(file_tokens, max_tokens=100, overlap_ratio=0.10)
        self.assertGreater(len(groups), 1)
        first_group_files = [f for f, _ in groups[0]]
        second_group_files = [f for f, _ in groups[1]]
        overlap_files = set(first_group_files) & set(second_group_files)
        self.assertTrue(overlap_files, "expected at least one file carried from group 1 into group 2")

    def test_overlap_skips_oversized_trailing_file(self):
        # Regression test for a real bug found by validating build_groups()
        # against a real repo's file tree (see the review doc's "Resolution,
        # part 3"): the overlap-carry loop's stopping condition (`carried >=
        # overlap_budget`) is checked using the value of `carried` from
        # BEFORE the candidate item is added, so as long as the small items
        # scanned so far still leave it under budget, the loop takes one
        # more step back and force-includes whatever's there next - even a
        # single file far bigger than the entire next group's budget.
        #
        # Here, small.txt + giant.txt (900 tokens, 9x max_tokens) used to
        # close the first group under check-after-append. Carrying
        # giant.txt whole into the next group isn't "a bit of overlap" -
        # it's a duplicate of the entire file, and because that next group
        # now starts already past max_tokens before a single new file is
        # added, it closes again immediately and re-carries giant.txt
        # again. Verified against the unfixed build_groups(): this exact
        # scenario produced 3 groups with giant.txt in every one of them.
        #
        # Since this test was written, build_groups() was swapped to
        # check-before-append ("strict") semantics — see the module
        # docstring. Under strict mode, small.txt and giant.txt can no
        # longer even share a group (50 + 900 > 100), so each of the three
        # files ends up alone: [small.txt], [giant.txt], [after.txt]. The
        # duplication invariant this test protects still holds (giant.txt
        # appears exactly once, not chain-duplicated across groups) — the
        # group count changed because strict mode isolates the oversized
        # file instead of merging it with a small neighbor first.
        file_tokens = [("small.txt", 50), ("giant.txt", 900), ("after.txt", 30)]
        groups = partition_repo.build_groups(file_tokens, max_tokens=100, overlap_ratio=0.10)
        files_in_groups = [f for g in groups for f, _ in g]

        self.assertEqual(
            files_in_groups.count("giant.txt"), 1,
            "an oversized trailing file must not be duplicated into subsequent "
            f"groups via overlap carry; got groups: {[[f for f, _ in g] for g in groups]}",
        )
        self.assertEqual(len(groups), 3)
        self.assertEqual([[f for f, _ in g] for g in groups], [["small.txt"], ["giant.txt"], ["after.txt"]])

    def test_overlap_carry_does_not_re_carry_seed_files(self):
        """Files carried into a group must not be carried forward again at the next seam."""
        # Mimics cascade: small files where overlap tail is mostly seed carry.
        file_tokens = [
            ("a.java", 400),
            ("b.java", 400),
            ("c.java", 400),
            ("d.java", 400),
            ("e.java", 400),
        ]
        groups = partition_repo.build_groups(file_tokens, max_tokens=1000, overlap_ratio=0.10)
        membership: dict[str, set[int]] = {}
        for idx, group in enumerate(groups):
            for relpath, _ in group:
                membership.setdefault(relpath, set()).add(idx)
        for relpath, ids in membership.items():
            if len(ids) > 1:
                ordered = sorted(ids)
                self.assertEqual(ordered, [ordered[0], ordered[0] + 1],
                                 f"{relpath} spans non-adjacent groups: {ordered}")

    def test_strict_mode_zero_progress_guard_prevents_infinite_loop(self):
        """A group whose entire content gets carried forward unchanged,
        followed by a file that still doesn't fit even against that full
        carry, must not retry against unchanged state forever. Regression
        for the infinite loop found while porting build_groups() to
        check-before-append (strict) semantics."""
        file_tokens = [("only.txt", 90), ("trigger.txt", 95)]
        groups = partition_repo.build_groups(file_tokens, max_tokens=100, overlap_ratio=0.10)
        all_files = [f for g in groups for f, _ in g]
        self.assertIn("only.txt", all_files)
        self.assertIn("trigger.txt", all_files)
        for g in groups:
            total = sum(t for _, t in g)
            if total > 100:
                self.assertEqual(len(g), 1, f"group exceeds max_tokens with more than one file: {g}")
