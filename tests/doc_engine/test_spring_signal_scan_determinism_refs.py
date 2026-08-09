"""Scan determinism and references-bucket suites."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.scanning._resolve_lineage import _SQLLINEAGE_AVAILABLE
from doc_engine.scanning.facts import facts_from_signals
from doc_engine.tools import spring_signal_scan
SCRIPT_DIR = SCRIPTS_DIR
USE_SNAPSHOT = os.environ.get("SPRING_SIGNAL_USE_SNAPSHOT", "").lower() in ("1", "true", "yes")
SNAPSHOT_SCANNERS = ["filesystem", "ast-grep"]

class ScanDeterminismTest(unittest.TestCase):
    """Same input tree must produce byte-identical output.

    Everything downstream of the scanner hashes raw bytes —
    compute_file_signature(), run_manifest.json's file_signatures, and any
    future assertion that a run is reproducible. So 'the content is equal' is
    not the property that matters here; 'the serialization is equal' is. These
    tests assert the stronger one.
    """

    def test_two_scans_of_the_same_tree_serialize_identically(self):
        # Measured caveat, recorded so nobody reads more into a green result
        # here than it earns: when this was run against the unfixed scanner
        # (entity_table_map emitted in ast-grep match order), this test still
        # PASSED, while the ordering invariants above failed. Two scans inside
        # one process happened to see the same match order, so back-to-back
        # comparison did not expose the very defect it was written for.
        #
        # Keep it as a broad regression net for nondeterminism that does vary
        # per call, but the explicit sortedness assertions are the detectors
        # that actually work. A probe that only re-runs and diffs is weaker
        # than an invariant that names the property.
        first = spring_signal_scan.scan(str(FIXTURE_DIR), scanners=SNAPSHOT_SCANNERS)
        second = spring_signal_scan.scan(str(FIXTURE_DIR), scanners=SNAPSHOT_SCANNERS)
        self.assertEqual(
            json.dumps(first, indent=2, sort_keys=False),
            json.dumps(second, indent=2, sort_keys=False),
            "two scans of an unchanged tree produced different bytes",
        )

    def test_duplicate_class_name_is_contested_with_lowest_path_identity(self):
        """Path A stays simple-name keyed; facts get distinct symbols from package decls.

        Deviations: map rekeyed to FQCN; facts collapse to one subject; package
        invented from path instead of `package` declaration; lineage guesses.
        """
        from doc_engine.scanning.symbol import parse

        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        for pkg, table in (("pkg_a", "a_user"), ("pkg_b", "b_user")):
            pkg_dir = os.path.join(tmp, pkg)
            os.makedirs(pkg_dir)
            with open(os.path.join(pkg_dir, "User.java"), "w", encoding="utf-8") as fh:
                fh.write(
                    f"package com.example.{pkg};\n\n"
                    "import jakarta.persistence.*;\n\n"
                    "@Entity\n"
                    f'@Table(name = "{table}")\n'
                    "public class User {\n"
                    "    @Id\n"
                    "    private Long id;\n"
                    "}\n"
                )

        result = spring_signal_scan.scan(tmp, scanners=SNAPSHOT_SCANNERS)
        self.assertIn("User", result["entity_table_map"])
        self.assertNotIn("com.example.pkg_a.User", result["entity_table_map"])
        entry = result["entity_table_map"]["User"]
        self.assertEqual(entry["table"], "a_user")
        self.assertTrue(entry["file"].startswith("pkg_a"), entry["file"])
        self.assertEqual(entry["status"], "contested")
        self.assertEqual(
            {(c["file"], c["table"]) for c in entry["candidates"]},
            {("pkg_a/User.java", "a_user"), ("pkg_b/User.java", "b_user")},
        )
        self.assertEqual(
            {c.get("package") for c in entry["candidates"]},
            {"com.example.pkg_a", "com.example.pkg_b"},
        )

        again = spring_signal_scan.scan(tmp, scanners=SNAPSHOT_SCANNERS)["entity_table_map"]["User"]
        self.assertEqual(entry, again)

        lineage = spring_signal_scan.resolve_jpql_to_lineage(
            "SELECT u FROM User u", result["entity_table_map"]
        )
        self.assertFalse(lineage["available"])
        self.assertIn("contested", lineage["reason"])

        maps = [f for f in facts_from_signals(result) if f["predicate"] == "MAPS_TO"]
        self.assertEqual(len(maps), 2)
        self.assertEqual({f["object"] for f in maps}, {"a_user", "b_user"})
        subjects = {f["subject"] for f in maps}
        self.assertEqual(len(subjects), 2)
        self.assertEqual(
            {parse(s).namespaces for s in subjects},
            {("com", "example", "pkg_a"), ("com", "example", "pkg_b")},
        )
        self.assertTrue(all(f["qualifiers"].get("display_name") == "User" for f in maps))
        self.assertEqual(
            {f["qualifiers"].get("fqcn") for f in maps},
            {"com.example.pkg_a.User", "com.example.pkg_b.User"},
        )


class ReferencesBucketTest(unittest.TestCase):
    """references__import / references__package (spring_ast_grep_rules.yml)
    build a repo-wide import/package index so file-summarizer can find
    cross-group relationships its own per-group file view can't see (see
    the "references" rule block's header comment). Two files in different
    fictional "groups" (directories, standing in for partition_repo.py
    groups, which this scanner has no concept of) — groupA/Consumer.java
    importing groupB.Service — must produce a references__import entry
    for the import, independent of any group boundary."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        group_a = os.path.join(self.tmpdir, "groupA")
        group_b = os.path.join(self.tmpdir, "groupB")
        os.makedirs(group_a)
        os.makedirs(group_b)
        with open(os.path.join(group_a, "Consumer.java"), "w") as f:
            f.write(
                "package groupA;\n\n"
                "import groupB.Service;\n\n"
                "public class Consumer {\n"
                "    private final Service service = new Service();\n"
                "}\n"
            )
        with open(os.path.join(group_b, "Service.java"), "w") as f:
            f.write("package groupB;\n\npublic class Service {\n}\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_cross_group_import_appears_in_references_bucket(self):
        result = spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS)
        import_entries = [
            e for e in result["evidence"]["references"]
            if e["rule_id"] == "references__import" and e["file"] == "groupA/Consumer.java"
        ]
        self.assertEqual(len(import_entries), 1)
        self.assertIn("groupB.Service", import_entries[0]["match"])
