"""Cohesive suite from tests/ci/test_repo_claims_baseline_predicates.py: TestAffirm, TestPredicateRegistry."""

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

class TestAffirm(unittest.TestCase):
    """--affirm is what makes the predicate usable. Without it a claim can
    only be re-affirmed by hand-computing a digest, and an unusable check is
    an ignored one."""

    def _repo(self, tmp, doc_body):
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "scripts" / "sub.py").write_text(
            'def f(x):\n    """Docs."""\n    return x + 1\n', encoding="utf-8")
        (root / "CONSTRAINTS.md").write_text(doc_body, encoding="utf-8")
        return root

    def test_affirm_round_trip(self):
        """affirm -> clean; mutate -> fails; affirm -> clean. The operational
        loop, which is what decides whether anyone adopts this."""
        body = ("**[Resolved]** a claim. "
                "<!-- verify: unchanged_since:scripts/sub.py:t2: -->\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp, body)

            def claim_passes():
                claims = crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
                return crc.evaluate_predicate(root, claims[0].predicates[0])[0]

            self.assertFalse(claim_passes(), "unaffirmed claim should not pass")
            self.assertEqual(crc.apply_affirm(root, ["CONSTRAINTS.md"]), ["CONSTRAINTS.md"])
            self.assertTrue(claim_passes(), "affirm did not stamp a usable digest")

            (root / "scripts" / "sub.py").write_text(
                'def f(x):\n    """Docs."""\n    return x + 99\n', encoding="utf-8")
            self.assertFalse(claim_passes(), "a behaviour change should trip it")

            crc.apply_affirm(root, ["CONSTRAINTS.md"])
            self.assertTrue(claim_passes(), "re-affirming did not clear it")

    def test_affirm_does_not_rewrite_inside_a_code_fence(self):
        """A fenced example documents the syntax. Rewriting the sample in
        CLAUDE.md that explains this feature would be a small, funny
        disaster -- the same guard apply_fix already carries."""
        body = ("```\n"
                "<!-- verify: unchanged_since:scripts/sub.py:t2: -->\n"
                "```\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp, body)
            self.assertEqual(crc.apply_affirm(root, ["CONSTRAINTS.md"]), [])
            self.assertIn("unchanged_since:scripts/sub.py:t2: -->",
                          (root / "CONSTRAINTS.md").read_text(encoding="utf-8"))

    def test_affirm_leaves_an_unknown_level_alone(self):
        """It must keep failing the check rather than being rewritten to
        something plausible -- silently repairing a claim nobody can evaluate
        is the same class of bug as a gate that cannot fail."""
        body = "**[Resolved]** x. <!-- verify: unchanged_since:scripts/sub.py:t9: -->\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp, body)
            self.assertEqual(crc.apply_affirm(root, ["CONSTRAINTS.md"]), [])

    def test_affirm_leaves_a_missing_subject_alone(self):
        body = "**[Resolved]** x. <!-- verify: unchanged_since:scripts/gone.py:t2: -->\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp, body)
            self.assertEqual(crc.apply_affirm(root, ["CONSTRAINTS.md"]), [])


class TestPredicateRegistry(unittest.TestCase):
    """The registry replaced a startswith() chain that duplicated the prefix
    list. These defend the properties that restructure either preserves or
    newly makes possible to break."""

    def test_an_unknown_predicate_is_rejected(self):
        """The closed-vocabulary guarantee, asserted rather than assumed. A
        document may select among keys this file defines; it can never supply
        behaviour. That is the exact inverse of the deleted
        verify_llms_docs.py, where the document supplied the command."""
        passed, why = crc.evaluate_predicate(REPO_ROOT, "exec_shell:rm -rf /")
        self.assertFalse(passed)
        self.assertIn("unknown predicate", why)

    def test_called_by_detects_static_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod = root / "pkg"
            mod.mkdir()
            (mod / "callee.py").write_text(
                "def helper():\n    return 1\n",
                encoding="utf-8",
            )
            (mod / "caller.py").write_text(
                "from callee import helper\n\ndef run():\n    return helper()\n",
                encoding="utf-8",
            )
            passed, why = crc.evaluate_predicate(
                root, "called_by:helper:pkg/caller.py"
            )
            self.assertTrue(passed, why)
            passed_missing, _ = crc.evaluate_predicate(
                root, "called_by:helper:pkg/callee.py"
            )
            self.assertFalse(passed_missing)

    def test_called_by_rejects_markdown_supplied_paths_malformed(self) -> None:
        passed, why = crc.evaluate_predicate(REPO_ROOT, "called_by:only_one_part")
        self.assertFalse(passed)
        self.assertIn("malformed", why)

    def test_behavior_unknown_key_fails_closed(self) -> None:
        passed, why = crc.evaluate_predicate(
            REPO_ROOT, "behavior:not_a_registered_key"
        )
        self.assertFalse(passed)
        self.assertIn("unknown behavior key", why)

    def test_behavior_registered_keys_hold_on_repo(self) -> None:
        for key in sorted(crc.BEHAVIOR_CHECKS):
            passed, why = crc.evaluate_predicate(REPO_ROOT, f"behavior:{key}")
            self.assertTrue(passed, f"behavior:{key} failed: {why}")

    def test_behavior_key_cannot_be_a_shell_command_from_markdown(self) -> None:
        """Documents select keys; they cannot smuggle argv (verify_llms_docs)."""
        passed, why = crc.evaluate_predicate(
            REPO_ROOT, "behavior:rm -rf /"
        )
        self.assertFalse(passed)
        self.assertIn("unknown behavior key", why)

    def test_no_predicate_prefix_is_a_prefix_of_another(self):
        """The invariant the registry creates a need for. Dispatch is
        first-match, which is unambiguous today only because no prefix
        shadows another. Add `path_exists_recursive:` and it would silently
        route to `path_exists:` with the rest of the string as its operand --
        wrong, and quiet. Currently true; this makes it stay true."""
        prefixes = list(crc.PREDICATE_HANDLERS)
        shadowed = [(a, b) for a in prefixes for b in prefixes
                    if a != b and b.startswith(a)]
        self.assertEqual(shadowed, [], f"prefix shadowing would misroute: {shadowed}")

    def test_every_registered_handler_is_reachable(self):
        """A handler in the dict that no predicate can select is dead code
        that looks live.

        Reachability is the whole property; the verdict is each handler's own
        business. The first version of this test also asserted the result was
        False, which is wrong: `path_absent:__no_such_thing__` correctly
        returns True, because the path really is absent. Asserting a verdict
        here was testing the handlers rather than the dispatch."""
        for prefix in crc.PREDICATE_HANDLERS:
            _, why = crc.evaluate_predicate(REPO_ROOT, f"{prefix}__no_such_thing__")
            self.assertNotIn("unknown predicate", why,
                             f"{prefix} fell through to the unknown-predicate branch")

    def test_the_reference_alternation_is_derived_from_the_prefix_list(self):
        """These were two literal tuples of the same eight strings. Deriving
        one from the other is what stops them drifting; this fails if someone
        re-inlines the list."""
        for prefix in crc.OWN_PATH_PREFIXES:
            self.assertIn(re.escape(prefix), crc._OWN_PREFIX_ALT)
