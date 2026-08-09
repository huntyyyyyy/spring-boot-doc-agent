"""Tests for scripts/ci/check_workflow_yaml.py — #57-class YAML parse gate."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pytest
from check_workflow_yaml import (
    check_workflows,
    collect_security_findings,
    scan_workflow_security,
)

from doc_engine.ci.workflow_size import (
    CI_CALLER_MAX_LOC,
    check_no_python_heredocs,
    check_workflow_loc,
)

pytestmark = pytest.mark.domain_ci_meta

class WorkflowYamlParseTest(unittest.TestCase):
    def test_committed_workflows_parse(self):
        self.assertEqual(check_workflows(), [])

    def test_unquoted_colon_in_step_name_is_caught(self):
        """Reproduction of the PR #57 Actions failure shape."""
        bad = (
            "name: CI\n"
            "on: [push]\n"
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - name: check (advisory: broken)\n"
            "        run: echo hi\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.yml"
            path.write_text(bad, encoding="utf-8")
            errors = check_workflows(Path(tmp))
        self.assertTrue(errors, msg="expected parse failure for unquoted colon")
        self.assertTrue(any("bad.yml" in e for e in errors))

    def test_quoted_colon_in_step_name_passes(self):
        good = (
            "name: CI\n"
            "on: [push]\n"
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            '      - name: "check (advisory: ok)"\n'
            "        run: echo hi\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "good.yml"
            path.write_text(good, encoding="utf-8")
            self.assertEqual(check_workflows(Path(tmp)), [])

class WorkflowSecurityRampTest(unittest.TestCase):
    def test_script_injection_is_critical(self):
        text = (
            "name: x\non: [pull_request]\npermissions:\n  contents: read\n"
            "jobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: echo ${{ github.event.pull_request.title }}\n"
        )
        findings = scan_workflow_security(Path("inj.yml"), text)
        self.assertTrue(any(f.rule == "script-injection" for f in findings))
        self.assertTrue(any(f.severity == "critical" for f in findings))

    def test_write_all_is_high(self):
        text = (
            "name: x\non: [push]\npermissions: write-all\n"
            "jobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - run: echo hi\n"
        )
        findings = scan_workflow_security(Path("wa.yml"), text)
        self.assertTrue(any(f.rule == "broad-permissions" for f in findings))

    def test_actions_v4_is_medium_advisory_not_hard(self):
        text = (
            "name: x\non: [push]\npermissions:\n  contents: read\n"
            "jobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.yml"
            path.write_text(text, encoding="utf-8")
            hard, advisory = collect_security_findings(Path(tmp))
        self.assertEqual(hard, [])
        self.assertTrue(any(f.rule == "unpinned-action" for f in advisory))
        self.assertTrue(all(f.severity == "medium" for f in advisory))

    def test_third_party_tag_is_high(self):
        text = (
            "name: x\non: [push]\npermissions:\n  contents: read\n"
            "jobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: some-org/deploy@v1\n"
        )
        findings = scan_workflow_security(Path("tp.yml"), text)
        hit = [f for f in findings if f.rule == "unpinned-action"]
        self.assertTrue(hit)
        self.assertEqual(hit[0].severity, "high")

    def test_committed_workflows_have_no_critical_high(self):
        hard, _advisory = collect_security_findings()
        self.assertEqual(
            hard,
            [],
            msg="committed workflows must not fail the severity ramp",
        )


class WorkflowSizeSoTTest(unittest.TestCase):
    def test_committed_workflows_pass_loc_and_heredoc(self):
        from check_workflow_yaml import WORKFLOWS, _label

        heredoc = check_no_python_heredocs(WORKFLOWS, label_fn=_label)
        hard, _adv = check_workflow_loc(WORKFLOWS, label_fn=_label)
        self.assertEqual(heredoc, [])
        self.assertEqual(hard, [])

    def test_fat_ci_yml_hard_fails(self):
        fat = "\n".join(f"# pad {i}" for i in range(CI_CALLER_MAX_LOC + 5))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ci.yml").write_text(fat + "\n", encoding="utf-8")
            hard, _adv = check_workflow_loc(root, label_fn=lambda p: p.name)
        self.assertTrue(any("ci.yml" in e for e in hard))

    def test_python_heredoc_hard_fails(self):
        text = "name: x\non: [push]\njobs:\n  t:\n    runs-on: ubuntu-latest\n"
        text += "    steps:\n      - run: |\n          python3 - <<'PY'\n          print(1)\n          PY\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fat.yml").write_text(text, encoding="utf-8")
            errors = check_no_python_heredocs(root, label_fn=lambda p: p.name)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
