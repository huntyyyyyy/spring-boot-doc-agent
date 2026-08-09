"""Build-file classification, gitignore opt-in, ast-grep failures."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.scanning._resolve_lineage import _SQLLINEAGE_AVAILABLE
from doc_engine.scanning.facts import facts_from_signals
from doc_engine.tools import spring_signal_scan
SCRIPT_DIR = SCRIPTS_DIR
USE_SNAPSHOT = os.environ.get("SPRING_SIGNAL_USE_SNAPSHOT", "").lower() in ("1", "true", "yes")
SNAPSHOT_SCANNERS = ["filesystem", "ast-grep"]

class BuildFileClassificationTest(unittest.TestCase):
    """Gradle/Maven build scripts and build-adjacent property files.

    These are classified by FILENAME, not parsed: ast-grep has no Groovy
    grammar at all (`-l groovy` -> "groovy is not supported!"), so a
    .gradle file can never get the structural treatment every .java rule
    gets. Before this existed they fell through every branch in scan()'s
    pass 1 -- read by file-summarizer, since partition_repo.py does not
    exclude them, but carrying no bucket and, more seriously, never
    reaching the secret-redaction path.

    Note these do NOT go through rule_coverage.py's non-vacuity gate, which
    only covers ast-grep rules. This suite is the only thing asserting the
    Python filename path works, so an assertion missing here is a hole
    nothing else covers."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, name, text=""):
        path = os.path.join(self.tmpdir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def _matches(self, result, bucket):
        return {(e["file"], e.get("match")) for e in result["evidence"][bucket]}

    def test_build_scripts_land_in_deployment(self):
        for name in ("build.gradle", "settings.gradle.kts", "pom.xml",
                     "build.xml", "extra.groovy"):
            self._write(name, "// build\n")
        found = self._matches(spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS), "deployment")
        for name in ("build.gradle", "settings.gradle.kts", "pom.xml",
                     "build.xml", "extra.groovy"):
            self.assertIn((name, "build script"), found, name)

    def test_a_plain_kts_script_is_not_a_build_file(self):
        """`.kts` alone is any Kotlin script. Matching it would put arbitrary
        Kotlin into operations.md, so the compound suffix is what counts."""
        self._write("scratch.kts", "println(1)\n")
        found = self._matches(spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS), "deployment")
        self.assertNotIn(("scratch.kts", "build script"), found)

    def test_gradle_properties_is_treated_as_config(self):
        self._write("gradle.properties", "org.gradle.jvmargs=-Xmx2g\n")
        found = self._matches(spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS), "configuration")
        self.assertIn(("gradle.properties", "config file"), found)

    def test_a_credential_in_gradle_properties_is_redacted(self):
        """The defect that motivated this: build.gradle's own comment records
        that gradle.properties carries `_password` entries, and that file
        matched none of the config patterns, so it never reached the
        redaction path at all."""
        self._write("gradle.properties", "repoUser=ci\nrepoPassword=hunter2literal\n")
        zones = spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS)["redaction_zones"]
        self.assertIn("gradle.properties", zones)
        self.assertEqual([z["line"] for z in zones["gradle.properties"]], [2])

    def test_a_quoted_placeholder_in_a_build_script_is_not_redacted(self):
        """Routing more files into the redaction path made an existing
        false positive matter: a quoted `${...}` was reported as a literal
        credential because the placeholder regex is anchored and the value
        keeps its quotes. Real build scripts write them exactly this way."""
        self._write("domain.gradle", 'password = "${REPO_PASSWORD}"\n')
        zones = spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS)["redaction_zones"]
        self.assertNotIn("domain.gradle", zones)

    def test_build_output_directories_stay_excluded(self):
        self._write("build/generated/Thing.java", "package x;\npublic class Thing {}\n")
        result = spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS)
        files = {e["file"] for entries in result["evidence"].values() for e in entries}
        self.assertFalse([f for f in files if f.startswith("build/")], files)


