"""Cohesive suite from tests/ci/test_check_repo_claims.py: build_tree, TreeCase."""

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

def build_tree(root: Path) -> None:
    """A miniature repo with the shape the checker cares about. Deliberately
    not a copy of the real one: a fixture that tracks the real tree would
    drift with it, which is the failure this whole script is about."""
    (root / ".git").mkdir()
    (root / "scripts").mkdir()
    (root / "tests").mkdir()
    (root / "skills").mkdir()
    (root / "docs" / "process" / "steering-prompts").mkdir(parents=True)
    (root / ".github" / "workflows").mkdir(parents=True)

    (root / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\n",
        encoding="utf-8")
    (root / "scripts" / "widget.py").write_text(
        "def do_a_thing():\n    return 1\n", encoding="utf-8")
    (root / "tests" / "test_widget.py").write_text(
        "def test_one():\n    pass\n\n\ndef test_two():\n    pass\n",
        encoding="utf-8")
    (root / ".github" / "workflows" / "ci.yml").write_text(
        "jobs:\n  test:\n    steps:\n"
        "      - name: pytest\n        run: pytest\n",
        encoding="utf-8")
    (root / "README.md").write_text(
        "See `scripts/widget.py` and `do_a_thing()`.\n", encoding="utf-8")
    (root / "docs" / "process" / "steering-prompts" / "01-x-research-prompt.md").write_text(
        "---\nstatus: resolved\nverify:\n  - path_exists:scripts/widget.py\n---\n\nBody.\n",
        encoding="utf-8")


class TreeCase(unittest.TestCase):
    """Runs the checker against a temp tree. `git ls-files` is stubbed rather
    than a real repo being initialized: the tests must not depend on git
    being installed, configured, or on this machine's global gitignore --
    one of which has already surprised a session here."""

    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp())
        build_tree(self.dir)
        self._real_tracked = crc.tracked_files
        crc.tracked_files = self._fake_tracked  # type: ignore[assignment]

    def tearDown(self) -> None:
        crc.tracked_files = self._real_tracked  # type: ignore[assignment]
        shutil.rmtree(self.dir, ignore_errors=True)

    def _fake_tracked(self, root: Path) -> list:
        return [p.relative_to(root).as_posix()
                for p in sorted(root.rglob("*"))
                if p.is_file() and ".git" not in p.parts]

    def run_check(self) -> int:
        return crc.main(["--root", str(self.dir),
                         "--baseline", str(self.dir / "missing_baseline.json")])

    def write(self, rel: str, text: str) -> None:
        write_text_creating_parents(self.dir / rel, text)


def write_text_creating_parents(path: Path, text: str) -> None:
    """Create parent dirs then write UTF-8 text (fixture tree helper)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
