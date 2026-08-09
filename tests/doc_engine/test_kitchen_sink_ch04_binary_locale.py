"""Kitchen-sink encoding binary/locale edges."""

from __future__ import annotations

import json
import os
import shutil
import tempfile

import pytest
from doc_engine.tools import partition_repo

from tests.support.kitchen_sink.constants import (
    DEEP_JAVA,
    EMPTY_JAVA,
    EMPTY_YML,
    LEDGER,
    NUL_JAVA,
    PY,
    SPACE_PATH,
    UNICODE_DIR_JAVA,
)
from tests.support.kitchen_sink.harness import _grouped, _run
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch04EncodingTestContinued(KitchenBoundTestCase):
    def setUp(self):
        self.signals = self.kitchen.signals
        self.groups = self.kitchen.groups

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
            os.path.join(self.kitchen.repo, EMPTY_JAVA.replace("/", os.sep)),
            2_000_000,
        )
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
            {
                (
                    d["configuration"],
                    d["coordinate"].get("group"),
                    d["coordinate"].get("name"),
                )
                for d in deps
            },
        )
        tcs = [r for r in deployment if r.get("rule_id") == "deployment__build_toolchain"]
        self.assertEqual(tcs[0]["toolchain_value"], "17")
        mods = [r for r in deployment if r.get("rule_id") == "deployment__build_module"]
        self.assertEqual({m["module"] for m in mods}, {"billing", "ledger"})
        catalogs = [
            r for r in deployment if r.get("rule_id") == "deployment__version_catalog"
        ]
        self.assertEqual({c["catalog_kind"] for c in catalogs}, {"version", "library"})

    def test_non_ascii_source_is_neither_dropped_nor_mangled(self):
        matches = [
            row.get("match", "")
            for rows in (self.signals.get("evidence") or {}).values()
            for row in rows
        ]
        blob = "\n".join(matches)
        # Positive witness: planted UNICODE_QUERY characters must appear.
        # Absence-of-mojibake alone passes if the query was dropped entirely.
        self.assertTrue(
            ("Á" in blob) or ("日本語" in blob) or ("café" in blob),
            "planted non-ASCII query text missing from evidence matches",
        )
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
        env.update(
            {
                "LC_ALL": "C",
                "LANG": "C",
                "PYTHONUTF8": "0",
                "PYTHONCOERCECLOCALE": "0",
            }
        )
        # Scoped to a one-file tree rather than the whole fixture: it isolates
        # the variable under test and keeps a full second ast-grep pass out of
        # the suite's runtime.
        with tempfile.TemporaryDirectory() as d:
            mini = os.path.join(d, "repo")
            shutil.copytree(
                os.path.join(self.kitchen.repo, LEDGER.replace("/", os.sep)),
                os.path.join(mini, "src"),
            )
            proc = _run(
                [
                    PY,
                    "-m",
                    "doc_engine.tools.spring_signal_scan",
                    mini,
                    "--out",
                    os.path.join(d, "s.json"),
                    "--scanners",
                    "filesystem,ast-grep",
                ],
                env=env,
            )
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
                self.assertTrue(
                    os.path.isfile(
                        os.path.join(self.kitchen.repo, rel.replace("/", os.sep))
                    )
                )
