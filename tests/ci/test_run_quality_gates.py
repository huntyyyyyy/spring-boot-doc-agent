"""Tests for doc_engine.ci.quality_gates — portable hard-gate runner."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from doc_engine.ci import quality_gates as qg


class RunQualityGatesTest(unittest.TestCase):
    def test_gate_new_code_coverage_uses_python_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp) / "coverage.xml"
            xml.write_text("<coverage/>", encoding="utf-8")
            captured: list[list[str]] = []

            def fake_run(command: list[str], *, label: str) -> int:
                captured.append(command)
                return 0

            with mock.patch.object(qg, "_run", side_effect=fake_run):
                code = qg.gate_new_code_coverage("origin/main", xml)
            self.assertEqual(code, 0)
            self.assertEqual(captured[0][0], sys.executable)
            self.assertEqual(captured[0][1:3], ["-m", "diff_cover.diff_cover_tool"])
            self.assertIn(str(xml), captured[0])

    def test_gate_import_cycles_uses_tach_module(self) -> None:
        captured: list[list[str]] = []

        def fake_run(command: list[str], *, label: str) -> int:
            captured.append(command)
            return 0

        with mock.patch.object(qg, "_run", side_effect=fake_run):
            self.assertEqual(qg.gate_import_cycles(), 0)
        self.assertEqual(captured[0][:4], [sys.executable, "-m", "tach", "check"])

    def test_gate_duplication_uses_jscpd_command(self) -> None:
        captured: list[list[str]] = []

        def fake_run(command: list[str], *, label: str) -> int:
            captured.append(command)
            return 0

        with (
            mock.patch.object(
                qg,
                "changed_python_under_packages",
                return_value=["src/doc_engine/a.py", "src/doc_engine/b.py"],
            ),
            mock.patch.object(
                qg,
                "jscpd_command",
                return_value=["/bin/jscpd", "--threshold=3", "a.py", "b.py"],
            ) as jscpd,
            mock.patch.object(qg, "_run", side_effect=fake_run),
        ):
            self.assertEqual(qg.gate_duplication("HEAD~1"), 0)
        jscpd.assert_called_once()
        self.assertEqual(captured[0][0], "/bin/jscpd")

    def test_gate_duplication_skips_when_no_changed_files(self) -> None:
        with mock.patch.object(qg, "changed_python_under_packages", return_value=[]):
            self.assertEqual(qg.gate_duplication("HEAD~1"), 0)

    def test_complexity_ratchet_skips_duplicate_scan_when_baseline_zero(self) -> None:
        with mock.patch.object(qg, "baseline_offender_ceiling", return_value=0):
            with mock.patch.object(qg, "_run") as run:
                self.assertEqual(qg.gate_complexity_ratchet(), 0)
        run.assert_not_called()

    def test_complexity_ratchet_runs_module_when_baseline_positive(self) -> None:
        captured: list[list[str]] = []

        def fake_run(command: list[str], *, label: str) -> int:
            captured.append(command)
            return 0

        with (
            mock.patch.object(qg, "baseline_offender_ceiling", return_value=3),
            mock.patch.object(qg, "_run", side_effect=fake_run),
        ):
            self.assertEqual(qg.gate_complexity_ratchet(), 0)
        self.assertEqual(
            captured[0][:3],
            [sys.executable, "-m", "doc_engine.ci.complexipy_ratchet"],
        )

    def test_baseline_offender_ceiling_reads_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "baseline.json"
            path.write_text(
                json.dumps({"schema_version": 1, "offender_count": 0}),
                encoding="utf-8",
            )
            self.assertEqual(qg.baseline_offender_ceiling(path), 0)

    def test_resolve_compare_ref_validates(self) -> None:
        with mock.patch.object(qg, "validate_git_rev", return_value="origin/main") as v:
            self.assertEqual(qg.resolve_compare_ref("origin/main"), "origin/main")
        v.assert_called_once_with("origin/main")

    def test_main_skip_coverage_omits_diff_cover(self) -> None:
        with (
            mock.patch.object(qg, "gate_duplication", return_value=0),
            mock.patch.object(qg, "gate_size_ratchet", return_value=0),
            mock.patch.object(qg, "gate_cognitive_complexity", return_value=0),
            mock.patch.object(qg, "gate_complexity_ratchet", return_value=0),
            mock.patch.object(qg, "gate_import_cycles", return_value=0),
            mock.patch.object(qg, "gate_new_code_coverage") as cov,
        ):
            code = qg.main(["--compare-ref", "HEAD~1", "--skip-coverage"])
        self.assertEqual(code, 0)
        cov.assert_not_called()

    def test_main_fail_fast_skips_later_gates(self) -> None:
        with (
            mock.patch.object(qg, "gate_import_cycles", return_value=1) as cycles,
            mock.patch.object(qg, "gate_size_ratchet") as size,
            mock.patch.object(qg, "gate_duplication") as dup,
            mock.patch.object(qg, "gate_cognitive_complexity") as cx,
            mock.patch.object(qg, "gate_complexity_ratchet") as ratchet,
            mock.patch.object(qg, "gate_new_code_coverage") as cov,
        ):
            code = qg.main(["--compare-ref", "HEAD~1", "--skip-coverage"])
        self.assertEqual(code, 1)
        cycles.assert_called_once()
        size.assert_not_called()
        dup.assert_not_called()
        cx.assert_not_called()
        ratchet.assert_not_called()
        cov.assert_not_called()

    def test_main_no_fail_fast_runs_all(self) -> None:
        with (
            mock.patch.object(qg, "gate_import_cycles", return_value=1),
            mock.patch.object(qg, "gate_size_ratchet", return_value=0) as size,
            mock.patch.object(qg, "gate_duplication", return_value=0) as dup,
            mock.patch.object(qg, "gate_cognitive_complexity", return_value=0) as cx,
            mock.patch.object(qg, "gate_complexity_ratchet", return_value=0) as ratchet,
        ):
            code = qg.main(
                ["--compare-ref", "HEAD~1", "--skip-coverage", "--no-fail-fast"]
            )
        self.assertEqual(code, 1)
        size.assert_called_once()
        dup.assert_called_once()
        cx.assert_called_once()
        ratchet.assert_called_once()

    def test_gate_size_ratchet_uses_module(self) -> None:
        captured: list[list[str]] = []

        def fake_run(command: list[str], *, label: str) -> int:
            captured.append(command)
            return 0

        with mock.patch.object(qg, "_run", side_effect=fake_run):
            self.assertEqual(qg.gate_size_ratchet(), 0)
        self.assertEqual(
            captured[0][:3],
            [sys.executable, "-m", "doc_engine.ci.size_ratchet"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
