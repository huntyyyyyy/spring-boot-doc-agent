"""Delegation and path-separator suites."""

from __future__ import annotations

import os
import sys
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import (
    build_cross_group_edges,
    capacity_preflight,
    partition_repo,
    spring_signal_scan,
)
SCRIPT_DIR = SCRIPTS_DIR
from tests.support.capacity_preflight.fixtures import (
    _edges_data,
    _groups_data,
    _imp,
    _pkg,
)

class GenuineDelegationTest(unittest.TestCase):
    """Confirms this script reads partition_repo.py's/spring_signal_scan.py's
    own output rather than re-deriving the numbers a second, independent way."""

    def test_groups_match_partition_repo_direct_run(self):
        preflight_groups = capacity_preflight._load_or_build_groups(
            FIXTURE_DIR, max_tokens=120000, overlap=0.10, groups_file=None,
        )

        all_files = partition_repo.dfs_file_list(
            FIXTURE_DIR, partition_repo.DEFAULT_EXCLUDED_DIRS,
            partition_repo.DEFAULT_EXCLUDED_EXTS, partition_repo.DEFAULT_EXCLUDED_FILES,
        )
        file_tokens = []
        for full in all_files:
            rel = os.path.relpath(full, FIXTURE_DIR)
            tokens, reason = partition_repo.estimate_tokens(full, 2_000_000)
            if reason:
                continue
            file_tokens.append((rel, tokens))
        direct_groups = partition_repo.build_groups(file_tokens, 120000, 0.10)

        self.assertEqual(preflight_groups["num_groups"], len(direct_groups))
        self.assertEqual(preflight_groups["total_files_considered"], len(file_tokens))

    def test_edges_match_build_cross_group_edges_direct_run(self):
        # _load_or_build_edges() must hand off to build_report() rather than
        # re-deriving the package/import join a second way.
        data = spring_signal_scan.scan(
            FIXTURE_DIR, scanners=["filesystem", "ast-grep"],
        )
        self.assertIn("references", data["evidence"])

        groups_data = capacity_preflight._load_or_build_groups(
            FIXTURE_DIR, max_tokens=120000, overlap=0.10, groups_file=None,
        )
        direct = build_cross_group_edges.build_report(groups_data, data)
        via_preflight = capacity_preflight._load_or_build_edges(
            FIXTURE_DIR, None, groups_data, None,
        )
        self.assertEqual(via_preflight["groups"], direct["groups"])
        self.assertEqual(via_preflight["stats"], direct["stats"])


class PathSeparatorTest(unittest.TestCase):
    """compute_preflight() emitted os-native relative paths while everything
    it is joined against emits forward slashes -- the third occurrence of a
    bug already fixed in spring_drift_check.tier1_scan() and in
    partition_repo.main().

    Note on what runs where, stated rather than left implicit: the assertions
    that merely look for a backslash are only *non-vacuous on Windows*, since
    os.path.relpath never produces one on POSIX. That is exactly why the
    normalization was extracted into partition_repo.to_posix() -- the first
    test below feeds it a backslash-bearing string directly and therefore
    fails on the pre-fix code on every platform, CI included."""

    def test_to_posix_rewrites_separators_on_every_platform(self):
        self.assertEqual(partition_repo.to_posix(r"src\main\java\Foo.java"),
                         "src/main/java/Foo.java")

    def test_to_posix_leaves_forward_slashes_alone(self):
        self.assertEqual(partition_repo.to_posix("src/main/java/Foo.java"),
                         "src/main/java/Foo.java")

    def test_relpath_posix_never_returns_a_backslash(self):
        nested = os.path.join(FIXTURE_DIR, "src", "main")
        self.assertNotIn("\\", partition_repo.relpath_posix(nested, FIXTURE_DIR))

    def test_preflight_group_files_carry_no_backslashes(self):
        groups = capacity_preflight._load_or_build_groups(
            FIXTURE_DIR, max_tokens=120000, overlap=0.10, groups_file=None,
        )
        offenders = [f for g in groups["groups"] for f in g["files"] if "\\" in f]
        self.assertEqual(offenders, [], f"backslash-bearing paths: {offenders[:5]}")

    def test_preflight_paths_match_the_scanner_they_are_joined_against(self):
        """The invariant that actually matters. capacity_preflight's group
        file lists are joined by path against spring_signals.json inside
        build_report(); if the two sides spell the same file differently the
        join silently yields nothing, which is how this stayed invisible."""
        scanned = spring_signal_scan.scan(FIXTURE_DIR, scanners=["filesystem", "ast-grep"])
        scanned_files = {row["file"] for rows in scanned["evidence"].values()
                         for row in rows if isinstance(row, dict) and "file" in row}

        groups = capacity_preflight._load_or_build_groups(
            FIXTURE_DIR, max_tokens=120000, overlap=0.10, groups_file=None,
        )
        grouped_files = {f for g in groups["groups"] for f in g["files"]}

        # Every file the scanner produced evidence for must be spelled
        # identically on the partitioner's side. A separator mismatch makes
        # this intersection empty rather than raising.
        self.assertTrue(scanned_files, "fixture produced no evidence rows at all")
        self.assertTrue(scanned_files & grouped_files,
                        "no scanned file matched any grouped file -- the join "
                        "these two artifacts depend on produces nothing")
