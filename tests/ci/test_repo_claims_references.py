"""Cohesive suite from tests/ci/test_repo_claims_derived_refs.py: TestNoShellExecution, TestReferences, TestVerifyPredicates."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import check_repo_claims as crc
from tests.conftest import REPO_ROOT
from tests.support.repo_claims.tree import TreeCase, build_tree

class TestNoShellExecution(TreeCase):
    """The 2f82971 regression class: markdown must never name anything but a
    key in a dict this file defines."""

    def test_unknown_key_is_an_error_not_a_silent_skip(self) -> None:
        self.write("README.md", "<!-- derived: no_such_key -->1<!-- /derived -->\n")
        self.assertEqual(self.run_check(), 1)

    def test_unknown_key_is_not_rewritten_by_fix(self) -> None:
        """--fix must not invent a value for a key it cannot compute. Doing so
        would turn an error into a silent pass, which is the gate-that-cannot-
        fail shape check E exists to prevent elsewhere."""
        original = "<!-- derived: no_such_key -->1<!-- /derived -->\n"
        self.write("README.md", original)
        crc.main(["--root", str(self.dir), "--fix"])
        self.assertEqual((self.dir / "README.md").read_text(encoding="utf-8"), original)
        self.assertEqual(self.run_check(), 1)

    def test_shell_metacharacters_cannot_form_a_key(self) -> None:
        """The regex charset is the boundary. A span carrying a command is not
        a malformed key -- it does not match the block syntax at all, so it is
        inert text."""
        for payload in ("ls; rm -rf /", "$(whoami)", "`id`", "a && b", "../../etc/passwd"):
            with self.subTest(payload=payload):
                self.write("README.md", f"<!-- derived: {payload} -->x<!-- /derived -->\n")
                self.assertEqual(len(crc.DERIVED_RE.findall(
                    (self.dir / "README.md").read_text(encoding="utf-8"))), 0)

    def test_no_subprocess_call_takes_markdown_derived_input(self) -> None:
        """Belt and braces: fail loudly if any subprocess call in the module
        ever grows an argument that isn't a literal. Today the only one is
        `git ls-files`."""
        import ast
        tree = ast.parse((REPO_ROOT / "scripts" / "ci" / "check_repo_claims.py")
                         .read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = getattr(func, "attr", getattr(func, "id", ""))
            if name not in {"run", "call", "check_output", "Popen", "system", "eval", "exec"}:
                continue
            self.assertTrue(node.args, "subprocess call with no argv")
            argv = node.args[0]
            self.assertIsInstance(argv, ast.List,
                                  "argv must be a literal list, never a built string")
            for element in argv.elts:
                self.assertIsInstance(element, ast.Constant,
                                      "every argv element must be a literal")


class TestReferences(TreeCase):
    """Check B."""

    def test_missing_path_fails(self) -> None:
        self.write("README.md", "See `scripts/nope.py`.\n")
        self.assertEqual(self.run_check(), 1)

    def test_missing_symbol_fails(self) -> None:
        self.write("README.md", "See `never_defined_anywhere()`.\n")
        self.assertEqual(self.run_check(), 1)

    def test_existing_symbol_passes(self) -> None:
        self.write("README.md", "See `do_a_thing()`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_camel_case_method_is_not_treated_as_a_python_symbol(self) -> None:
        """The pipeline documents hundreds of Java methods. None are Python."""
        self.write("README.md", "The service calls `findAllByStatus()`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_glob_matching_a_file_passes(self) -> None:
        (self.dir / "scripts" / "helper_extra.py").write_text(
            "x = 1\n", encoding="utf-8")
        self.write("README.md", "Helpers live at `scripts/helper_*.py`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_glob_matching_nothing_fails(self) -> None:
        self.write("README.md", "See `scripts/nomatch_*.py`.\n")
        self.assertEqual(self.run_check(), 1)

    def test_placeholder_path_is_not_resolved(self) -> None:
        self.write("README.md", "Write `claude/llms/pr-N.md`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_target_repo_path_is_out_of_scope(self) -> None:
        """These docs describe *other* people's services constantly."""
        self.write("README.md", "Reads `src/main/java/com/x/Foo.java` and `application.yml`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_line_anchor_beyond_end_of_file_fails(self) -> None:
        self.write("README.md", "See `scripts/widget.py:900`.\n")
        self.assertEqual(self.run_check(), 1)

    def test_line_anchor_inside_the_file_passes(self) -> None:
        self.write("README.md", "See `scripts/widget.py:2`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_historical_record_is_not_reference_checked(self) -> None:
        """An append-only log correctly cites files that existed when it was
        written. verify_llms_docs.py was real for 19 PRs."""
        self.write("claude/session-log.md", "Added `scripts/long_since_deleted.py`.\n")
        self.assertEqual(self.run_check(), 0)

    def test_tombstone_line_is_exempt(self) -> None:
        self.write("README.md",
                   "- ~~`scripts/gone.py`~~ — deleted as a security defect.\n")
        self.assertEqual(self.run_check(), 0)

    def test_tombstone_exemption_is_line_scoped(self) -> None:
        """A tombstone must not excuse the next claim down."""
        self.write("README.md",
                   "- ~~`scripts/gone.py`~~ — deleted.\n"
                   "- `scripts/also_missing.py` is current.\n")
        self.assertEqual(self.run_check(), 1)


class TestVerifyPredicates(TreeCase):
    """Check C."""

    PROMPT = "claude/steering-prompts/01-x-research-prompt.md"

    def test_satisfied_predicate_passes(self) -> None:
        self.assertEqual(self.run_check(), 0)

    def test_contradicted_path_exists_fails(self) -> None:
        (self.dir / "scripts" / "widget.py").unlink()
        self.assertEqual(self.run_check(), 1)

    def test_path_absent_contradicted_fails(self) -> None:
        """The direction that actually bit: `status: not started` while the
        deliverable already exists."""
        self.write(self.PROMPT,
                   "---\nstatus: not started\nverify:\n"
                   "  - path_absent:scripts/widget.py\n---\n")
        self.assertEqual(self.run_check(), 1)

    def test_contains_predicate_both_directions(self) -> None:
        self.write(self.PROMPT,
                   "---\nstatus: resolved\nverify:\n"
                   "  - contains:scripts/widget.py:do_a_thing\n---\n")
        self.assertEqual(self.run_check(), 0)
        self.write(self.PROMPT,
                   "---\nstatus: resolved\nverify:\n"
                   "  - contains:scripts/widget.py:absent_literal\n---\n")
        self.assertEqual(self.run_check(), 1)

    def test_contains_on_a_missing_file_fails(self) -> None:
        self.write(self.PROMPT,
                   "---\nstatus: resolved\nverify:\n"
                   "  - contains:scripts/nope.py:anything\n---\n")
        self.assertEqual(self.run_check(), 1)

    def test_unknown_predicate_fails_rather_than_passing_silently(self) -> None:
        self.write(self.PROMPT,
                   "---\nstatus: resolved\nverify:\n  - rm -rf /\n---\n")
        self.assertEqual(self.run_check(), 1)

    def test_status_with_no_verify_is_reported(self) -> None:
        self.write(self.PROMPT, "---\nstatus: resolved\n---\n")
        self.assertEqual(self.run_check(), 1)

    def test_missing_verify_is_baseline_eligible_but_a_failure_is_not(self) -> None:
        """The split that keeps the baseline from becoming an escape hatch:
        an unchecked claim can be accepted, a contradicted one never can."""
        self.write(self.PROMPT, "---\nstatus: resolved\n---\n")
        _, soft = crc.collect_all(self.dir)
        self.assertTrue(any(f.fingerprint.startswith("C-missing:") for f in soft))

        self.write(self.PROMPT,
                   "---\nstatus: resolved\nverify:\n  - path_exists:scripts/nope.py\n---\n")
        hard, _ = crc.collect_all(self.dir)
        self.assertTrue(any(f.check == "C" for f in hard))
