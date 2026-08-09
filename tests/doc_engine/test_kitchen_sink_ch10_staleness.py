"""Kitchen-sink Ch10 staleness drift."""

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

class Ch10StalenessTest(unittest.TestCase):
    """Drift as a staleness detector, on a copy so mutation cannot perturb the
    artifacts every other class reads (and so test order stays irrelevant)."""

    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.mkdtemp(prefix="ks_drift_")
        cls.repo = os.path.join(cls.scratch, "repo")
        shutil.copytree(_STATE["repo"], cls.repo)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.scratch, ignore_errors=True)

    def _drift(self):
        out = os.path.join(self.scratch, "drift.json")
        proc = _run([PY, "-m", "doc_engine.tools.spring_drift_check", self.repo,
                     os.path.join(_STATE["out"], "spring_signals.json"),
                     "--manifest", os.path.join(_STATE["out"], "run_manifest.json"),
                     "--out", out])
        self.assertIn(proc.returncode, (0, 1), proc.stdout + proc.stderr)
        with open(out, encoding="utf-8") as f:
            return json.load(f)

    def _statuses(self, report, rel):
        return {r["status"] for r in report["results"] if r.get("file") == rel}

    def _mutate(self, rel, old, new):
        path = os.path.join(self.repo, rel.replace("/", os.sep))
        text = open(path, encoding="utf-8").read()
        self.addCleanup(lambda: open(path, "w", encoding="utf-8", newline="\n").write(text))
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text.replace(old, new) if old else text + new)

    def test_renamed_table_drifts_its_citation(self):
        self._mutate(TWO_ENTITIES, 'name = "alpha_tbl"', 'name = "alpha_renamed"')
        self.assertIn("drifted", self._statuses(self._drift(), TWO_ENTITIES))

    def test_deleted_file_marks_its_citations_deleted(self):
        path = os.path.join(self.repo, DUP_LEDGER.replace("/", os.sep))
        text = open(path, encoding="utf-8").read()
        os.remove(path)
        self.addCleanup(lambda: open(path, "w", encoding="utf-8", newline="\n").write(text))
        self.assertIn("file_deleted", self._statuses(self._drift(), DUP_LEDGER))

    def test_config_value_only_change_is_flagged_for_review(self):
        """The enterprise case this outcome exists for: checked-in config is a
        placeholder and real values arrive at deploy time, so a value moving
        under an unchanged key means something unusual happened."""
        self._mutate(SECRETS_YML, "hunter2literalvalue", "differentliteralvalue")
        self.assertIn("config_values_only_changed_review_needed",
                      self._statuses(self._drift(), SECRETS_YML))

    def test_added_config_key_is_structural_drift(self):
        self._mutate(SECRETS_YML, None, "extra:\n  added: 1\n")
        self.assertIn("config_structure_changed",
                      self._statuses(self._drift(), SECRETS_YML))
