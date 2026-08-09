"""Cohesive suite from tests/doc_engine/test_enterprise_kitchen_sink.py: Ch12GateResponsibilityTest."""

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

class Ch12GateResponsibilityTest(unittest.TestCase):
    """Which layer is responsible for catching which defect — including the
    defects no layer catches.

    The zeros in this class are as load-bearing as the ones: a gate's scope is
    only meaningful if what falls outside it is also written down.
    """

    def _gate(self, docs, *extra):
        """Copied-docs form — see Ch01._gate for why the write check is off
        here. test_stray_write_* below drives the real in-repo path with the
        write check on."""
        return _run([PY, "-m", "doc_engine.tools.check_pipeline_output", docs,
                     "--target-repo", _STATE["repo"], "--no-write-check", *extra])

    def _coverage(self, docs, *extra):
        return _run([PY, "-m", "doc_engine.tools.citation_coverage", docs,
                     "--target-repo", _STATE["repo"], *extra])

    def _secrets(self, *paths):
        return _run([PY, "-m", "doc_engine.tools.check_no_secrets_leaked", *paths])

    def test_three_citation_defects_all_fail_the_gate(self):
        """Collapsed into one mutated copy and one subprocess — three distinct
        issue classes, one process."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(docs, "database.md")
        text = open(path, encoding="utf-8").read()
        text = text.replace("[Evidenced —", "[Evidenced -", 1)          # malformed
        text = re.sub(r"(\[Evidenced — [^\];]+?):(\d+)\]",
                      lambda m: f"{m.group(1)}:999999]", text, count=1)  # past EOF
        text += "\n- Fabricated [Evidenced — no/such/File.java:1].\n"    # nonexistent
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("malformed evidence tag", proc.stderr)
        self.assertIn("points past the end", proc.stderr)
        self.assertIn("does not exist under", proc.stderr)

    def test_extra_file_in_docs_fails_the_gate(self):
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        with open(os.path.join(docs, "notes.md"), "w", encoding="utf-8") as f:
            f.write("stray\n")
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("unexpected file in docs dir", proc.stderr)

    def test_duplicate_output_path_shows_up_as_a_missing_name(self):
        """Two writers handed the same output_path produce fourteen writes
        with one name duplicated and another missing — which a count check
        passes and the name-set check does not."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        shutil.copyfile(os.path.join(docs, "readme.md"), os.path.join(docs, "glossary.md"))
        os.remove(os.path.join(docs, "testing.md"))
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing expected doc: testing.md", proc.stderr)

    def test_stray_write_is_caught_and_no_write_check_removes_the_control(self):
        """The real in-repo path, with the write check genuinely on: it reads
        `git status --porcelain` in the target repo, so this exercises the
        actual mechanism rather than a stand-in."""
        stray = os.path.join(_STATE["repo"], "stray-written-by-a-subagent.txt")
        with open(stray, "w", encoding="utf-8") as f:
            f.write("a writer went outside docs/\n")
        self.addCleanup(lambda: os.path.exists(stray) and os.remove(stray))
        strict = _run([PY, "-m", "doc_engine.tools.check_pipeline_output", _STATE["docs"],
                       "--target-repo", _STATE["repo"]])
        self.assertEqual(strict.returncode, 1)
        self.assertIn("unexpected write outside the docs directory", strict.stderr)
        self.assertEqual(self._gate(_STATE["docs"]).returncode, 0,
                         "--no-write-check should remove exactly this control")

    def test_a_stray_write_into_a_gitignored_path_fails_the_gate(self):
        """Ignored untracked paths are checked via git ls-files -o -i."""
        ignored_dir = os.path.join(_STATE["repo"], GITIGNORED_DIR)
        os.makedirs(ignored_dir, exist_ok=True)
        stray = os.path.join(ignored_dir, "oops.md")
        with open(stray, "w", encoding="utf-8") as f:
            f.write("written outside docs/, into a gitignored directory\n")
        self.addCleanup(lambda: os.path.exists(stray) and os.remove(stray))
        proc = _run([PY, "-m", "doc_engine.tools.check_pipeline_output", _STATE["docs"],
                     "--target-repo", _STATE["repo"]])
        self.assertEqual(proc.returncode, 1,
                         "gate must report a write into a gitignored path")
        self.assertIn("gitignored path", proc.stderr)

    def test_citation_coverage_is_a_worklist_by_default_and_a_gate_under_strict(self):
        """Three finding kinds, one strict run: a miscased tag the Stage-4 gate
        cannot see, an untagged claim, and a re-anchored citation."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        _miscase_first_tag(self, os.path.join(docs, "database.md"))
        with open(os.path.join(docs, "operations.md"), "a", encoding="utf-8") as f:
            f.write("\nBillingController.save() writes to billing_invoice on every request.\n")
        self.assertEqual(self._coverage(docs).returncode, 0, "must be a worklist by default")
        strict = self._coverage(docs, "--strict")
        self.assertEqual(strict.returncode, 1)
        self.assertIn("miscased_tag", strict.stdout)
        self.assertIn("untagged_claim", strict.stdout)

    def test_planted_credentials_fail_the_secrets_check(self):
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        with open(os.path.join(docs, "configuration.md"), "a", encoding="utf-8") as f:
            f.write("\nLeaked: AKIAABCDEFGHIJKLMNOP\n-----BEGIN RSA PRIVATE KEY-----\n")
        proc = self._secrets(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("aws_access_key_id", proc.stderr)
        self.assertIn("pem_private_key", proc.stderr)

    def test_placeholder_values_must_not_fire(self):
        """Negative control. Flagging ${VAR}/CHANGEME would make the checker
        noise, and doc-taxonomy.md wants those written up as 'supplied at
        deploy time'."""
        scratch = tempfile.mkdtemp(prefix="ks_ph_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "configuration.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("password: ${DB_PASSWORD}\napi-key: CHANGEME\nsecret: <set-me>\n")
        self.assertEqual(self._secrets(path).returncode, 0)

    def test_a_secret_in_prose_is_caught_by_no_layer_at_all(self):
        """The one defect class nothing in this pipeline reports. A stated
        scope limit, not an unintended defect: the key-name heuristic needs the
        secret-shaped key to be the line's own key, so a value moved into
        narrative prose is invisible, and only AKIA/PEM are context-free.
        Pinned so that a change to the boundary is visible in the diff — if
        this starts failing, _secret_heuristics.py's docstring needs updating
        with it."""
        scratch = tempfile.mkdtemp(prefix="ks_prose_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "summaries.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump([{"summary": "The datasource password is hunter2literalvalue"}], f)
        self.assertEqual(self._secrets(path).returncode, 0)
