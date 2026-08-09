"""Cohesive suite from tests/ratchets/test_metamorphic.py: setUpModule, tearDownModule, CorpusCase."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
FIXTURES = SCRIPTS_DIR / "coverage" / "rule_fixtures"
import java_perturbations as perturb
import set_delta as sd
_TMP: Path = None
BASE: Path = None
BASE_SET = None

def setUpModule() -> None:
    """One reference corpus and one reference scan, reused by every case.
    Each scan shells out to ast-grep, so rescanning per test would multiply
    the suite's runtime for no additional assurance."""
    global _TMP, BASE, BASE_SET
    _TMP = Path(tempfile.mkdtemp(prefix="metamorphic_"))
    BASE = _TMP / "base"
    shutil.copytree(FIXTURES, BASE)
    BASE_SET = sd.signals_set(BASE)
    if not BASE_SET:
        raise AssertionError(
            "the reference scan found nothing; every relation below would hold "
            "vacuously against an empty set")


def tearDownModule() -> None:
    shutil.rmtree(_TMP, ignore_errors=True)


class CorpusCase(unittest.TestCase):
    """Each test gets its own copy, so a mutation cannot leak sideways."""

    def variant(self) -> Path:
        target = Path(tempfile.mkdtemp(prefix="variant_", dir=_TMP)) / "repo"
        shutil.copytree(BASE, target)
        return target

    def assertRelation(self, repo: Path, relation, msg: str = "") -> None:
        residue = sd.classify(sd.delta(BASE_SET, sd.signals_set(repo)), relation)
        if not residue.is_empty():
            self.fail(f"{msg}\nunexplained:\n" + "\n".join(residue.describe()))
