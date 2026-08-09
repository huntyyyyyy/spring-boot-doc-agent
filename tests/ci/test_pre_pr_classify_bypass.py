"""Cohesive suite from tests/ci/test_pre_pr.py: ClassifyPathRiskTest, BypassTest, ReceiptTest, BuildSuitesTest, ResolveModeTest, RequireOutageToolchainTest."""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest import mock
import pre_pr

import pytest

pytestmark = pytest.mark.domain_ci_meta

class ClassifyPathRiskTest(unittest.TestCase):
    def test_docs_only_is_fast(self):
        self.assertEqual(
            pre_pr.classify_path_risk(["README.md", "docs/process/session-log.md"]),
            "fast",
        )

    def test_scripts_change_is_standard(self):
        self.assertEqual(
            pre_pr.classify_path_risk(["scripts/ci/pre_pr.py"]),
            "standard",
        )

    def test_empty_is_standard(self):
        self.assertEqual(pre_pr.classify_path_risk([]), "standard")

    def test_github_workflow_is_standard(self):
        self.assertEqual(
            pre_pr.classify_path_risk([".github/workflows/ci.yml"]),
            "standard",
        )

class BypassTest(unittest.TestCase):
    def test_skip_without_reason_exits(self):
        with mock.patch.dict(os.environ, {"PRE_PR_SKIP": "1"}, clear=False):
            os.environ.pop("PRE_PR_SKIP_REASON", None)
            with self.assertRaises(SystemExit) as ctx:
                pre_pr.check_bypass()
            self.assertEqual(ctx.exception.code, 2)

    def test_skip_with_reason_returns_entry(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            bypass_log = Path(tmp) / "pre-pr-bypass-test.log"
            with mock.patch.dict(
                os.environ,
                {"PRE_PR_SKIP": "1", "PRE_PR_SKIP_REASON": "emergency hotfix"},
                clear=False,
            ):
                with mock.patch.object(pre_pr, "BYPASS_LOG", bypass_log):
                    entry = pre_pr.check_bypass()
        self.assertIsNotNone(entry)
        self.assertEqual(entry["reason"], "emergency hotfix")

class ReceiptTest(unittest.TestCase):
    def test_write_receipt_has_required_keys(self, tmp_path_factory=None):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            receipt_path = Path(tmp) / "pre-pr-receipt.json"
            with mock.patch.object(pre_pr, "RECEIPT_PATH", receipt_path):
                receipt = pre_pr.Receipt(
                    schema_version=2,
                    git_sha="abc",
                    mode="actions_outage",
                    suites=[
                        pre_pr.SuiteResult("ruff", "pass", 10, "hard", "exit=0"),
                    ],
                    tool_versions={"python": "3.11"},
                    overall="pass",
                    attestation="actions_outage",
                    github_status_note="https://www.githubstatus.com/",
                )
                pre_pr.write_receipt(receipt)
            data = json.loads(receipt_path.read_text(encoding="utf-8"))
        for key in (
            "schema_version",
            "git_sha",
            "mode",
            "suites",
            "tool_versions",
            "overall",
            "attestation",
            "github_status_note",
        ):
            self.assertIn(key, data)
        self.assertEqual(data["overall"], "pass")
        self.assertEqual(data["schema_version"], 2)
        self.assertEqual(data["attestation"], "actions_outage")
        self.assertEqual(data["github_status_note"], "https://www.githubstatus.com/")
        self.assertEqual(data["suites"][0]["name"], "ruff")

class BuildSuitesTest(unittest.TestCase):
    def test_fast_skips_pytest(self):
        names = [n for n, _, _ in pre_pr.build_suites("fast")]
        self.assertNotIn("pytest", names)
        self.assertNotIn("test_domain_markers", names)
        self.assertIn("check_repo_claims", names)
        self.assertIn("ruff", names)

    def test_standard_includes_pytest_not_stage0(self):
        names = [n for n, _, _ in pre_pr.build_suites("standard")]
        self.assertIn("pytest", names)
        self.assertIn("in_repo_quality_gates", names)
        self.assertIn("test_domain_markers", names)
        self.assertIn("facade_poke_surface", names)
        self.assertNotIn("stage0_portable", names)
        self.assertNotIn("mutate_advisory", names)

    def test_full_includes_advisory_mutate(self):
        names = [n for n, _, _ in pre_pr.build_suites("full")]
        self.assertIn("pytest", names)
        self.assertIn("in_repo_quality_gates", names)
        self.assertIn("sonar_local_advisory", names)
        self.assertIn("mutate_advisory", names)
        self.assertIn("stage0_portable", names)
        self.assertNotIn("codeql_invariants", names)

    def test_actions_outage_includes_codeql_and_certify(self):
        names = [n for n, _, _ in pre_pr.build_suites("actions_outage")]
        self.assertIn("stage0_portable", names)
        self.assertIn("mutate_advisory", names)
        self.assertIn("codeql_invariants", names)
        self.assertIn("codeql_compile_and_ql_tests", names)
        self.assertIn("codeql_fixture_runtime", names)
        self.assertIn("certify_scan_only", names)
        self.assertIn("certify_certified", names)

class ResolveModeTest(unittest.TestCase):
    def _ns(self, *, auto=False, fast=False, full=False, actions_outage=False):
        return mock.Mock(
            auto=auto, fast=fast, full=full, actions_outage=actions_outage
        )

    def test_auto_code_diff_is_standard_not_full(self):
        with mock.patch.object(
            pre_pr,
            "changed_files_vs_main",
            return_value=["scripts/ci/pre_pr.py"],
        ):
            mode = pre_pr.resolve_mode(self._ns(auto=True))
        self.assertEqual(mode, "standard")
        self.assertNotEqual(mode, "full")

    def test_auto_docs_only_is_fast(self):
        with mock.patch.object(
            pre_pr,
            "changed_files_vs_main",
            return_value=["README.md", "docs/process/session-log.md"],
        ):
            mode = pre_pr.resolve_mode(self._ns(auto=True))
        self.assertEqual(mode, "fast")

    def test_no_flags_defaults_to_path_risk(self):
        with mock.patch.object(
            pre_pr,
            "changed_files_vs_main",
            return_value=["src/doc_engine/paths.py"],
        ):
            mode = pre_pr.resolve_mode(self._ns())
        self.assertEqual(mode, "standard")

    def test_full_flag_ignores_path_risk(self):
        with mock.patch.object(
            pre_pr,
            "changed_files_vs_main",
            return_value=["README.md"],
        ):
            mode = pre_pr.resolve_mode(self._ns(full=True))
        self.assertEqual(mode, "full")

    def test_actions_outage_flag(self):
        mode = pre_pr.resolve_mode(self._ns(actions_outage=True))
        self.assertEqual(mode, "actions_outage")

class RequireOutageToolchainTest(unittest.TestCase):
    def test_missing_codeql_fails(self):
        with mock.patch.object(pre_pr.shutil, "which", return_value=None):
            code = pre_pr.require_outage_toolchain()
        self.assertEqual(code, 1)

    def test_all_present_passes(self):
        def which(name):
            return f"/bin/{name}"

        with mock.patch.object(pre_pr.shutil, "which", side_effect=which):
            code = pre_pr.require_outage_toolchain()
        self.assertEqual(code, 0)
