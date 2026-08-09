"""E-FAC0 / E-RES0: façade poke inventory + design-research commit hook."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import pytest

from adapters.claude.hooks import require_design_research as rdr

pytestmark = pytest.mark.domain_ci_meta

REPO = Path(__file__).resolve().parents[2]


class FacadePokeSurfaceTest(unittest.TestCase):
    def test_check_script_exits_zero_on_current_tree(self):
        proc = subprocess.run(
            [sys.executable, str(REPO / "scripts/ci/check_facade_poke_surface.py")],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("OK:", proc.stdout)


class DesignResearchHookTest(unittest.TestCase):
    def _run_hook(self, command: str, staged: list[str]) -> dict:
        payload = json.dumps({"tool_input": {"command": command}})
        buf = io.StringIO()
        with mock.patch.object(rdr.sys, "stdin") as stdin:
            stdin.read.return_value = payload
            with mock.patch.object(rdr, "staged_files", return_value=staged):
                with mock.patch(
                    "builtins.print",
                    side_effect=lambda *args, **kwargs: buf.write(args[0]),
                ):
                    with self.assertRaises(SystemExit) as ctx:
                        rdr.main()
        self.assertEqual(ctx.exception.code, 0)
        return json.loads(buf.getvalue())

    def test_non_commit_allows(self):
        data = self._run_hook("pytest tests/ -q", [])
        self.assertEqual(data["decision"], "approve")

    def test_design_commit_without_memo_blocks(self):
        data = self._run_hook(
            "git commit -m 'x'",
            ["src/doc_engine/tools/run_manifest_ports.py"],
        )
        self.assertEqual(data["decision"], "block")
        self.assertIn("principal-se-research-epic", data["reason"])

    def test_design_commit_with_spec_memo_allows(self):
        data = self._run_hook(
            "git commit -m 'x'",
            [
                "src/doc_engine/tools/run_manifest_ports.py",
                "docs/research/14-facade-poke-research-hooks-2026.md",
            ],
        )
        self.assertEqual(data["decision"], "approve")
