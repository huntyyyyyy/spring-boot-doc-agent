"""Kitchen-sink Ch12: check_pipeline_output gate responsibility."""

from __future__ import annotations

import os
import re
import shutil
import sys
import unittest

import pytest

from tests.support.kitchen_sink.constants import _STATE
from tests.support.kitchen_sink.harness import (
    _copy_docs,
    _run,
    setUpModule,
    tearDownModule,
)

pytestmark = pytest.mark.domain_integration

PY = sys.executable
GITIGNORED_DIR = "generated"

# unittest discovers these names on the module.
assert setUpModule and tearDownModule


class Ch12PipelineOutputGateTest(unittest.TestCase):
    """Which pipeline-output defects the Stage-4 gate catches."""

    def _gate(self, docs, *extra):
        """Copied-docs form — write check off (see stray-write tests for on)."""
        return _run(
            [
                PY,
                "-m",
                "doc_engine.tools.check_pipeline_output",
                docs,
                "--target-repo",
                _STATE["repo"],
                "--no-write-check",
                *extra,
            ]
        )

    def test_three_citation_defects_all_fail_the_gate(self):
        """Three issue classes in one mutated copy / one subprocess."""
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(docs, "database.md")
        text = open(path, encoding="utf-8").read()
        text = text.replace("[Evidenced —", "[Evidenced -", 1)
        text = re.sub(
            r"(\[Evidenced — [^\];]+?):(\d+)\]",
            lambda match: f"{match.group(1)}:999999]",
            text,
            count=1,
        )
        text += "\n- Fabricated [Evidenced — no/such/File.java:1].\n"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("malformed evidence tag", proc.stderr)
        self.assertIn("points past the end", proc.stderr)
        self.assertIn("does not exist under", proc.stderr)

    def test_extra_file_in_docs_fails_the_gate(self):
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        with open(os.path.join(docs, "notes.md"), "w", encoding="utf-8") as handle:
            handle.write("stray\n")
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("unexpected file in docs dir", proc.stderr)

    def test_duplicate_output_path_shows_up_as_a_missing_name(self):
        scratch, docs = _copy_docs()
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        shutil.copyfile(
            os.path.join(docs, "readme.md"), os.path.join(docs, "glossary.md")
        )
        os.remove(os.path.join(docs, "testing.md"))
        proc = self._gate(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing expected doc: testing.md", proc.stderr)

    def test_stray_write_is_caught_and_no_write_check_removes_the_control(self):
        stray = os.path.join(_STATE["repo"], "stray-written-by-a-subagent.txt")
        with open(stray, "w", encoding="utf-8") as handle:
            handle.write("a writer went outside docs/\n")
        self.addCleanup(lambda: os.path.exists(stray) and os.remove(stray))
        strict = _run(
            [
                PY,
                "-m",
                "doc_engine.tools.check_pipeline_output",
                _STATE["docs"],
                "--target-repo",
                _STATE["repo"],
            ]
        )
        self.assertEqual(strict.returncode, 1)
        self.assertIn("unexpected write outside the docs directory", strict.stderr)
        self.assertEqual(
            self._gate(_STATE["docs"]).returncode,
            0,
            "--no-write-check should remove exactly this control",
        )

    def test_a_stray_write_into_a_gitignored_path_fails_the_gate(self):
        ignored_dir = os.path.join(_STATE["repo"], GITIGNORED_DIR)
        os.makedirs(ignored_dir, exist_ok=True)
        stray = os.path.join(ignored_dir, "oops.md")
        with open(stray, "w", encoding="utf-8") as handle:
            handle.write("written outside docs/, into a gitignored directory\n")
        self.addCleanup(lambda: os.path.exists(stray) and os.remove(stray))
        proc = _run(
            [
                PY,
                "-m",
                "doc_engine.tools.check_pipeline_output",
                _STATE["docs"],
                "--target-repo",
                _STATE["repo"],
            ]
        )
        self.assertEqual(
            proc.returncode, 1, "gate must report a write into a gitignored path"
        )
        self.assertIn("gitignored path", proc.stderr)
