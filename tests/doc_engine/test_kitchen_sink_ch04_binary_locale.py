"""Kitchen-sink encoding binary/locale edges."""

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

class Ch04EncodingTestContinued(unittest.TestCase):
    def setUp(self):
            self.signals = _STATE["signals"]
            self.groups = _STATE["groups"]

    def _skip_reason(self, rel):
            for s in self.groups["skipped"]:
                if s["file"] == rel:
                    return s["reason"]
            return None

    def test_nul_byte_file_is_skipped_as_binary(self):
            self.assertEqual(self._skip_reason(NUL_JAVA), "binary")

    def test_zero_byte_java_costs_exactly_one_token(self):
            self.assertIn(EMPTY_JAVA, _grouped(self.groups))
            self.assertIsNone(self._skip_reason(EMPTY_JAVA))
            tokens, reason = partition_repo.estimate_tokens(
                os.path.join(_STATE["repo"], EMPTY_JAVA.replace("/", os.sep)), 2_000_000)
            self.assertEqual((tokens, reason), (1, None))

    def test_zero_byte_config_is_absent_rather_than_present_and_empty(self):
            self.assertNotIn(EMPTY_YML, self.signals["config_key_sets"])
            self.assertNotIn(EMPTY_YML, self.signals["redaction_zones"])

    def test_build_gradle_signals_extracted(self):
            """Build scripts are now structurally read for plugins, dependencies,
            and toolchains — not just classified by filename."""
            deployment = self.signals["evidence"]["deployment"]
            plugins = [r for r in deployment if r.get("rule_id") == "deployment__build_plugin"]
            self.assertEqual(
                {(p["plugin_id"], p["plugin_version"]) for p in plugins},
                {("org.springframework.boot", "3.2.0"), ("java", None)},
            )
            deps = [r for r in deployment if r.get("rule_id") == "deployment__build_dependency"]
            self.assertIn(
                ("implementation", "org.springframework.boot", "spring-boot-starter-web"),
                {(d["configuration"], d["coordinate"].get("group"), d["coordinate"].get("name")) for d in deps},
            )
            tcs = [r for r in deployment if r.get("rule_id") == "deployment__build_toolchain"]
            self.assertEqual(tcs[0]["toolchain_value"], "17")
            mods = [r for r in deployment if r.get("rule_id") == "deployment__build_module"]
            self.assertEqual({m["module"] for m in mods}, {"billing", "ledger"})
            catalogs = [r for r in deployment if r.get("rule_id") == "deployment__version_catalog"]
            self.assertEqual({c["catalog_kind"] for c in catalogs}, {"version", "library"})

    def test_non_ascii_source_is_neither_dropped_nor_mangled(self):
            matches = [row.get("match", "")
                       for rows in (self.signals.get("evidence") or {}).values()
                       for row in rows]
            blob = "\n".join(matches)
            self.assertNotIn("Ã", blob, "mojibake in evidence match text")
            self.assertNotIn("�", blob, "replacement chars in evidence match text")

    def test_scan_survives_non_ascii_under_a_non_utf8_locale(self):
            """Regression test for the locale-codec decode of ast-grep's stdout.
            ast-grep emits UTF-8; decoded with the locale's preferred encoding a
            character whose UTF-8 contains 0x81/0x8D/0x8F/0x90/0x9D (Á is C3 81,
            с is D1 81) raises UnicodeDecodeError and kills the scan, while é/日
            degrade to silent mojibake. Forcing an ASCII/cp1252 locale in the
            child reproduces the original conditions exactly."""
            env = dict(os.environ)
            env.update({"LC_ALL": "C", "LANG": "C", "PYTHONUTF8": "0",
                        "PYTHONCOERCECLOCALE": "0"})
            # Scoped to a one-file tree rather than the whole fixture: it isolates
            # the variable under test and keeps a full second ast-grep pass out of
            # the suite's runtime.
            with tempfile.TemporaryDirectory() as d:
                mini = os.path.join(d, "repo")
                shutil.copytree(os.path.join(_STATE["repo"], LEDGER.replace("/", os.sep)),
                                os.path.join(mini, "src"))
                proc = _run([PY, "-m", "doc_engine.tools.spring_signal_scan", mini,
                             "--out", os.path.join(d, "s.json"),
                             "--scanners", "filesystem,ast-grep"], env=env)
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                with open(os.path.join(d, "s.json"), encoding="utf-8") as f:
                    mini_signals = json.load(f)
                blob = json.dumps(mini_signals, ensure_ascii=False)
                self.assertNotIn("Ã", blob)
                self.assertNotIn("�", blob)

    def test_unicode_space_and_deep_paths_survive_the_walk(self):
            grouped = _grouped(self.groups)
            for rel in (UNICODE_DIR_JAVA, SPACE_PATH, DEEP_JAVA):
                with self.subTest(path=rel):
                    self.assertIn(rel, grouped)
                    self.assertTrue(os.path.isfile(
                        os.path.join(_STATE["repo"], rel.replace("/", os.sep))))
