"""Tests for CleanMeasureFactory wipe + cohesion wiring (no full pytest)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from doc_engine.ci.coverage_measure import CleanMeasureFactory, run_clean_measure


class CleanMeasureFactoryTest(unittest.TestCase):
    def test_wipe_removes_only_cwd_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / ".coverage").write_bytes(b"x")
            (cwd / ".coverage.pid1").write_bytes(b"y")
            (cwd / "coverage.xml").write_text("<coverage/>", encoding="utf-8")
            other = cwd / "subdir"
            other.mkdir()
            keep = other / ".coverage"
            keep.write_bytes(b"z")
            removed = CleanMeasureFactory(cwd).wipe_local_artifacts()
            self.assertFalse((cwd / ".coverage").exists())
            self.assertFalse((cwd / "coverage.xml").exists())
            self.assertTrue(keep.exists())
            self.assertGreaterEqual(len(removed), 3)

    def test_run_clean_measure_skip_pytest_validates(self) -> None:
        sample = """\
<?xml version="1.0" ?>
<coverage line-rate="1" branch-rate="1" version="7.0" timestamp="1">
  <packages>
    <package name="demo" line-rate="1" branch-rate="1" complexity="0">
      <classes>
        <class name="ok.py" filename="src/ok.py"
               line-rate="1" branch-rate="1" complexity="0">
          <lines><line number="1" hits="1"/></lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
"""
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "src").mkdir()
            (cwd / "coverage.xml").write_text(sample, encoding="utf-8")
            (cwd / ".coverage").write_bytes(b"stale")
            with mock.patch(
                "doc_engine.ci.coverage_measure.CleanMeasureFactory.run_pytest_cov"
            ) as run_cov:
                rc, xml = run_clean_measure(cwd=cwd, skip_pytest=True)
            run_cov.assert_not_called()
            self.assertEqual(rc, 0)
            self.assertIsNotNone(xml)
            self.assertFalse((cwd / ".coverage").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
