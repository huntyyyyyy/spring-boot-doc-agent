"""Kitchen-sink encoding BOM/CRLF twins."""

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

class Ch04EncodingTest(unittest.TestCase):
    def setUp(self):
            self.signals = _STATE["signals"]
            self.groups = _STATE["groups"]

    def _skip_reason(self, rel):
            for s in self.groups["skipped"]:
                if s["file"] == rel:
                    return s["reason"]
            return None

    def test_bom_and_no_bom_twins_produce_identical_key_sets(self):
            """A BOM read as plain utf-8 leaves a literal ﻿, which is category
            Cf — neither \\s nor \\w — so the ^\\s*-anchored key regex fails on line
            1 entirely. When line 1 is a group header it never enters the indent
            stack and every descendant key silently loses its prefix, which yields
            a key set that looks plausible and is wholly wrong. Byte-identical
            twins are the assertion; membership of one key would not have caught
            the prefix loss."""
            keys = self.signals["config_key_sets"]
            self.assertIn(BOM_YML, keys)
            self.assertEqual(keys[BOM_YML], keys[NOBOM_YML])
            self.assertIn("spring.jwt-secret", keys[BOM_YML])

    def test_secret_on_the_line_after_a_bom_header_is_still_flagged(self):
            """Same root cause, confidentiality side: a blinded line 1 shifts the
            indent stack, and the secret heuristics are anchored the same way."""
            zones = self.signals["redaction_zones"]
            self.assertIn(BOM_YML, zones, "BOM'd config produced no redaction zones")
            self.assertEqual({h["line"] for h in zones[BOM_YML]},
                             {h["line"] for h in zones[NOBOM_YML]})

    def test_multi_segment_profile_names_are_recognized_as_config(self):
            """Multi-segment Spring profiles (application-dev-local.yml) must be
            ingested: CONFIG_NAME_PATTERNS uses [\\w.-]+ so hyphenated profile
            segments reach config_key_sets and redaction_zones."""
            self.assertTrue(any(p.match("application-dev-local.yml")
                                for p in spring_signal_scan.CONFIG_NAME_PATTERNS))
            self.assertTrue(any(p.match("application-prod.yml")
                                for p in spring_signal_scan.CONFIG_NAME_PATTERNS))
            self.assertTrue(any(p.match("bootstrap-dev-local.properties")
                                for p in spring_signal_scan.CONFIG_NAME_PATTERNS))
            keys = self.signals["config_key_sets"]
            self.assertIn(MULTI_SEG_YML, keys)
            self.assertIn("spring.datasource.password", keys[MULTI_SEG_YML])
            zones = self.signals["redaction_zones"]
            self.assertIn(MULTI_SEG_YML, zones,
                          "multi-segment profile must receive credential scanning")

    def test_crlf_and_lf_twins_produce_identical_key_sets(self):
            keys = self.signals["config_key_sets"]
            self.assertEqual(keys[CRLF_PROPS], keys[LF_PROPS])

    def test_crlf_java_is_scanned_with_sane_line_numbers(self):
            self.assertIn(CRLF_JAVA, _grouped(self.groups))
            for rows in (self.signals.get("evidence") or {}).values():
                for row in rows:
                    if row["file"] == CRLF_JAVA:
                        self.assertGreaterEqual(row.get("line", 1), 1)

    def test_invalid_utf8_is_included_via_the_latin1_fallback(self):
            """latin-1 accepts every byte, so this is a silent mis-decode by
            design. Pinned as stated behavior, not endorsed."""
            self.assertIn(LATIN1_JAVA, _grouped(self.groups))
            self.assertIsNone(self._skip_reason(LATIN1_JAVA))
