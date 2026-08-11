"""Semantic adversarial-review hooks: inject, audit, stop rewrite.

Run: ``python3 -m pytest tests/ci/test_semantic_review_hooks.py -q``
"""

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


class SemanticReviewHooksTest(unittest.TestCase):
    def setUp(self) -> None:
        common = _load("semantic_review_common")
        common.clear_state()
        self.common = common

    def tearDown(self) -> None:
        self.common.clear_state()

    def test_prompt_detects_adversarial_review(self) -> None:
        self.assertTrue(
            self.common.prompt_is_review(
                "adversarial review of this Implement-Ready DDL package"
            )
        )
        self.assertFalse(
            self.common.prompt_is_review("fix the typo in README please")
        )

    def test_scan_flags_scoreboard_without_if_then(self) -> None:
        taut = "\n".join(
            [
                "# Review",
                "**Support.** The claim is good.",
                "**Refuse.** The claim is bad.",
                "**Refuse.** Another refuse stamp.",
                "**Nuance.** Slightly nuanced restatement.",
                "| ID | Finding |",
                "| C1 | Support |",
                "| C2 | Refuse |",
                "x" * 80,
            ]
        )
        bad, reasons = self.common.scan_review_text(taut)
        self.assertTrue(bad, reasons)

    def test_scan_allows_if_then_heavy_review(self) -> None:
        good = (
            "If the registry is wipe/rebuild derived, then a lock_registry row "
            "cannot be the single-writer mechanism because rebuild erases locks. "
            "If LockCheck means IR versus edges, then validate_write on SQL leases "
            "is a different predicate. Disposition after that: refuse the rename. "
            + ("detail " * 40)
        )
        bad, reasons = self.common.scan_review_text(good)
        self.assertFalse(bad, reasons)

    def test_inject_arms_and_adds_context(self) -> None:
        inject = _load("inject_semantic_review")
        payload = {
            "prompt": "Please do an adversarial review of this architecture package"
        }
        buf = io.StringIO()
        with mock.patch.object(inject.sys, "stdin", io.StringIO(json.dumps(payload))):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(inject.main(), 0)
        out = json.loads(buf.getvalue())
        self.assertTrue(out.get("continue"))
        self.assertIn("if→then", out.get("additional_context", ""))
        self.assertTrue(self.common.load_state().get("active"))

    def test_stop_followup_when_finding(self) -> None:
        self.common.mark_review_active("adversarial review")
        self.common.record_finding(["verdict_stamps=5 if_then=0"])
        stop = _load("stop_semantic_review_rewrite")
        payload = {"status": "completed", "loop_count": 0}
        buf = io.StringIO()
        with mock.patch.object(stop.sys, "stdin", io.StringIO(json.dumps(payload))):
            with mock.patch(
                "builtins.print", side_effect=lambda *a, **k: buf.write(a[0])
            ):
                self.assertEqual(stop.main(), 0)
        out = json.loads(buf.getvalue())
        self.assertIn("followup_message", out)
        self.assertIn("if→then", out["followup_message"])

    def test_hooks_json_wires_semantic_review(self) -> None:
        hooks = json.loads((REPO / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
        before = hooks["hooks"]["beforeSubmitPrompt"]
        self.assertTrue(
            any("inject_semantic_review" in h.get("command", "") for h in before)
        )
        self.assertTrue(
            any(
                "audit_semantic_review_response" in h.get("command", "")
                for h in hooks["hooks"]["afterAgentResponse"]
            )
        )
        self.assertTrue(
            any(
                "stop_semantic_review_rewrite" in h.get("command", "")
                for h in hooks["hooks"]["stop"]
            )
        )


if __name__ == "__main__":
    unittest.main()
