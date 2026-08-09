"""Kitchen-sink Ch10 staleness drift."""

from __future__ import annotations

import json
import os

import pytest

from tests.support.kitchen_sink.constants import (
    DUP_LEDGER,
    PY,
    SECRETS_YML,
    TWO_ENTITIES,
)
from tests.support.kitchen_sink.harness import _run
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch10StalenessTest(KitchenBoundTestCase):
    """Drift as a staleness detector, on a copy so mutation cannot perturb the
    artifacts every other class reads (and so test order stays irrelevant)."""

    @pytest.fixture(autouse=True)
    def _bind_repo_copy(self, kitchen_repo_copy):
        # unittest.TestCase cannot take fixture args on test methods (pytest).
        self.repo = kitchen_repo_copy

    def _drift(self):
        out = os.path.join(os.path.dirname(self.repo), "drift.json")
        proc = _run(
            [
                PY,
                "-m",
                "doc_engine.tools.spring_drift_check",
                self.repo,
                os.path.join(self.kitchen.out, "spring_signals.json"),
                "--manifest",
                os.path.join(self.kitchen.out, "run_manifest.json"),
                "--out",
                out,
            ]
        )
        self.assertIn(proc.returncode, (0, 1), proc.stdout + proc.stderr)
        with open(out, encoding="utf-8") as f:
            return json.load(f)

    def _statuses(self, report, rel):
        return {r["status"] for r in report["results"] if r.get("file") == rel}

    def _mutate(self, rel, old, new):
        path = os.path.join(self.repo, rel.replace("/", os.sep))
        text = open(path, encoding="utf-8").read()
        self.addCleanup(
            lambda: open(path, "w", encoding="utf-8", newline="\n").write(text)
        )
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text.replace(old, new) if old else text + new)

    def test_renamed_table_drifts_its_citation(self):
        self._mutate(TWO_ENTITIES, 'name = "alpha_tbl"', 'name = "alpha_renamed"')
        self.assertIn("drifted", self._statuses(self._drift(), TWO_ENTITIES))

    def test_deleted_file_marks_its_citations_deleted(self):
        path = os.path.join(self.repo, DUP_LEDGER.replace("/", os.sep))
        text = open(path, encoding="utf-8").read()
        os.remove(path)
        self.addCleanup(
            lambda: open(path, "w", encoding="utf-8", newline="\n").write(text)
        )
        self.assertIn("file_deleted", self._statuses(self._drift(), DUP_LEDGER))

    def test_config_value_only_change_is_flagged_for_review(self):
        """The enterprise case this outcome exists for: checked-in config is a
        placeholder and real values arrive at deploy time, so a value moving
        under an unchanged key means something unusual happened."""
        self._mutate(SECRETS_YML, "hunter2literalvalue", "differentliteralvalue")
        self.assertIn(
            "config_values_only_changed_review_needed",
            self._statuses(self._drift(), SECRETS_YML),
        )

    def test_added_config_key_is_structural_drift(self):
        self._mutate(SECRETS_YML, None, "extra:\n  added: 1\n")
        self.assertIn(
            "config_structure_changed",
            self._statuses(self._drift(), SECRETS_YML),
        )
