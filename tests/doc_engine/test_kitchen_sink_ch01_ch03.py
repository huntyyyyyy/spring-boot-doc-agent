"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: Ch01FaultInjectionTest, Ch03DerivedIndexTest."""

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

class Ch01FaultInjectionTest(unittest.TestCase):
    """The suite's thesis.

    DDIA Ch.1 distinguishes a fault (a component deviating from spec) from a
    failure (the system stopping service), and argues for deliberately
    inducing faults, because an untriggered fault-tolerance mechanism is
    indistinguishable from one that does not work. Applied here: before this
    class, nothing proved a corrupted run actually fails.
    """

    def _gate(self, docs, *extra):
        # --no-write-check because these run against a *copy* of docs/ that
        # lives outside the target repo. With docs elsewhere the write check
        # asserts nothing in the repo changed, which the run's own real docs/
        # legitimately violates. The write check gets its own dedicated test
        # in Ch12, against the real in-repo path.
        return _run([PY, "-m", "doc_engine.tools.check_pipeline_output", docs,
                     "--target-repo", _STATE["repo"], "--no-write-check", *extra])

    def test_clean_output_passes(self):
        """The control. Without it every assertion below could pass for the
        wrong reason."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_a_missing_doc_becomes_a_process_failure(self):
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        os.remove(os.path.join(docs, "testing.md"))
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing expected doc: testing.md", proc.stderr)

    def test_a_miscased_tag_is_a_fault_that_never_becomes_a_failure(self):
        """Deliberately adjacent to the test above: the same magnitude of
        defect, and the gate the pipeline actually blocks on returns 0. A
        lowercase tag word matches neither the valid patterns nor the
        malformed-span detector, so the citation is scored as absent
        everywhere. Fault without failure — the contrast is the point."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        _miscase_first_tag(self, os.path.join(docs, "database.md"))
        self.assertEqual(self._gate(docs).returncode, 0)

    def test_operator_error_exits_two_not_one(self):
        """Exit 2 (the checker could not run) is a different condition from
        exit 1 (the run is bad). A caller that collapses them loses that."""
        proc = self._gate(os.path.join(_STATE["tmp"], "no-such-dir"))
        self.assertEqual(proc.returncode, 2)

class Ch03DerivedIndexTest(unittest.TestCase):
    """entity_table_map is an index over evidence.persistence keyed by bare
    class name — package deliberately excluded, so the key is not unique.
    "Two entities in one file" is an index-build question; the cross-module
    name clash is a key-resolution question."""

    def setUp(self):
        self.signals = _STATE["signals"]
        self.mapping = self.signals["entity_table_map"]

    def test_two_entities_in_one_file_resolve_to_their_own_tables(self):
        """README.md's stated fix — each entity's own @Table, rather than the
        first @Table in the file paired with the first class in it. Untested
        until now: no other fixture has two entity classes in one file."""
        self.assertIn("Alpha", self.mapping)
        self.assertIn("Beta", self.mapping)
        self.assertEqual(self.mapping["Alpha"]["table"], "alpha_tbl")
        self.assertEqual(self.mapping["Beta"]["table"], "beta_tbl")
        self.assertEqual(self.mapping["Alpha"]["file"], TWO_ENTITIES)
        self.assertEqual(self.mapping["Beta"]["file"], TWO_ENTITIES)

    def test_entity_without_its_own_table_does_not_borrow_a_siblings(self):
        """The sharper form: Delta has no @Table, so it must fall back to
        inferred default naming rather than scavenging Gamma's explicit one."""
        self.assertEqual(self.mapping["Gamma"]["table"], "gamma_explicit")
        self.assertIn("Delta", self.mapping)
        self.assertNotEqual(self.mapping["Delta"]["table"], "gamma_explicit")
        self.assertEqual(self.mapping["Delta"]["table"], "delta")

    def test_non_unique_key_collision_is_contested_and_deterministic(self):
        """Same bare class name in two modules. The evidence bucket keeps both
        rows; the index keeps one citation-identity entry keyed by lowest file
        path, marked status=contested with both candidates listed so JPQL
        lineage can refuse rather than guess."""
        entry = self.mapping["Invoice"]
        self.assertEqual(entry["file"], min(DUP_BILLING, DUP_LEDGER))
        self.assertEqual(entry["status"], "contested")
        self.assertEqual(
            {(c["file"], c["table"]) for c in entry["candidates"]},
            {(DUP_BILLING, "billing_invoice"), (DUP_LEDGER, "ledger_invoice")},
        )
        rows = {r["file"] for r in self.signals["evidence"]["persistence"]
                if r.get("class_name") == "Invoice"}
        self.assertEqual(rows, {DUP_BILLING, DUP_LEDGER},
                         "the index may drop a row; the evidence bucket must not")
        jpql = [e for e in self.signals["evidence"]["raw_queries"]
                if e.get("query_kind") == "jpql" and "Invoice" in (e.get("query") or "")]
        self.assertTrue(jpql, "fixture must include JPQL over the contested name")
        for e in jpql:
            self.assertFalse(e["lineage"]["available"], e)
            self.assertIn("contested", e["lineage"]["reason"])

    def test_nested_entity_holder_scavenges_inner_table_today(self):
        """Characterizes nested @Entity under stopBy:end — both InnerEntity and
        non-@Entity NestedEntityHolder currently map to nested_inner (scavenge).
        Not endorsed; pin so a silent change is visible."""
        self.assertEqual(self.mapping["InnerEntity"]["table"], "nested_inner")
        self.assertEqual(self.mapping["InnerEntity"]["file"], NESTED_ENTITY)
        self.assertEqual(
            self.mapping["NestedEntityHolder"]["table"], "nested_inner"
        )
        self.assertEqual(self.mapping["NestedEntityHolder"]["file"], NESTED_ENTITY)

    def test_index_keys_are_sorted_and_every_entry_resolves(self):
        keys = list(self.mapping)
        self.assertEqual(keys, sorted(keys))
        for name, entry in self.mapping.items():
            with self.subTest(entity=name):
                self.assertTrue(os.path.isfile(
                    os.path.join(_STATE["repo"], entry["file"].replace("/", os.sep))))
