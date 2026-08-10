"""E-DOC1: research-map look-first hooks + domain entry door."""

from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.domain_ci_meta

REPO = Path(__file__).resolve().parents[2]
HOOKS = REPO / ".cursor" / "hooks"
if str(HOOKS) not in sys.path:
    sys.path.insert(0, str(HOOKS))


def _load(name: str):
    import importlib.util

    path = HOOKS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ResearchMapHooksTest(unittest.TestCase):
    def test_inject_research_map_mentions_readme(self) -> None:
        mod = _load("inject_research_map")
        buf = io.StringIO()
        with mock.patch.object(mod.sys, "stdin", io.StringIO("{}")):
            with mock.patch("builtins.print", side_effect=lambda *a, **k: buf.write(a[0])):
                self.assertEqual(mod.main(), 0)
        payload = json.loads(buf.getvalue())
        self.assertIn("docs/research/README.md", payload["additional_context"])

    def test_require_denies_without_receipt(self) -> None:
        from research_map_common import receipt_path

        require = _load("require_research_map_read")
        receipt = receipt_path()
        if receipt.exists():
            receipt.unlink()
        payload = {
            "tool_name": "Write",
            "tool_input": {"path": str(REPO / "docs" / "design" / "x.md")},
        }
        buf = io.StringIO()
        with mock.patch.object(require.sys, "stdin", io.StringIO(json.dumps(payload))):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(require.main(), 0)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["permission"], "deny")

    def test_record_then_allow(self) -> None:
        from research_map_common import receipt_path

        record = _load("record_research_map_read")
        require = _load("require_research_map_read")
        receipt = receipt_path()
        if receipt.exists():
            receipt.unlink()
        read_payload = {
            "tool_name": "Read",
            "tool_input": {"path": str(REPO / "docs" / "research" / "README.md")},
        }
        with mock.patch.object(record.sys, "stdin", io.StringIO(json.dumps(read_payload))):
            with mock.patch("builtins.print"):
                self.assertEqual(record.main(), 0)
        self.assertTrue(receipt.is_file())

        write_payload = {
            "tool_name": "Write",
            "tool_input": {"path": str(REPO / "docs" / "design" / "y.md")},
        }
        buf = io.StringIO()
        with mock.patch.object(
            require.sys, "stdin", io.StringIO(json.dumps(write_payload))
        ):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(require.main(), 0)
        self.assertEqual(json.loads(buf.getvalue())["permission"], "allow")


class ResearchDomainLayoutTest(unittest.TestCase):
    def test_domain_map_and_folders_exist(self) -> None:
        research = REPO / "docs" / "research"
        self.assertTrue((research / "README.md").is_file())
        for name in (
            "process",
            "coverage-quality",
            "ci",
            "kitchen",
            "bounded-contexts",
            "stage0",
            "archive",
        ):
            self.assertTrue((research / name).is_dir(), name)
        self.assertTrue((REPO / "docs" / "process" / "session-log.md").is_file())
        self.assertTrue(
            (
                REPO
                / "docs"
                / "process"
                / "steering-prompts"
                / "00-shared-research-standards.md"
            ).is_file()
        )
        self.assertTrue((REPO / "claude" / "README.md").is_file())
