"""Cohesive suite from tests/ci/test_check_no_client_identifiers.py: DenylistPassTest, TrackedTreeDenylistTest, CliExitCodeTest."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import check_no_client_identifiers as gate
from tests.support.client_identifiers.harness import findings, run_main

class DenylistPassTest(unittest.TestCase):
    def test_a_name_from_the_checkout_is_caught(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp)
            src = checkout / "src" / "main" / "java" / "com" / "acme" / "service"
            src.mkdir(parents=True)
            (src / "AcmeOrderService.java").write_text("class AcmeOrderService {}")
            result: List[str] = []
            gate._denylist_pass(
                "the aggregate mentions AcmeOrderService in passing",
                checkout, result)
            self.assertEqual(len(result), 1)
            self.assertIn("AcmeOrderService", result[0])

    def test_short_names_are_not_flagged(self) -> None:
        """Very short stems produce noise ('Ids') -- the >=6 char floor is
        the documented reason this exists."""
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp)
            src = checkout / "src" / "main" / "java"
            src.mkdir(parents=True)
            (src / "Ids.java").write_text("class Ids {}")
            result: List[str] = []
            gate._denylist_pass(
                "nothing here mentions Ids by name, oh wait Ids", checkout, result)
            self.assertEqual(result, [])

    def test_a_name_absent_from_the_payload_is_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            checkout = Path(tmp)
            src = checkout / "src" / "main" / "java"
            src.mkdir(parents=True)
            (src / "AcmeOrderService.java").write_text("class AcmeOrderService {}")
            result: List[str] = []
            gate._denylist_pass("clean payload, no identifiers at all", checkout, result)
            self.assertEqual(result, [])


class TrackedTreeDenylistTest(unittest.TestCase):
    """Repo-wide denylist: plant a token outside the denylist file and assert bite."""

    def test_denylist_file_loads_at_least_one_token(self) -> None:
        tokens = gate.load_denylist(REPO_ROOT)
        self.assertGreaterEqual(len(tokens), 1)

    def test_planted_token_in_temp_path_is_reported(self) -> None:
        tokens = gate.load_denylist(REPO_ROOT)
        token = tokens[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = "docs/note.md"
            path = root / rel
            path.parent.mkdir(parents=True)
            path.write_text(f"mentions {token} once\n", encoding="utf-8")
            findings = gate.scan_paths_for_tokens(
                root, [rel], tokens=tokens, skip_denylist_file=True
            )
            self.assertTrue(findings)
            self.assertTrue(any("docs/note.md" in f for f in findings))
            self.assertTrue(any("content matches a denylist entry" in f for f in findings))
            joined = "\n".join(findings)
            self.assertNotIn(token, joined)

    def test_planted_token_in_path_name_is_reported(self) -> None:
        tokens = gate.load_denylist(REPO_ROOT)
        token = tokens[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = f"vendor/{token}/README.md"
            path = root / rel
            path.parent.mkdir(parents=True)
            path.write_text("clean body\n", encoding="utf-8")
            findings = gate.scan_paths_for_tokens(
                root, [rel], tokens=tokens, skip_denylist_file=True
            )
            self.assertTrue(any("path" in f and "matches a denylist entry" in f for f in findings))
            joined = "\n".join(findings)
            self.assertNotIn(token, joined)
            self.assertIn("<denylist-token>", joined)

    def test_clean_temp_tree_has_no_findings(self) -> None:
        tokens = gate.load_denylist(REPO_ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = "README.md"
            (root / rel).write_text("no client checkout names here\n", encoding="utf-8")
            self.assertEqual(
                gate.scan_paths_for_tokens(
                    root, [rel], tokens=tokens, skip_denylist_file=True
                ),
                [],
            )

    def test_tracked_tree_cli_exits_zero_on_this_repo(self) -> None:
        code, out, err = run_main(["--tracked-tree"])
        self.assertEqual(code, 0, err)
        self.assertIn("clean tracked tree", out)


class CliExitCodeTest(unittest.TestCase):
    def test_a_clean_aggregate_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aggregate.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "_producer": "stage0-oracle-compare",
                "evidence_tier": "source-text",
                "shared_input_digest": "0" * 64,
                "java_files_scanned": 0,
                "interfaces_with_extends": 0,
                "summaries": [],
                "misses": [],
                "unclassified_total": 0,
                "thresholds": {"min_recall": None, "max_unclassified": None, "note": ""}
            }))
            code, out, _ = run_main([str(path)])
            self.assertEqual(code, 0)
            self.assertIn("clean", out)

    def test_a_violation_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aggregate.json"
            path.write_text(json.dumps({"not_a_real_key": 1}))
            code, _, err = run_main([str(path)])
            self.assertEqual(code, 1)
            self.assertIn("REDACTION GATE FAILED", err)

    def test_a_missing_file_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "does_not_exist.json"
            code, _, err = run_main([str(missing)])
            self.assertEqual(code, 1)
            self.assertIn("no aggregate at", err)

    def test_invalid_json_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aggregate.json"
            path.write_text("not valid json {")
            code, _, err = run_main([str(path)])
            self.assertEqual(code, 1)
            self.assertIn("not valid JSON", err)

    def test_usage_error_exits_two(self) -> None:
        code, _, err = run_main([])
        self.assertEqual(code, 2)
        self.assertIn("aggregate path required", err)
