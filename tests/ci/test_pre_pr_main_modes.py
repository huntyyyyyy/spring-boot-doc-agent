"""Cohesive suite from tests/ci/test_pre_pr.py: MainActionsOutageTest, MainAutoUsesStandardSuitesTest, MainBypassTest."""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest import mock
import pre_pr

import pytest

pytestmark = pytest.mark.domain_ci_meta

class MainActionsOutageTest(unittest.TestCase):
    def test_missing_toolchain_exits_before_suites(self):
        import tempfile

        captured: list[str] = []

        def capture_build(mode: str):
            captured.append(mode)
            return []

        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            with mock.patch.object(pre_pr, "require_outage_toolchain", return_value=1):
                with mock.patch.object(
                    pre_pr, "build_suites", side_effect=capture_build
                ):
                    with mock.patch.object(pre_pr, "RECEIPT_PATH", receipt):
                        code = pre_pr.main(["--actions-outage"])
        self.assertEqual(code, 1)
        self.assertEqual(captured, [])

    def test_skip_refused_under_outage(self):
        with mock.patch.dict(
            os.environ,
            {"PRE_PR_SKIP": "1", "PRE_PR_SKIP_REASON": "should not work here"},
            clear=False,
        ):
            with mock.patch.object(pre_pr, "require_outage_toolchain", return_value=0):
                code = pre_pr.main(["--actions-outage"])
        self.assertEqual(code, 2)

    def test_success_writes_attestation_receipt(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"

            def empty_suites(mode: str):
                self.assertEqual(mode, "actions_outage")
                return []

            env = {k: v for k, v in os.environ.items() if k not in (
                "PRE_PR_SKIP",
                "PRE_PR_SKIP_REASON",
            )}
            with mock.patch.dict(os.environ, env, clear=True):
                with mock.patch.object(pre_pr, "require_outage_toolchain", return_value=0):
                    with mock.patch.object(pre_pr, "check_bypass", return_value=None):
                        with mock.patch.object(
                            pre_pr, "build_suites", side_effect=empty_suites
                        ):
                            with mock.patch.object(pre_pr, "RECEIPT_PATH", receipt):
                                with mock.patch.object(
                                    pre_pr, "_tool_versions", return_value={}
                                ):
                                    with mock.patch.object(
                                        pre_pr, "_git_sha", return_value="deadbeef"
                                    ):
                                        code = pre_pr.main(
                                            [
                                                "--actions-outage",
                                                "--status-url",
                                                "https://www.githubstatus.com/",
                                            ]
                                        )
            self.assertEqual(code, 0)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["mode"], "actions_outage")
            self.assertEqual(data["attestation"], "actions_outage")
            self.assertEqual(
                data["github_status_note"], "https://www.githubstatus.com/"
            )
            self.assertEqual(data["schema_version"], 2)
            self.assertEqual(data["overall"], "pass")

class MainAutoUsesStandardSuitesTest(unittest.TestCase):
    def test_main_auto_calls_build_suites_with_standard(self):
        import tempfile

        captured: list[str] = []

        def capture_build(mode: str):
            captured.append(mode)
            return []

        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            with mock.patch.object(pre_pr, "check_bypass", return_value=None):
                with mock.patch.object(
                    pre_pr,
                    "changed_files_vs_main",
                    return_value=["scripts/ci/pre_pr.py"],
                ):
                    with mock.patch.object(
                        pre_pr, "build_suites", side_effect=capture_build
                    ):
                        with mock.patch.object(pre_pr, "RECEIPT_PATH", receipt):
                            with mock.patch.object(
                                pre_pr, "_tool_versions", return_value={}
                            ):
                                with mock.patch.object(
                                    pre_pr, "_git_sha", return_value="deadbeef"
                                ):
                                    code = pre_pr.main(["--auto"])
            self.assertEqual(code, 0)
            self.assertEqual(captured, ["standard"])
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["mode"], "standard")
            self.assertNotEqual(data["mode"], "full")

class MainBypassTest(unittest.TestCase):
    def test_main_bypass_exits_zero(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "receipt.json"
            bypass = Path(tmp) / "bypass.log"
            with mock.patch.dict(
                os.environ,
                {"PRE_PR_SKIP": "1", "PRE_PR_SKIP_REASON": "broken hook escape"},
                clear=False,
            ):
                with mock.patch.object(pre_pr, "RECEIPT_PATH", receipt):
                    with mock.patch.object(pre_pr, "BYPASS_LOG", bypass):
                        code = pre_pr.main(["--fast"])
            self.assertEqual(code, 0)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["overall"], "bypassed")
