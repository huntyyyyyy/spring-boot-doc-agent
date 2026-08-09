"""Tests for coverage report path cohesion (cross-worktree dilution guard)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from doc_engine.ci.coverage_path_cohesion import (
    PathCohesionError,
    assert_paths_cohesive,
    cohesion_violations,
)
from doc_engine.ci.coverage_report import CoberturaXmlReport, FileCoverage


class PathCohesionValidatorTest(unittest.TestCase):
    def test_clean_relative_paths_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src").mkdir()
            paths = ["src/doc_engine/cli.py", "src/stf/__init__.py"]
            self.assertEqual(cohesion_violations(paths, root), [])
            assert_paths_cohesive(paths, root)

    def test_foreign_wt_cov_prefix_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "spring-boot-doc-agent"
            root.mkdir()
            foreign = (
                str(root.parent / "wt-cov-measure" / "src" / "doc_engine" / "cli.py")
            )
            bad = cohesion_violations([foreign], root)
            self.assertTrue(bad, msg="expected foreign wt-cov path to violate")
            with self.assertRaises(PathCohesionError) as ctx:
                assert_paths_cohesive([foreign], root)
            self.assertIn("cohesion failed", str(ctx.exception))

    def test_relative_path_escaping_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            bad = cohesion_violations(["../outside.py"], root)
            self.assertTrue(bad)
            self.assertIn("escapes", bad[0])

    def test_absolute_path_outside_tree_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            outside = Path(tmp) / "other" / "src" / "x.py"
            outside.parent.mkdir(parents=True)
            outside.write_text("#", encoding="utf-8")
            bad = cohesion_violations([str(outside)], root)
            self.assertTrue(bad)

    def test_report_adapter_source_paths_feed_guard(self) -> None:
        report = CoberturaXmlReport(
            (
                FileCoverage("src/ok.py", 1, 0, 0, 0),
                FileCoverage(
                    "C:/Users/x/Downloads/wt-cov-other/src/bad.py", 1, 0, 0, 0
                ),
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "spring-boot-doc-agent"
            root.mkdir()
            with self.assertRaises(PathCohesionError):
                assert_paths_cohesive(report.source_paths(), root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
