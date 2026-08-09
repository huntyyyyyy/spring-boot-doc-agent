"""Suite for .cursor/hooks/inject_nonvacuous_test_witness.py."""

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


class InjectNonvacuousTestWitnessTest(unittest.TestCase):
    def test_injects_context_for_tests_path(self) -> None:
        mod = _load("inject_nonvacuous_test_witness")
        payload = {
            "tool_name": "Write",
            "tool_input": {
                "path": str(REPO / "tests" / "ci" / "test_example.py"),
            },
        }
        buf = io.StringIO()
        with mock.patch.object(mod.sys, "stdin", io.StringIO(json.dumps(payload))):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(mod.main(), 0)
        out = json.loads(buf.getvalue())
        self.assertIn("Non-vacuous receipt rule", out["additional_context"])
        self.assertIn("empty receipt must fail", out["additional_context"])

    def test_silent_for_non_test_writes(self) -> None:
        mod = _load("inject_nonvacuous_test_witness")
        payload = {
            "tool_name": "Write",
            "tool_input": {"path": str(REPO / "README.md")},
        }
        buf = io.StringIO()
        with mock.patch.object(mod.sys, "stdin", io.StringIO(json.dumps(payload))):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(mod.main(), 0)
        self.assertEqual(buf.getvalue(), "")
