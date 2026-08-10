"""Non-vacuous receipt witness: commit-time control-plane check."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.domain_adapters

REPO = Path(__file__).resolve().parents[2]
ADAPTER_HOOKS = REPO / "adapters" / "claude" / "hooks"
sys.path.insert(0, str(ADAPTER_HOOKS))

import nonvacuous_receipt_witness as witness  # noqa: E402


class NonvacuousWitnessLogicTest(unittest.TestCase):
    def test_control_plane_paths_detected(self) -> None:
        self.assertTrue(
            witness.is_control_plane_path(
                "src/doc_engine/ci/stalker_telemetry/run_store.py"
            )
        )
        self.assertTrue(witness.is_control_plane_path("scripts/ci/pre_pr.py"))
        self.assertFalse(witness.is_control_plane_path("README.md"))

    def test_clean_tree_witness_present(self) -> None:
        """Standing suite must already satisfy markers or every CP commit dies."""
        self.assertEqual(
            witness.missing_nonvacuous_witness(
                REPO, ["src/doc_engine/ci/stalker_telemetry/run_store.py"]
            ),
            [],
        )

    def test_missing_markers_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            suite = root / "tests" / "ci"
            suite.mkdir(parents=True)
            (suite / "test_stalker_telemetry.py").write_text(
                "def test_noop():\n    assert True\n", encoding="utf-8"
            )
            problems = witness.missing_nonvacuous_witness(
                root, ["scripts/ci/pre_pr.py"]
            )
            self.assertEqual(len(problems), 1)
            self.assertIn("non-vacuous receipt markers", problems[0])

    def test_unrelated_staged_files_skip_check(self) -> None:
        self.assertEqual(
            witness.missing_nonvacuous_witness(REPO, ["docs/README.md"]), []
        )


class HardenedFindingsWireTest(unittest.TestCase):
    def test_findings_includes_nonvacuous_check(self) -> None:
        import require_hardened_tests as gate

        with mock.patch.object(gate, "staged_files", return_value=["README.md"]):
            with mock.patch.object(gate, "staged_deletions", return_value=set()):
                with mock.patch.object(gate, "failing_gates", return_value=[]):
                    self.assertEqual(gate.findings(), [])

        with mock.patch.object(
            gate, "staged_files", return_value=["scripts/ci/pre_pr.py"]
        ):
            with mock.patch.object(gate, "staged_deletions", return_value=set()):
                with mock.patch.object(gate, "failing_gates", return_value=[]):
                    with mock.patch.object(
                        gate,
                        "missing_nonvacuous_witness",
                        return_value=["vacuous"],
                    ) as mocked:
                        problems = gate.findings()
        self.assertIn("vacuous", problems)
        mocked.assert_called_once()
