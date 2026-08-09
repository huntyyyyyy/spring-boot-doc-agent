"""Tests for MeasureRun wipe + dual-mode strategies (no full pytest)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from doc_engine.ci.coverage_artifact_policy import (
    CLIMB_BANNER,
    CLIMB_XML_NAME,
    ORACLE_XML_NAME,
)
from doc_engine.ci.coverage_measure import MeasureRun, main, run_clean_measure
from doc_engine.ci.coverage_measure_modes import (
    ClimbMeasureStrategy,
    MeasureMode,
    OracleMeasureStrategy,
    strategy_for,
)

SAMPLE_XML = """\
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


class MeasureRunTest(unittest.TestCase):
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
            removed = MeasureRun(cwd).wipe_local_artifacts()
            self.assertFalse((cwd / ".coverage").exists())
            self.assertFalse((cwd / "coverage.xml").exists())
            self.assertTrue(keep.exists())
            self.assertGreaterEqual(len(removed), 3)

    def test_climb_wipe_preserves_oracle_xml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / ORACLE_XML_NAME).write_text("<oracle/>", encoding="utf-8")
            (cwd / CLIMB_XML_NAME).write_text("<climb/>", encoding="utf-8")
            (cwd / ".coverage").write_bytes(b"x")
            strategy = ClimbMeasureStrategy(scope_package="doc_engine.ci")
            MeasureRun(cwd, strategy=strategy).wipe_local_artifacts()
            self.assertTrue((cwd / ORACLE_XML_NAME).exists())
            self.assertFalse((cwd / CLIMB_XML_NAME).exists())
            self.assertFalse((cwd / ".coverage").exists())

    def test_run_clean_measure_skip_pytest_validates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "src").mkdir()
            (cwd / "coverage.xml").write_text(SAMPLE_XML, encoding="utf-8")
            (cwd / ".coverage").write_bytes(b"stale")
            with mock.patch(
                "doc_engine.ci.coverage_measure.MeasureRun.run_pytest_cov"
            ) as run_cov:
                rc, xml = run_clean_measure(cwd=cwd, skip_pytest=True)
            run_cov.assert_not_called()
            self.assertEqual(rc, 0)
            self.assertIsNotNone(xml)
            self.assertFalse((cwd / ".coverage").exists())


class MeasureModeStrategyTest(unittest.TestCase):
    def test_oracle_argv_includes_fail_under(self) -> None:
        argv = OracleMeasureStrategy().pytest_cov_argv(
            fail_under_floor=98.7, extra_pytest_args=None
        )
        self.assertIn("--cov=doc_engine", argv)
        self.assertIn("--cov-fail-under=98.7", argv)
        self.assertIn("--cov-report=xml", argv)

    def test_climb_argv_scoped_without_fail_under(self) -> None:
        strategy = ClimbMeasureStrategy(scope_package="doc_engine.ci")
        argv = strategy.pytest_cov_argv(
            fail_under_floor=98.7, extra_pytest_args=["tests/ci"]
        )
        self.assertIn("--cov=doc_engine.ci", argv)
        self.assertNotIn("--cov=doc_engine", argv)
        self.assertTrue(any(a.startswith("--cov-report=xml:") for a in argv))
        self.assertFalse(any(a.startswith("--cov-fail-under") for a in argv))
        self.assertIn("tests/ci", argv)
        self.assertFalse(strategy.allows_gap_report())
        self.assertFalse(strategy.allows_fail_under())

    def test_climb_banner_and_strategy_factory(self) -> None:
        strategy = strategy_for(MeasureMode.CLIMB, scope_package="doc_engine.ci")
        self.assertEqual(strategy.xml_name, CLIMB_XML_NAME)
        self.assertIn("not CI oracle", CLIMB_BANNER)
        with self.assertRaises(ValueError):
            strategy_for(MeasureMode.CLIMB, scope_package=None)
        with self.assertRaises(ValueError):
            ClimbMeasureStrategy(scope_package="  ")

    def test_climb_execute_writes_climb_xml_leaves_oracle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "src").mkdir()
            (cwd / ORACLE_XML_NAME).write_text(SAMPLE_XML, encoding="utf-8")
            strategy = ClimbMeasureStrategy(scope_package="doc_engine.ci")

            def fake_run(cmd, cwd=None, check=False):  # noqa: ANN001
                del cmd, check
                Path(cwd).joinpath(CLIMB_XML_NAME).write_text(
                    SAMPLE_XML, encoding="utf-8"
                )
                return mock.Mock(returncode=0)

            with mock.patch("subprocess.run", side_effect=fake_run):
                with mock.patch("sys.stderr"):
                    rc, xml = MeasureRun(cwd, strategy=strategy).execute()
            self.assertEqual(rc, 0)
            self.assertIsNotNone(xml)
            assert xml is not None
            self.assertEqual(xml.name, CLIMB_XML_NAME)
            self.assertTrue((cwd / ORACLE_XML_NAME).exists())
            self.assertTrue((cwd / CLIMB_XML_NAME).exists())

    def test_main_climb_refuses_custom_floor(self) -> None:
        with mock.patch(
            "doc_engine.ci.coverage_measure_cli.checkout_root",
            return_value=Path.cwd(),
        ):
            rc = main(["--mode", "climb", "--scope", "doc_engine.ci", "--floor", "99"])
        self.assertEqual(rc, 2)

    def test_main_climb_requires_scope(self) -> None:
        rc = main(["--mode", "climb"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
