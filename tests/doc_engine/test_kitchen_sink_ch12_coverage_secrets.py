"""Kitchen-sink Ch12: citation coverage + secrets gate responsibility."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

import pytest

from tests.support.kitchen_sink.harness import _miscase_first_tag, _run
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration

PY = sys.executable


class Ch12CoverageSecretsGateTest(KitchenBoundTestCase):
    """Citation-coverage worklist/strict and secrets-check scope limits."""

    @pytest.fixture(autouse=True)
    def _bind_docs_scratch(self, kitchen_docs_scratch):
        self._docs_scratch = kitchen_docs_scratch

    def _coverage(self, docs, *extra):
        return _run(
            [
                PY,
                "-m",
                "doc_engine.tools.citation_coverage",
                docs,
                "--target-repo",
                self.kitchen.repo,
                *extra,
            ]
        )

    def _secrets(self, *paths):
        return _run([PY, "-m", "doc_engine.tools.check_no_secrets_leaked", *paths])

    def test_citation_coverage_is_a_worklist_by_default_and_a_gate_under_strict(self):
        _scratch, docs = self._docs_scratch
        _miscase_first_tag(self, os.path.join(docs, "database.md"))
        with open(os.path.join(docs, "operations.md"), "a", encoding="utf-8") as handle:
            handle.write(
                "\nBillingController.save() writes to billing_invoice on every request.\n"
            )
        self.assertEqual(
            self._coverage(docs).returncode, 0, "must be a worklist by default"
        )
        strict = self._coverage(docs, "--strict")
        self.assertEqual(strict.returncode, 1)
        self.assertIn("miscased_tag", strict.stdout)
        self.assertIn("untagged_claim", strict.stdout)

    def test_planted_credentials_fail_the_secrets_check(self):
        _scratch, docs = self._docs_scratch
        with open(
            os.path.join(docs, "configuration.md"), "a", encoding="utf-8"
        ) as handle:
            handle.write(
                "\nLeaked: AKIAABCDEFGHIJKLMNOP\n-----BEGIN RSA PRIVATE KEY-----\n"
            )
        proc = self._secrets(docs)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("aws_access_key_id", proc.stderr)
        self.assertIn("pem_private_key", proc.stderr)

    def test_placeholder_values_must_not_fire(self):
        scratch = tempfile.mkdtemp(prefix="ks_ph_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "configuration.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("password: ${DB_PASSWORD}\napi-key: CHANGEME\nsecret: <set-me>\n")
        self.assertEqual(self._secrets(path).returncode, 0)

    def test_a_secret_in_prose_is_not_caught_by_the_heuristic(self):
        """Pinned scope limit: prose passwords stay invisible to the heuristic."""
        scratch = tempfile.mkdtemp(prefix="ks_prose_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "summaries.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(
                [{"summary": "The datasource password is hunter2literalvalue"}], handle
            )
        self.assertEqual(self._secrets(path).returncode, 0)
