"""Cohesive suite from tests/doc_engine/test_partition_repo.py: EstimateTokensTest, RespectGitignoreOptInTest, EmittedPathSeparatorTest."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.core.excludes import load_gitignore_spec
from doc_engine.tools import partition_repo
SCRIPT_DIR = SCRIPTS_DIR

class EstimateTokensTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, name, content):
        path = os.path.join(self.tmpdir, name)
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_dense_extension_uses_lower_divisor(self):
        # Same content, different extension -> different token estimate.
        # This is the actual fix: structured-data formats (yml/json/etc.)
        # measured meaningfully denser than chars/4 assumes (see the
        # CHARS_PER_TOKEN_DENSE comment in partition_repo.py for the
        # calibration data) - the old flat chars/4 under-counted them.
        content = "x" * 400  # 400 chars
        java_path = self._write("Sample.java", content)
        yml_path = self._write("sample.yml", content)

        java_tokens, _ = partition_repo.estimate_tokens(java_path, max_file_bytes=10_000)
        yml_tokens, _ = partition_repo.estimate_tokens(yml_path, max_file_bytes=10_000)

        self.assertEqual(java_tokens, 400 // partition_repo.CHARS_PER_TOKEN_DEFAULT)
        self.assertEqual(yml_tokens, 400 // partition_repo.CHARS_PER_TOKEN_DENSE)
        self.assertGreater(yml_tokens, java_tokens, "same content should estimate MORE tokens under the dense divisor")

    def test_all_dense_extensions_recognized(self):
        content = "a" * 100
        for ext in sorted(partition_repo.DENSE_EXTS):
            path = self._write(f"sample{ext}", content)
            tokens, reason = partition_repo.estimate_tokens(path, max_file_bytes=10_000)
            self.assertIsNone(reason)
            self.assertEqual(tokens, 100 // partition_repo.CHARS_PER_TOKEN_DENSE, f"extension {ext} not using dense divisor")

    def test_binary_file_skipped(self):
        path = os.path.join(self.tmpdir, "binary.dat")
        with open(path, "wb") as f:
            f.write(b"\x00\x01\x02\x03" * 100)
        tokens, reason = partition_repo.estimate_tokens(path, max_file_bytes=10_000)
        self.assertEqual(tokens, 0)
        self.assertEqual(reason, "binary")

    def test_oversized_file_skipped(self):
        path = self._write("big.txt", "x" * 1000)
        tokens, reason = partition_repo.estimate_tokens(path, max_file_bytes=500)
        self.assertEqual(tokens, 0)
        self.assertIn("too-large", reason)


class RespectGitignoreOptInTest(unittest.TestCase):
    """--respect-gitignore is additive-only: default behavior (flag/spec
    omitted) must be unaffected, and a directory not covered by the
    hardcoded DEFAULT_EXCLUDED_DIRS floor should only disappear when the
    repo's own .gitignore excludes it AND the caller opts in."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmpdir, "scratch"))
        with open(os.path.join(self.tmpdir, "scratch", "notes.txt"), "w") as f:
            f.write("not source")
        with open(os.path.join(self.tmpdir, "kept.txt"), "w") as f:
            f.write("kept")
        with open(os.path.join(self.tmpdir, ".gitignore"), "w") as f:
            f.write("scratch/\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _relpaths(self, gitignore_spec):
        files = partition_repo.dfs_file_list(
            self.tmpdir,
            partition_repo.DEFAULT_EXCLUDED_DIRS,
            partition_repo.DEFAULT_EXCLUDED_EXTS,
            partition_repo.DEFAULT_EXCLUDED_FILES,
            gitignore_spec=gitignore_spec,
        )
        return {os.path.relpath(f, self.tmpdir).replace("\\", "/") for f in files}

    def test_scratch_dir_included_without_opt_in(self):
        self.assertEqual(self._relpaths(gitignore_spec=None), {".gitignore", "kept.txt", "scratch/notes.txt"})

    def test_scratch_dir_excluded_with_opt_in(self):
        spec = load_gitignore_spec(self.tmpdir)
        self.assertIsNotNone(spec, "pathspec must be installed for this test to be meaningful")
        self.assertEqual(self._relpaths(gitignore_spec=spec), {".gitignore", "kept.txt"})


class EmittedPathSeparatorTest(unittest.TestCase):
    """groups.json's `files` are joined by path against spring_signals.json's
    `file` fields -- Stage 1 slices the evidence by which group each cited file
    falls in. spring_signal_scan.py normalizes every path it emits to forward
    slashes, so partition_repo.py must too.

    Regression: it did not. `main()` used a raw os.path.relpath(), so on Windows
    every nested path came out with backslashes and matched nothing. The failure
    was silent -- Stage 1 subagents received an empty evidence slice rather than
    an error, quietly defeating the "don't rediscover what ast-grep already
    found" design. Caught only by a real end-to-end run against spring-petclinic,
    where 54 of 55 cited files matched no group.

    Third instance of this same bug class in this repo; see spring_drift_check.py's
    tier1_scan() and claude/session-log.md."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        nested = os.path.join(self.tmpdir, "src", "main", "java", "com", "example")
        os.makedirs(nested)
        with open(os.path.join(nested, "Thing.java"), "w") as f:
            f.write("class Thing {}\n")
        with open(os.path.join(self.tmpdir, "root.txt"), "w") as f:
            f.write("root\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run_partition(self):
        out = os.path.join(self.tmpdir, "groups.json")
        subprocess.run(
            [sys.executable, "-m", "doc_engine.tools.partition_repo",
             self.tmpdir, "--out", out],
            check=True, capture_output=True, text=True,
        )
        with open(out) as f:
            return json.load(f)

    def test_emitted_paths_use_forward_slashes(self):
        data = self._run_partition()
        emitted = [f for g in data["groups"] for f in g["files"]]
        self.assertTrue(emitted, "partition produced no files")
        offenders = [f for f in emitted if "\\" in f]
        self.assertEqual(offenders, [], f"backslashes in emitted paths: {offenders}")

    def test_nested_path_matches_signal_scan_style_key(self):
        # The exact join Stage 1 performs, on the shape that actually broke.
        data = self._run_partition()
        emitted = {f for g in data["groups"] for f in g["files"]}
        self.assertIn("src/main/java/com/example/Thing.java", emitted)