class RespectGitignoreOptInTest(unittest.TestCase):
    """--respect-gitignore is additive-only: a directory not covered by the
    hardcoded EXCLUDED_DIRS floor (unlike vendor/, venv/, etc.) should only
    disappear from the scan when the repo's own .gitignore excludes it AND
    the caller opts in via respect_gitignore=True.

    This scratch repo is a real `git init`-ed one, not just a bare
    directory with a .gitignore file: ast-grep's own native gitignore
    handling (what run_ast_grep's --no-ignore vcs omission relies on for
    the ast-grep-side half of this feature) only activates inside an
    actual VCS root, the same as ripgrep's underlying `ignore` crate --
    a .gitignore next to files with no .git present is invisible to it.
    Real target repos for this plugin are checkouts, so this is
    realistic, not a workaround."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q"], cwd=self.tmpdir, check=True)
        scratch_dir = os.path.join(self.tmpdir, "scratch_module")
        os.makedirs(scratch_dir)
        with open(os.path.join(scratch_dir, "Scratch.java"), "w") as f:
            f.write("package scratch_module;\n\n@Entity\npublic class Scratch {\n}\n")
        with open(os.path.join(self.tmpdir, ".gitignore"), "w") as f:
            f.write("scratch_module/\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_scratch_module_scanned_without_opt_in(self):
        result = spring_signal_scan.scan(self.tmpdir, scanners=SNAPSHOT_SCANNERS)
        self.assertEqual(result["files_scanned"]["java"], 1)
        self.assertIn("Scratch", result["entity_table_map"])

    def test_scratch_module_excluded_with_opt_in(self):
        result = spring_signal_scan.scan(self.tmpdir, respect_gitignore=True, scanners=SNAPSHOT_SCANNERS)
        self.assertEqual(result["files_scanned"]["java"], 0)
        self.assertNotIn("Scratch", result["entity_table_map"])


class AstGrepFailureIsAnExceptionTest(unittest.TestCase):
    """run_ast_grep() used to call sys.exit(1) on a failing ast-grep.

    That is the identical defect AstGrepNotFoundError was introduced to fix
    in find_ast_grep(), left in place at two sites because the original fix
    converted only the "binary missing" path. SystemExit derives from
    BaseException, and unittest's _handleClassSetUp catches only Exception --
    so a sys.exit() raised under setUpClass (which is where three suites call
    scan()) kills the whole test process with no "Ran N tests" line, instead
    of being reported as one class's setUpClass error.

    These tests pin the property that actually matters: an ordinary
    `except Exception` must catch it. Asserting the exception type alone
    would not -- SystemExit would satisfy an assertRaises(BaseException) just
    as well, which is precisely how this went unnoticed the first time.
    """

    class _FakeProc:
        def __init__(self, returncode=0, stdout="", stderr=""):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    def _run_with(self, proc, monkey):
        original = spring_signal_scan.subprocess.run
        spring_signal_scan.subprocess.run = lambda *a, **k: proc
        try:
            return monkey()
        finally:
            spring_signal_scan.subprocess.run = original

    def test_nonzero_exit_raises_ast_grep_error(self):
        proc = self._FakeProc(returncode=2, stderr="bad rule file")
        with self.assertRaises(spring_signal_scan.AstGrepError):
            self._run_with(proc, lambda: spring_signal_scan.run_ast_grep("ast-grep", "."))

    def test_unparseable_output_raises_ast_grep_error(self):
        proc = self._FakeProc(returncode=0, stdout="not json at all")
        with self.assertRaises(spring_signal_scan.AstGrepError):
            self._run_with(proc, lambda: spring_signal_scan.run_ast_grep("ast-grep", "."))

    def test_nonzero_exit_is_catchable_as_a_plain_exception(self):
        """The regression witness. Against the pre-fix code this fails by
        the SystemExit propagating straight through the `except Exception`."""
        proc = self._FakeProc(returncode=2, stderr="bad rule file")
        caught = None
        try:
            self._run_with(proc, lambda: spring_signal_scan.run_ast_grep("ast-grep", "."))
        except Exception as exc:  # noqa: BLE001 -- catching broadly is the point
            caught = exc
        self.assertIsNotNone(
            caught, "run_ast_grep raised something `except Exception` cannot catch")
        self.assertNotIsInstance(caught, SystemExit)

    def test_unparseable_output_is_catchable_as_a_plain_exception(self):
        proc = self._FakeProc(returncode=0, stdout="{{{")
        caught = None
        try:
            self._run_with(proc, lambda: spring_signal_scan.run_ast_grep("ast-grep", "."))
        except Exception as exc:  # noqa: BLE001 -- catching broadly is the point
            caught = exc
        self.assertIsNotNone(caught)
        self.assertNotIsInstance(caught, SystemExit)

    def test_the_failure_message_still_names_ast_grep_and_the_status(self):
        """CLI behavior is meant to be unchanged: main() prints the exception
        and exits 1, so the text a user sees must still carry the detail that
        used to be printed directly."""
        proc = self._FakeProc(returncode=3, stderr="rule parse failed")
        with self.assertRaises(spring_signal_scan.AstGrepError) as ctx:
            self._run_with(proc, lambda: spring_signal_scan.run_ast_grep("ast-grep", "."))
        message = str(ctx.exception)
        self.assertIn("ast-grep", message)
        self.assertIn("3", message)
        self.assertIn("rule parse failed", message)

    def test_not_found_error_is_still_an_ast_grep_error(self):
        """Subclassing keeps every existing `except AstGrepNotFoundError`
        call site meaning exactly what it meant before."""
        self.assertTrue(issubclass(spring_signal_scan.AstGrepNotFoundError,
                                   spring_signal_scan.AstGrepError))
