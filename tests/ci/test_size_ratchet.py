"""Tests for doc_engine.ci.size_ratchet — file LOC / function statement ceilings."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from doc_engine.ci import size_ratchet as sr

import pytest

pytestmark = pytest.mark.domain_ci_meta

class SizeRatchetCompareTest(unittest.TestCase):
    def test_unchanged_offenders_pass(self) -> None:
        baseline = {
            "schema_version": 3,
            "files": {"src/doc_engine/big.py": 300},
            "functions": {"src/doc_engine/big.py::f": 60},
            "file_offender_count": 1,
            "fn_offender_count": 1,
        }
        issues = sr.compare(
            baseline,
            {"src/doc_engine/big.py": 300, "src/doc_engine/ok.py": 40},
            {"src/doc_engine/big.py::f": 60, "src/doc_engine/ok.py::g": 3},
        )
        self.assertEqual(issues, [])

    def test_new_file_over_hard_fails(self) -> None:
        baseline = {
            "schema_version": 3,
            "files": {},
            "functions": {},
            "file_offender_count": 0,
            "fn_offender_count": 0,
        }
        issues = sr.compare(
            baseline,
            {"src/doc_engine/huge.py": sr.FILE_LOC_HARD + 1},
            {},
        )
        self.assertTrue(any("new file offender" in i for i in issues), issues)

    def test_growth_of_baselined_file_fails(self) -> None:
        baseline = {
            "schema_version": 3,
            "files": {"src/doc_engine/big.py": 300},
            "functions": {},
            "file_offender_count": 1,
            "fn_offender_count": 0,
        }
        issues = sr.compare(
            baseline,
            {"src/doc_engine/big.py": 320},
            {},
        )
        self.assertTrue(any("grew" in i for i in issues), issues)

    def test_improvement_without_update_passes(self) -> None:
        baseline = {
            "schema_version": 3,
            "files": {"src/doc_engine/big.py": 300},
            "functions": {"src/doc_engine/big.py::f": 60},
            "file_offender_count": 1,
            "fn_offender_count": 1,
        }
        issues = sr.compare(baseline, {}, {})
        self.assertEqual(issues, [])

    def test_soft_advisories_do_not_hard_fail(self) -> None:
        mid_loc = (sr.FILE_LOC_SOFT + sr.FILE_LOC_HARD) // 2
        notes = sr.soft_advisories(
            {"src/doc_engine/mid.py": mid_loc},
            {"src/doc_engine/mid.py::f": sr.FN_STMTS_HARD},
        )
        self.assertEqual(len(notes), 2)
        issues = sr.compare(
            {
                "schema_version": 3,
                "files": {},
                "functions": {},
                "file_offender_count": 0,
                "fn_offender_count": 0,
            },
            {"src/doc_engine/mid.py": mid_loc},
            {"src/doc_engine/mid.py::f": sr.FN_STMTS_HARD},
        )
        self.assertEqual(issues, [])

    def test_file_loc_hard_is_flat_225(self) -> None:
        self.assertEqual(sr.FILE_LOC_HARD, 225)
        self.assertEqual(sr.FILE_LOC_SOFT, 150)
        self.assertLess(sr.FILE_LOC_SOFT, sr.FILE_LOC_HARD)
        self.assertEqual(
            sr.hard_file_offenders({"a.py": 225, "b.py": 226}),
            {"b.py": 226},
        )

class SizeRatchetMainTest(unittest.TestCase):
    def test_update_writes_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "size_baseline.json"
            with (
                mock.patch.object(
                    sr,
                    "measure_tree",
                    return_value=({"a.py": 50}, {"a.py::f": 3}),
                ),
                mock.patch(
                    "doc_engine.ci.size_ratchet.checked_path_under_repo",
                    side_effect=lambda p: p,
                ),
            ):
                code = sr.main(["--baseline", str(path), "--update"])
            self.assertEqual(code, 0)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], 3)
            self.assertEqual(data["file_loc_hard"], 225)
            self.assertEqual(data["file_loc_soft"], 150)
            self.assertEqual(data["file_offender_count"], 0)
            self.assertEqual(data["fn_offender_count"], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
