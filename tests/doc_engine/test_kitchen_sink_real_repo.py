"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: RealEnterpriseRepoTest."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest

import pytest

from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS
from doc_engine.tools import spring_signal_scan
from tests.conftest import SCRIPTS_DIR
from tests.support.kitchen_sink.harness import (
    _evidence_files,
    _grouped,
    _has_segment,
    _kitchen_sink_real_repo,
    _run,
)

pytestmark = pytest.mark.domain_integration

PY = sys.executable
SCRIPT_DIR = SCRIPTS_DIR  # retained for kitchen-sink suite cohesion


class RealEnterpriseRepoTest(unittest.TestCase):
    """Only assertions that hold for *any* Spring repo.

    Content-specific expectations stay in the synthetic classes. Same opt-in
    shape as ``test_partition_repo_real_world`` so CI stays hermetic when the
    real-repo env is unset (class skips).
    """

    @classmethod
    def setUpClass(cls):
        repo = os.path.abspath(_kitchen_sink_real_repo() or "")
        if not os.path.isdir(repo):
            raise unittest.SkipTest(f"real repo {repo!r} is not a directory")
        cls.repo = repo
        cls.scratch = tempfile.mkdtemp(prefix="ks_real_")
        cls.out = os.path.join(cls.scratch, "run")
        cls.proc = _run(
            [
                PY,
                "-m",
                "doc_engine.pipeline.local_runner",
                repo,
                "--out-dir",
                cls.out,
                "--skip-drift",
                "--allow-mock",
            ]
        )
        with open(os.path.join(cls.out, "spring_signals.json"), encoding="utf-8") as handle:
            cls.signals = json.load(handle)
        with open(os.path.join(cls.out, "groups.json"), encoding="utf-8") as handle:
            cls.groups = json.load(handle)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.scratch, ignore_errors=True)

    def test_chain_completes_and_gates_pass(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout[-4000:])

    def test_evidence_buckets_are_sorted(self):
        for bucket, rows in (self.signals.get("evidence") or {}).items():
            with self.subTest(bucket=bucket):
                self.assertEqual(
                    rows, sorted(rows, key=lambda row: (row["file"], row.get("line", 0)))
                )

    def test_entity_index_keys_are_sorted(self):
        keys = list(self.signals["entity_table_map"])
        self.assertEqual(keys, sorted(keys))

    def test_no_excluded_directory_leaked(self):
        pool = _grouped(self.groups) | set(_evidence_files(self.signals))
        for excluded in DEFAULT_EXCLUDED_DIRS:
            with self.subTest(excluded=excluded):
                self.assertEqual(
                    [path for path in pool if _has_segment(path, excluded)], []
                )

    def test_overlap_is_adjacent_only(self):
        """Overlap must stay between adjacent groups (CONSTRAINTS.md §6)."""
        where: dict[str, set[int]] = {}
        for group in self.groups["groups"]:
            for path in group["files"]:
                where.setdefault(path, set()).add(group["id"])
        for path, ids in where.items():
            if len(ids) > 1:
                with self.subTest(file=path):
                    self.assertEqual(ids, {min(ids), min(ids) + 1})

    def test_contested_entity_keys_are_well_formed(self):
        contested = {
            name: entry
            for name, entry in self.signals["entity_table_map"].items()
            if entry.get("status") == "contested"
        }
        for name, entry in contested.items():
            with self.subTest(entity=name):
                self.assertGreaterEqual(len(entry.get("candidates") or []), 2)
                tables = {candidate["table"] for candidate in entry["candidates"]}
                files = {candidate["file"] for candidate in entry["candidates"]}
                self.assertEqual(len(files), len(entry["candidates"]))
                lineage = spring_signal_scan.resolve_jpql_to_lineage(
                    f"SELECT x FROM {name} x", self.signals["entity_table_map"]
                )
                self.assertFalse(lineage["available"])
                self.assertIn("contested", lineage["reason"])
                self.assertIn(entry["table"], tables)

    def test_multi_hyphen_application_profiles_reach_config_key_sets(self):
        on_disk = []
        for dirpath, _dirnames, filenames in os.walk(self.repo):
            for name in filenames:
                lower = name.lower()
                if not (
                    lower.startswith("application")
                    and (
                        lower.endswith(".yml")
                        or lower.endswith(".yaml")
                        or lower.endswith(".properties")
                    )
                ):
                    continue
                if name.count("-") >= 2:
                    rel = os.path.relpath(os.path.join(dirpath, name), self.repo)
                    on_disk.append(rel.replace("\\", "/"))
        keys = self.signals.get("config_key_sets") or {}
        for rel in on_disk:
            with self.subTest(file=rel):
                self.assertIn(rel, keys)

    def test_fault_injection_holds_on_real_output(self):
        scratch = tempfile.mkdtemp(prefix="ks_real_docs_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        copy = os.path.join(scratch, "docs")
        shutil.copytree(os.path.join(self.out, "docs"), copy)
        os.remove(os.path.join(copy, "testing.md"))
        proc = _run(
            [
                PY,
                "-m",
                "doc_engine.tools.check_pipeline_output",
                copy,
                "--target-repo",
                self.repo,
                "--no-write-check",
            ]
        )
        self.assertEqual(proc.returncode, 1)
