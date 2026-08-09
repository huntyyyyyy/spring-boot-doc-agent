"""Cohesive suite from tests/ci/test_repo_claims_baseline_predicates.py: TestMirrorDebt."""

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

import pytest

pytestmark = pytest.mark.domain_ci_meta

class TestMirrorDebt(unittest.TestCase):
    """Prompts 00-06 have a canonical copy in the Claude project; editing one
    creates an obligation no CLI session can discharge. This turns that
    obligation from a paragraph someone has to read into a counted number."""

    def _repo(self, tmp):
        root = Path(tmp)
        prompts = root / "docs" / "process" / "steering-prompts"
        prompts.mkdir(parents=True)
        for name in ["00-a.md", "01-b.md", "06-c.md", "07-not-mirrored.md",
                     "13-also-not.md"]:
            (prompts / name).write_text(f"# {name}\n", encoding="utf-8")
        return root

    def test_an_unrecorded_prompt_counts_as_debt(self):
        """Absent state must not read as clean. A checker whose default is
        'everything is fine' reports best when it knows least."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            self.assertEqual(len(crc.mirror_debt(root)), 3)

    def test_recording_clears_the_debt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            crc.write_mirror_state(root)
            self.assertEqual(crc.mirror_debt(root), [])

    def test_editing_a_mirrored_prompt_reopens_its_debt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            crc.write_mirror_state(root)
            edited = root / "docs" / "process" / "steering-prompts" / "01-b.md"
            edited.write_text("# 01-b.md\n\nstatus changed\n", encoding="utf-8")
            self.assertEqual(crc.mirror_debt(root),
                             ["docs/process/steering-prompts/01-b.md"])

    def test_prompts_above_06_are_not_tracked(self):
        """07+ were authored in this repo and exist nowhere else, so they
        carry no mirror obligation. Counting them would inflate the debt with
        work nobody owes."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            crc.write_mirror_state(root)
            (root / "docs" / "process" / "steering-prompts" / "07-not-mirrored.md").write_text(
                "# heavily edited\n", encoding="utf-8")
            self.assertEqual(crc.mirror_debt(root), [])

    def test_affirming_claims_does_not_clear_mirror_debt(self):
        """The hazard this design exists to avoid. Affirming means "I re-read
        this claim"; mirroring means "I copied this file to the project."
        Sharing one verb would let a routine --affirm silently clear real
        mirror debt, making the number lowest exactly when someone had been
        most casual."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            crc.write_mirror_state(root)
            prompt = root / "docs" / "process" / "steering-prompts" / "01-b.md"
            prompt.write_text("# 01-b.md\n\nedited\n", encoding="utf-8")
            self.assertEqual(len(crc.mirror_debt(root)), 1)

            crc.apply_affirm(root, ["docs/process/steering-prompts/01-b.md"])
            self.assertEqual(len(crc.mirror_debt(root)), 1,
                             "--affirm must not clear mirror debt")

    def test_the_state_file_says_what_it_cannot_prove(self):
        """It records debt, not sync -- nothing here can see the project copy.
        A reader who mistakes it for proof of sync would trust it exactly
        where it is weakest."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._repo(tmp)
            crc.write_mirror_state(root)
            payload = json.loads((root / crc.MIRROR_STATE).read_text(encoding="utf-8"))
            self.assertIn("cannot see the project", payload["$comment"])
