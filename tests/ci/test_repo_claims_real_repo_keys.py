"""Cohesive suite from tests/ci/test_check_repo_claims.py: TestRealRepoKeys."""

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
from tests.support.repo_claims.tree import TreeCase, build_tree

class TestRealRepoKeys(unittest.TestCase):
    """Against the actual tree. These are the assertions that would notice
the checker having quietly stopped looking at anything."""
def test_predicates_attach_to_the_claim_that_declares_them(self) -> None:
        """A verify: comment belongs to the tag above it, not to every tag in
        the file -- otherwise one opted-in entry would silently mark the whole
        document as checked."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Flagged]** first, unchecked.\n\n"
                "**[Resolved]** second. <!-- verify: path_absent:gone.txt -->\n",
                encoding="utf-8")
            claims = crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            self.assertEqual(claims[0].predicates, ())
            self.assertEqual(claims[1].predicates, ("path_absent:gone.txt",))

def test_claim_key_survives_insert_above(self) -> None:
        """Ordinal keys churned the baseline on every CONSTRAINTS edit; content
        digests must not."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = (
                "**[Resolved]** ships the ledger beside signals.\n\n"
                "**[Flagged]** unchecked hole.\n"
            )
            (root / "CONSTRAINTS.md").write_text(body, encoding="utf-8")
            before = {
                c.status: c.key
                for c in crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            }
            (root / "CONSTRAINTS.md").write_text(
                "**[New info]** inserted above.\n\n" + body, encoding="utf-8")
            after = {
                c.status: c.key
                for c in crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            }
            self.assertEqual(before["Resolved"], after["Resolved"])
            self.assertEqual(before["Flagged"], after["Flagged"])
            self.assertNotEqual(after["New info"], before["Resolved"])

def test_claim_key_follows_body_not_position_on_reorder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** alpha body unique.\n\n"
                "**[Flagged]** beta body unique.\n",
                encoding="utf-8")
            first = {
                c.status: c.key
                for c in crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            }
            (root / "CONSTRAINTS.md").write_text(
                "**[Flagged]** beta body unique.\n\n"
                "**[Resolved]** alpha body unique.\n",
                encoding="utf-8")
            second = {
                c.status: c.key
                for c in crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            }
            self.assertEqual(first["Resolved"], second["Resolved"])
            self.assertEqual(first["Flagged"], second["Flagged"])

def test_claim_key_changes_when_lead_sentence_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** original lead sentence about the tool.\n",
                encoding="utf-8")
            key1 = crc.extract_bracket_tag_claims(
                root, root / "CONSTRAINTS.md")[0].key
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** completely different lead about another fact.\n",
                encoding="utf-8")
            key2 = crc.extract_bracket_tag_claims(
                root, root / "CONSTRAINTS.md")[0].key
            self.assertNotEqual(key1, key2)

def test_claim_key_ignores_verify_comment_text(self) -> None:
        """Adding predicates must not reinvent identity."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** same lead about the ledger.\n", encoding="utf-8")
            key1 = crc.extract_bracket_tag_claims(
                root, root / "CONSTRAINTS.md")[0].key
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** same lead about the ledger. "
                "<!-- verify: path_exists:x.txt -->\n",
                encoding="utf-8")
            key2 = crc.extract_bracket_tag_claims(
                root, root / "CONSTRAINTS.md")[0].key
            self.assertEqual(key1, key2)

def test_refuse_revival_tombstone_exempts_absent_glob(self) -> None:
        """Intentional absence prose must not fail check B on a zero-match glob."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "CI refuses revival of `scripts/test_*.py` forwarders.\n",
                encoding="utf-8")
            self.assertEqual(crc.check_references(root, ["CONSTRAINTS.md"]), [])

def test_live_claim_still_flags_absent_glob(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "Wire suites via `scripts/test_*.py` in CI.\n",
                encoding="utf-8")
            findings = crc.check_references(root, ["CONSTRAINTS.md"])
            self.assertTrue(any("scripts/test_*.py" in f.message for f in findings),
                            findings)

def test_the_checker_actually_inspects_files(self) -> None:
        """Non-vacuity against the real tree: if tracked_markdown() ever
        returned nothing, every markdown check would report clean forever."""
        self.assertGreater(len(crc.tracked_markdown(REPO_ROOT)), 20)

def test_every_derivation_key_is_computable(self) -> None:
        for key, fn in crc.DERIVATIONS.items():
            with self.subTest(key=key):
                value = fn(REPO_ROOT)
                self.assertTrue(value.isdigit() and int(value) > 0,
                                f"{key} produced {value!r}")

def test_codeql_rule_count_matches_rule_coverage_denominator(self) -> None:
        """Denominator SoR is the CodeQL pack — both `=` and `as rule_id` forms."""
        import sys
        coverage_dir = str(REPO_ROOT / "scripts" / "coverage")
        if coverage_dir not in sys.path:
            sys.path.insert(0, coverage_dir)
        import rule_coverage as rc  # noqa: E402

        derived = crc.DERIVATIONS["codeql_rule_count"](REPO_ROOT)
        self.assertEqual(derived, str(len(rc.rule_ids())))
        self.assertIn("raw_queries__query", rc.rule_ids())
