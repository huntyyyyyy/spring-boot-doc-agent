"""Kitchen-sink encoding BOM/CRLF twins."""

from __future__ import annotations

import pytest

from doc_engine.tools import spring_signal_scan
from tests.support.kitchen_sink.constants import (
    BOM_YML,
    CRLF_JAVA,
    CRLF_PROPS,
    LATIN1_JAVA,
    LF_PROPS,
    MULTI_SEG_YML,
    NOBOM_YML,
)
from tests.support.kitchen_sink.harness import _grouped
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch04EncodingTest(KitchenBoundTestCase):
    def setUp(self):
        self.signals = self.kitchen.signals
        self.groups = self.kitchen.groups

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
        self.assertEqual(
            {h["line"] for h in zones[BOM_YML]},
            {h["line"] for h in zones[NOBOM_YML]},
        )

    def test_multi_segment_profile_names_are_recognized_as_config(self):
        """Multi-segment Spring profiles (application-dev-local.yml) must be
        ingested: CONFIG_NAME_PATTERNS uses [\\w.-]+ so hyphenated profile
        segments reach config_key_sets and redaction_zones."""
        self.assertTrue(
            any(
                p.match("application-dev-local.yml")
                for p in spring_signal_scan.CONFIG_NAME_PATTERNS
            )
        )
        self.assertTrue(
            any(
                p.match("application-prod.yml")
                for p in spring_signal_scan.CONFIG_NAME_PATTERNS
            )
        )
        self.assertTrue(
            any(
                p.match("bootstrap-dev-local.properties")
                for p in spring_signal_scan.CONFIG_NAME_PATTERNS
            )
        )
        keys = self.signals["config_key_sets"]
        self.assertIn(MULTI_SEG_YML, keys)
        self.assertIn("spring.datasource.password", keys[MULTI_SEG_YML])
        zones = self.signals["redaction_zones"]
        self.assertIn(
            MULTI_SEG_YML,
            zones,
            "multi-segment profile must receive credential scanning",
        )

    def test_crlf_and_lf_twins_produce_identical_key_sets(self):
        keys = self.signals["config_key_sets"]
        self.assertEqual(keys[CRLF_PROPS], keys[LF_PROPS])

    def test_crlf_java_is_scanned_with_sane_line_numbers(self):
        self.assertIn(CRLF_JAVA, _grouped(self.groups))
        crlf_rows = [
            row
            for rows in (self.signals.get("evidence") or {}).values()
            for row in rows
            if row["file"] == CRLF_JAVA
        ]
        self.assertGreater(
            len(crlf_rows), 0, f"no evidence rows for planted {CRLF_JAVA}"
        )
        for row in crlf_rows:
            self.assertGreaterEqual(row.get("line", 0), 1)

    def test_invalid_utf8_is_included_via_the_latin1_fallback(self):
        """latin-1 accepts every byte, so this is a silent mis-decode by
        design. Pinned as stated behavior, not endorsed."""
        self.assertIn(LATIN1_JAVA, _grouped(self.groups))
        self.assertIsNone(self._skip_reason(LATIN1_JAVA))
