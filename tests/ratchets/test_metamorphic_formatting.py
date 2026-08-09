"""Cohesive suite from tests/ratchets/test_metamorphic.py: FormattingIsMeaningPreservingTest, EncodingAndLineEndingsTest, IrrelevantFileTypesTest, BuildFileTypeTest."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH

import pytest

pytestmark = pytest.mark.domain_ci_meta

FIXTURES = SCRIPTS_DIR / "coverage" / "rule_fixtures"
import java_perturbations as perturb
import set_delta as sd
from tests.support.metamorphic import harness as meta
from tests.support.metamorphic.harness import CorpusCase


def setUpModule() -> None:
    meta.setUpModule()


def tearDownModule() -> None:
    meta.tearDownModule()

class FormattingIsMeaningPreservingTest(CorpusCase):
    """Every FORMATTING_ONLY transform must leave the set untouched -- except
    the one this repo has already flagged as unresolved, which is asserted
    separately below rather than skipped."""

    KNOWN_MOVES_THE_SET = "wrap_annotation_args"

    def _apply(self, name: str) -> Path:
        repo = self.variant()
        transform = perturb.FORMATTING_ONLY[name]
        for java in repo.glob("*.java"):
            java.write_text(transform(java.read_text(encoding="utf-8")),
                            encoding="utf-8")
        return repo

    def test_each_formatting_transform_changes_nothing(self) -> None:
        for name in perturb.FORMATTING_ONLY:
            if name == self.KNOWN_MOVES_THE_SET:
                continue
            with self.subTest(transform=name):
                self.assertRelation(self._apply(name), sd.unchanged(),
                                    f"{name} moved the evidence set")

    def test_wrapping_annotation_args_still_moves_the_set(self) -> None:
        """A ratchet on a known defect, asserted in the direction that is
        true today so it fails in BOTH directions.

        CONSTRAINTS.md's "Known precision tradeoffs" records this as flagged
        and unresolved: the stored `match` is only the matched node's first
        line, so splitting `@GetMapping("/x")` across lines leaves
        `@GetMapping(` behind and the member no longer compares equal. This
        suite reproduced it independently, from the scanner side rather than
        the drift-comparator side.

        **If this test starts failing, the defect was fixed.** Delete it and
        fold wrap_annotation_args back into the loop above -- do not adjust
        it to keep passing.
        """
        residue = sd.classify(
            sd.delta(meta.BASE_SET, sd.signals_set(self._apply(self.KNOWN_MOVES_THE_SET))),
            sd.unchanged())
        self.assertFalse(
            residue.is_empty(),
            "wrap_annotation_args no longer moves the set -- the first-line "
            "match defect appears fixed; see this test's docstring")

class EncodingAndLineEndingsTest(CorpusCase):
    """Closes a bound test_drift_normalization states it does not cover:
    'No encoding or line-ending perturbation.'"""

    def test_crlf_line_endings_change_nothing(self) -> None:
        repo = self.variant()
        for java in repo.glob("*.java"):
            raw = java.read_text(encoding="utf-8").replace("\n", "\r\n")
            java.write_bytes(raw.encode("utf-8"))
        self.assertRelation(repo, sd.unchanged(), "CRLF moved the evidence set")

    def test_a_utf8_bom_changes_nothing(self) -> None:
        repo = self.variant()
        for java in repo.glob("*.java"):
            java.write_bytes(b"\xef\xbb\xbf" + java.read_bytes())
        self.assertRelation(repo, sd.unchanged(), "a BOM moved the evidence set")

class IrrelevantFileTypesTest(CorpusCase):
    """Adding a file no Java rule can match must not move Java members."""

    def test_an_empty_file_adds_nothing(self) -> None:
        repo = self.variant()
        (repo / "Empty.java").write_text("", encoding="utf-8")
        self.assertRelation(repo, sd.unchanged(), "an empty file moved the set")

    def test_a_unicode_filename_is_handled(self) -> None:
        repo = self.variant()
        (repo / "Ünïcode.txt").write_text("nothing structural\n", encoding="utf-8")
        self.assertRelation(repo, sd.unchanged(), "a unicode filename moved the set")

    def test_unparseable_java_does_not_disturb_its_siblings(self) -> None:
        """A file ast-grep cannot parse must not take the rest of the corpus
        with it. Locality under a hostile input, not just a benign one."""
        repo = self.variant()
        (repo / "Broken.java").write_text("public class {{{ <<< not java\n",
                                          encoding="utf-8")
        self.assertRelation(repo, sd.confined_to(["Broken.java"]),
                            "an unparseable file disturbed other files")

class BuildFileTypeTest(CorpusCase):
    """The .gradle axis.

    These get a filename-level bucket entry and no structural signals, since
    ast-grep has no Groovy grammar. So the correct relation is confinement to
    the file itself, NOT `unchanged` -- adding one genuinely does add a
    member. Writing `unchanged` here first is what made that concrete: the
    test failed, and it was the test that was wrong, not the scanner.
    """

    def test_adding_a_gradle_file_moves_only_itself(self) -> None:
        repo = self.variant()
        (repo / "build.gradle").write_text(
            'dependencies { implementation("org.springframework.boot:x") }\n',
            encoding="utf-8")
        self.assertRelation(repo, sd.confined_to(["build.gradle"]),
                            "a .gradle file moved a member of another file")

    def test_adding_a_properties_file_moves_only_itself(self) -> None:
        repo = self.variant()
        (repo / "gradle.properties").write_text("repoPassword=literal\n",
                                                encoding="utf-8")
        self.assertRelation(repo, sd.confined_to(["gradle.properties"]),
                            "a .properties file moved a member of another file")

    def test_a_gradle_file_contributes_no_structural_rule(self) -> None:
        """The consequence of the missing Groovy grammar, asserted rather
        than assumed: whatever a .gradle file contributes, it is not a hit
        from one of the Java rules in spring_ast_grep_rules.yml."""
        repo = self.variant()
        (repo / "build.gradle").write_text("@RestController\n@Entity\n",
                                           encoding="utf-8")
        added = sd.delta(meta.BASE_SET, sd.signals_set(repo)).added
        for member in added:
            self.assertNotIn("__", member.rule_id,
                             f"a .gradle file produced a structural rule hit: {member}")
