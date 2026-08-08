"""Tests for doc_engine.ci.coverage_gap_average — below-floor climb inventory."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from doc_engine.ci import coverage_gap_average as cga


SAMPLE_XML = """\
<?xml version="1.0" ?>
<coverage line-rate="0.5" branch-rate="0.5" version="7.0" timestamp="1">
  <packages>
    <package name="demo" line-rate="0.5" branch-rate="0.5" complexity="0">
      <classes>
        <class name="green.py" filename="src/demo/green.py"
               line-rate="1.0" branch-rate="1.0" complexity="0">
          <lines>
            <line number="1" hits="1"/>
            <line number="2" hits="1"/>
          </lines>
        </class>
        <class name="mid.py" filename="src/demo/mid.py"
               line-rate="0.5" branch-rate="0.5" complexity="0">
          <lines>
            <line number="1" hits="1"/>
            <line number="2" hits="0"/>
            <line number="3" hits="1" branch="true" condition-coverage="50% (1/2)"/>
          </lines>
        </class>
        <class name="low.py" filename="src/demo/low.py"
               line-rate="0.0" branch-rate="0.0" complexity="0">
          <lines>
            <line number="1" hits="0"/>
            <line number="2" hits="0"/>
          </lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
"""


class CoverageGapAverageTest(unittest.TestCase):
    def test_partition_excludes_green_from_gap_average(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "coverage.xml"
            path.write_text(SAMPLE_XML, encoding="utf-8")
            files = cga.parse_file_coverages(path)
            report = cga.build_report(files, floor=98.7)
        self.assertEqual(len(report.files), 3)
        self.assertEqual(len(report.meeting_floor), 1)
        self.assertEqual(report.meeting_floor[0].path, "src/demo/green.py")
        self.assertEqual(len(report.below_floor), 2)
        below_paths = {f.path for f in report.below_floor}
        self.assertEqual(below_paths, {"src/demo/mid.py", "src/demo/low.py"})
        self.assertLess(report.below_floor_cover_pct, report.whole_repo_cover_pct)
        self.assertLess(report.below_floor_cover_pct, 98.7)
        self.assertGreater(report.below_floor_mean_file_pct, 0.0)
        self.assertLess(report.below_floor_mean_file_pct, 98.7)

    def test_all_green_reports_100_gap_average(self) -> None:
        files = [
            cga.FileCoverage("a.py", 10, 0, 0, 0),
            cga.FileCoverage("b.py", 5, 0, 2, 0),
        ]
        report = cga.build_report(files, floor=98.7)
        self.assertEqual(len(report.below_floor), 0)
        self.assertEqual(report.below_floor_cover_pct, 100.0)
        self.assertEqual(report.below_floor_mean_file_pct, 100.0)

    def test_worst_orders_lowest_cover_first(self) -> None:
        files = [
            cga.FileCoverage("mid.py", 10, 2, 0, 0),
            cga.FileCoverage("low.py", 10, 8, 0, 0),
            cga.FileCoverage("ok.py", 10, 0, 0, 0),
        ]
        report = cga.build_report(files, floor=98.7)
        worst = report.worst(2)
        self.assertEqual([w.path for w in worst], ["low.py", "mid.py"])

    def test_main_missing_xml_exits_2(self) -> None:
        code = cga.main(["--coverage-xml", "definitely-missing-coverage.xml"])
        self.assertEqual(code, 2)

    def test_format_text_mentions_exclusion(self) -> None:
        report = cga.build_report(
            [cga.FileCoverage("x.py", 10, 5, 0, 0)],
            floor=98.7,
        )
        text = cga.format_text(report, worst=5)
        self.assertIn("below_floor_cover", text)
        self.assertIn("green files excluded", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
