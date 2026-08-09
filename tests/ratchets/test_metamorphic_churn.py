"""Cohesive suite from tests/ratchets/test_metamorphic.py: SingleEditLocalityTest, BulkRenameTest, ChurnIsIdempotentTest, AppendOnlyGrowthTest, MassDeletionTest, RescanDeterminismTest, DuplicationScalesTest, HarnessIsNotVacuousTest."""

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
_TMP: Path = None
BASE: Path = None
BASE_SET = None
from tests.support.metamorphic.harness import (
    CorpusCase,
    setUpModule,
    tearDownModule,
)

class SingleEditLocalityTest(CorpusCase):
    def test_one_file_edited_moves_only_that_file(self) -> None:
        repo = self.variant()
        target = repo / "ApiSurface.java"
        target.write_text(target.read_text(encoding="utf-8")
                          .replace("@RestController", "@RestController\n@Timed", 1),
                          encoding="utf-8")
        self.assertRelation(repo, sd.confined_to(["ApiSurface.java"]),
                            "a one-file edit reached other files")

class BulkRenameTest(CorpusCase):
    """Locality at scale. A rename moves every member of the renamed file,
    so the relation is confinement to the union of old and new names."""

    def test_renaming_every_file_confines_movement_to_those_names(self) -> None:
        repo = self.variant()
        affected = []
        for java in sorted(repo.glob("*.java")):
            new = java.with_name(f"Renamed{java.name}")
            affected += [java.name, new.name]
            java.rename(new)
        self.assertRelation(repo, sd.confined_to(affected),
                            "a bulk rename moved members of untouched files")

class ChurnIsIdempotentTest(CorpusCase):
    """Sustained churn. Applying a meaning-preserving edit k times must land
    in the same place as applying it once -- idempotence, which no other
    suite in this repo asserts by name."""

    REPEATS = 5

    def test_repeated_reindent_is_stable(self) -> None:
        repo = self.variant()
        seen = []
        for _ in range(self.REPEATS):
            for java in repo.glob("*.java"):
                java.write_text(perturb.reindent(java.read_text(encoding="utf-8")),
                                encoding="utf-8")
            seen.append(sd.signals_set(repo))
        self.assertEqual(len(set(seen)), 1, "the set moved between churn rounds")
        self.assertRelation(repo, sd.unchanged(),
                            f"{self.REPEATS} rounds of reindent moved the set")

class AppendOnlyGrowthTest(CorpusCase):
    def test_adding_files_only_grows_the_set(self) -> None:
        repo = self.variant()
        for i in range(3):
            (repo / f"Added{i}.java").write_text(
                f"package fx;\n@RestController\npublic class Added{i} {{}}\n",
                encoding="utf-8")
        self.assertRelation(repo, sd.grows_only(),
                            "adding files removed an existing member")

class MassDeletionTest(CorpusCase):
    def test_deleting_files_removes_only_their_members(self) -> None:
        repo = self.variant()
        removed = [p.name for p in sorted(repo.glob("*.java"))[:3]]
        for name in removed:
            (repo / name).unlink()
        self.assertRelation(repo, sd.confined_to(removed),
                            "deleting files disturbed the survivors")

class RescanDeterminismTest(CorpusCase):
    """An invariant, not a probe: two scans of an unchanged tree must be
    equal as sets. Stated because directional-tests rule 4 records a
    re-run-and-diff probe passing against an unfixed scanner."""

    def test_two_scans_of_the_same_tree_agree(self) -> None:
        self.assertEqual(sd.signals_set(BASE), BASE_SET)

class DuplicationScalesTest(CorpusCase):
    """Whole-tree duplication must multiply every rule's count by exactly 2."""

    def test_duplicating_the_corpus_doubles_every_rule_count(self) -> None:
        repo = self.variant()
        copy_dir = repo / "copy"
        copy_dir.mkdir()
        for java in list(repo.glob("*.java")):
            shutil.copy2(java, copy_dir / java.name)
        problems = sd.check_scaling(BASE_SET, sd.signals_set(repo), 2)
        self.assertEqual(problems, [], "\n".join(problems))

class HarnessIsNotVacuousTest(CorpusCase):
    """Proves the machinery above can fail. Without this, every assertion in
    this file could be passing because the corpus scans to nothing, or
    because assertRelation never inspects anything."""

    def test_a_real_semantic_edit_is_reported_under_unchanged(self) -> None:
        repo = self.variant()
        target = repo / "ApiSurface.java"
        target.write_text(target.read_text(encoding="utf-8")
                          .replace("@RestController", "@RestController\n@Timed", 1),
                          encoding="utf-8")
        residue = sd.classify(sd.delta(BASE_SET, sd.signals_set(repo)), sd.unchanged())
        self.assertFalse(residue.is_empty(),
                         "a real added annotation produced no residue")

    def test_the_reference_corpus_is_not_empty(self) -> None:
        self.assertGreater(len(BASE_SET), 10, len(BASE_SET))
