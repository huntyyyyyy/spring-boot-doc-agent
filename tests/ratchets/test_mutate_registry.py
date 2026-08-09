"""Cohesive suite from tests/ratchets/test_mutate.py: RegistryLoadTest, RegistryAnchorsTest."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import mutate
import mutator_registry

import pytest

pytestmark = pytest.mark.domain_ci_meta

_KNOWN_GATE_MUTATOR_NAMES = frozenset({
    "secret-heuristic-stops-unquoting",
    "build-file-guard-loosened",
    "relation-permits-everything",
    "query-limit-ceiling-removed",
    "context-packet-budget-trim-disabled",
    "freshness-mismatch-always-fresh",
    "agent-regains-grep",
    "rule-loses-its-args-form",
    "derived-count-edited",
    "prompt-contract-drifts",
})

class RegistryLoadTest(unittest.TestCase):
    """OCP registry loads the catalog; harness does not own the operator list."""

    def tearDown(self) -> None:
        mutator_registry.clear_sources()

    def test_load_registry_returns_all_known_mutators(self) -> None:
        loaded = mutator_registry.load_registry()
        names = {m.name for m in loaded}
        self.assertTrue(
            _KNOWN_GATE_MUTATOR_NAMES.issubset(names),
            f"missing from registry: {_KNOWN_GATE_MUTATOR_NAMES - names}",
        )
        self.assertEqual(names, mutator_registry.known_names())

    def test_mutate_mutators_alias_matches_registry(self) -> None:
        self.assertEqual(
            [m.name for m in mutate.MUTATORS],
            [m.name for m in mutator_registry.all_mutators()],
        )

    def test_register_source_extends_catalog(self) -> None:
        extra = mutate.Mutator(
            "incident-seeded-extra", "scripts/ratchets/set_delta.py", "",
            "THE RESIDUE IS THE FINDING", "THE RESIDUE IS THE FINDING!",
            "test_set_delta.py",
            "registry OCP extension must accept an incident-seeded mutator",
        )
        mutator_registry.register_source(lambda: (extra,))
        self.assertIn("incident-seeded-extra", mutator_registry.known_names())

    def test_short_why_is_rejected(self) -> None:
        bad = mutate.Mutator(
            "too-vague", "scripts/ratchets/set_delta.py", "",
            "x", "y", "test_set_delta.py", "short",
        )
        mutator_registry.register_source(lambda: (bad,))
        with self.assertRaises(ValueError):
            mutator_registry.load_registry()

class RegistryAnchorsTest(unittest.TestCase):
    """Every mutator must still find its anchor in the real tree."""

    def test_every_mutator_anchor_exists(self) -> None:
        """A drifted anchor is a mutator that silently tests nothing. Checked
        the way the mutator itself locates its target: structurally for the
        ast-grep ones, literally for the rest -- asserting a substring against
        a pattern containing `$V` would fail for the wrong reason."""
        for m in mutate.MUTATORS:
            with self.subTest(mutator=m.name):
                path = mutate.REPO_ROOT / m.path
                self.assertTrue(path.is_file(), f"{m.path} is missing")
                if m.lang:
                    found = subprocess.run(
                        ["ast-grep", "run", "-l", m.lang, "-p", m.find,
                         "--json=compact", str(path)],
                        capture_output=True, text=True)
                    self.assertNotEqual(
                        json.loads(found.stdout or "[]"), [],
                        f"{m.name}'s structural pattern matches nothing in {m.path}")
                else:
                    self.assertIn(m.find, path.read_text(encoding="utf-8"),
                                  f"{m.name}'s literal anchor has drifted out of "
                                  f"{m.path}; it is testing nothing")

    def test_literal_mutators_state_why_they_are_not_structural(self) -> None:
        """Text matching is the thing this repo spent a release removing. A
        literal anchor is allowed, but only for the two reasons the Mutator
        docstring gives, so the count is pinned here rather than left to grow
        quietly."""
        literal = {m.path for m in mutate.MUTATORS if not m.lang}
        self.assertEqual(
            literal,
            {"adapters/claude/agents/gap-analyzer.md",
             "adapters/claude/agents/file-summarizer.md", "CLAUDE.md",
             "src/doc_engine/scanning/resources/spring_ast_grep_rules.yml"},
            "a new literal mutator appeared; either make it structural or "
            "extend Mutator's docstring with the reason it cannot be")

    def test_every_mutator_names_a_real_suite(self) -> None:
        for m in mutate.MUTATORS:
            with self.subTest(mutator=m.name):
                try:
                    path = mutate.resolve_suite_path(
                        mutate.REPO_ROOT, m.expected_caught_by
                    )
                except FileNotFoundError:
                    path = None
                self.assertIsNotNone(
                    path,
                    f"{m.name} names a suite that does not exist",
                )

    def test_resolve_suite_path_finds_nested_taxonomy_suites(self) -> None:
        """Regression: flat tests/<name> lookup broke after tests/ nesting."""
        for suite, fragment in (
            ("test_set_delta.py", "ratchets"),
            ("test_secret_heuristics.py", "doc_engine"),
            ("test_check_repo_claims.py", "ci"),
        ):
            with self.subTest(suite=suite):
                path = mutate.resolve_suite_path(mutate.REPO_ROOT, suite)
                self.assertTrue(path.is_file(), suite)
                self.assertIn(fragment, path.as_posix())
                self.assertEqual(path.name, suite)

    def test_every_mutator_states_why(self) -> None:
        """A survivor report is only actionable if it says what stopped being
        defended. An empty `why` makes the report a name and a shrug."""
        for m in mutate.MUTATORS:
            with self.subTest(mutator=m.name):
                self.assertGreater(len(m.why.strip()), 20, m.name)

    def test_mutator_names_are_unique(self) -> None:
        names = [m.name for m in mutate.MUTATORS]
        self.assertEqual(len(names), len(set(names)))

    def test_a_mutation_actually_changes_the_text(self) -> None:
        for m in mutate.MUTATORS:
            with self.subTest(mutator=m.name):
                self.assertNotEqual(m.find, m.replace, m.name)
