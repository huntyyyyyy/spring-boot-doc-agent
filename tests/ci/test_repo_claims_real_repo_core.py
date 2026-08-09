"""Cohesive suite from tests/ci/test_check_repo_claims.py: TestRealRepoCore."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import check_repo_claims as crc
import pytest
from tests.conftest import REPO_ROOT

pytestmark = pytest.mark.domain_ci_meta


class TestRealRepoCore(unittest.TestCase):
    """Against the actual tree. These are the assertions that would notice
    the checker having quietly stopped looking at anything."""

    def test_real_repo_passes(self) -> None:
        # --root must be the suite's REPO_ROOT so gate mutators that rewrite
        # CLAUDE.md / agents under a mutate.py sandbox are visible (the
        # script's own default repo_root() follows the installed package).
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "ci" / "check_repo_claims.py"),
                "--root",
                str(REPO_ROOT),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(
            result.returncode,
            0,
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_no_real_agent_declares_grep(self) -> None:
        """The backtest for check F. The fixture tests prove the check can
        fire; this proves it is aimed at the real tree, where all five agents
        declared `tools: Read, Grep, Glob, Write` before this change."""
        agents = crc._agent_definitions(REPO_ROOT)
        self.assertTrue(
            agents, "no agent definitions found — check F is aimed at nothing"
        )
        for path in agents:
            self.assertNotIn(
                "Grep", crc._declared_tools(path), f"{path.name} declares Grep"
            )

    def test_real_derived_blocks_match_registry(self) -> None:
        """Backtest for check A. Hermetic TreeCase suites prove stale numbers
        fail; this aims the same check at the committed tree so a hand-edit of
        ``<!-- derived: predicate_count -->`` (mutate: derived-count-edited)
        cannot survive."""
        markdown = crc.tracked_markdown(REPO_ROOT)
        findings = crc.check_derived_blocks(REPO_ROOT, markdown)
        self.assertEqual(
            findings,
            [],
            "; ".join(f"{f.path}:{f.line} {f.message}" for f in findings),
        )

    def test_real_bash_agents_are_scoped_by_settings(self) -> None:
        """Every agent granted Bash must be narrowed by the committed
        allowlist, since its own frontmatter cannot express the scope."""
        settings = json.loads(
            (REPO_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")
        )
        permissions = settings.get("permissions", {})
        bash_agents = [
            p.name
            for p in crc._agent_definitions(REPO_ROOT)
            if "Bash" in crc._declared_tools(p)
        ]
        if bash_agents:
            self.assertTrue(
                any(
                    e.startswith(crc.SCOPED_BASH_PREFIX)
                    for e in permissions.get("allow", [])
                ),
                f"{bash_agents} declare Bash with no scoped allow entry",
            )
            for required in crc.TEXT_SEARCH_DENIES:
                self.assertIn(required, permissions.get("deny", []))
            for required in crc.NETWORK_EGRESS_DENIES:
                self.assertIn(required, permissions.get("deny", []))

    def test_every_steering_prompt_with_a_status_has_predicates(self) -> None:
        """Scoped to the steering-prompt corpus, which is what this test's
        name has always claimed. It previously asserted over *all* missing
        findings, which was the same thing while prompts were the only
        corpus; CONSTRAINTS.md joining made the assertion wider than the
        name. Those claims are genuinely unfalsifiable today and ride the
        baseline -- that is the finding, not a reason to weaken this."""
        _, soft = crc.collect_all(REPO_ROOT)
        unchecked = [
            f.path
            for f in soft
            if f.fingerprint.startswith("C-missing:")
            and f.path.startswith("claude/steering-prompts/")
        ]
        self.assertEqual(
            unchecked, [], f"prompts with an unchecked status: {unchecked}"
        )

    def test_constraints_claims_are_actually_collected(self) -> None:
        """Non-vacuity for the corpus registry. Scoping the test above means
        an empty CONSTRAINTS.md extractor would no longer fail anything, so
        this asserts the corpus is really being read. CONSTRAINTS.md is the
        repo's densest claim store; if this ever reads zero, the extractor
        broke rather than the file becoming clean."""
        claims = [
            c for c in crc.collect_claims(REPO_ROOT) if c.corpus == "constraints"
        ]
        self.assertGreater(
            len(claims),
            10,
            "CONSTRAINTS.md bracket-tag extraction returned almost nothing",
        )
        self.assertTrue(
            any(c.status == "Resolved" for c in claims),
            f"no [Resolved] claim found; statuses seen: "
            f"{sorted({c.status for c in claims})}",
        )

    def test_bracket_tags_inside_fenced_blocks_are_not_claims(self) -> None:
        """A tag shown as an example in a code fence documents the syntax; it
        does not assert anything. Counting it would make every doc that
        explains the convention look like it carries claims."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** a real claim.\n\n"
                "```\n**[Resolved]** an example in a fence.\n```\n",
                encoding="utf-8",
            )
            claims = crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            self.assertEqual(len(claims), 1, [c.status for c in claims])

    def test_an_inline_verify_comment_opts_a_claim_in(self) -> None:
        """Read-only adoption: a CONSTRAINTS.md entry joins the checked set by
        carrying its own predicates in an HTML comment, which renders as
        nothing. No migration of the file is required."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Resolved]** ships a thing. <!-- verify: path_exists:real.txt -->\n\n"
                "**[Flagged]** unchecked entry.\n",
                encoding="utf-8",
            )
            (root / "real.txt").write_text("x", encoding="utf-8")
            claims = crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            self.assertEqual(claims[0].predicates, ("path_exists:real.txt",))
            self.assertEqual(claims[1].predicates, ())

    def test_a_long_status_tag_is_not_silently_dropped(self) -> None:
        """Regression: the first extractor capped the tag at 60 characters,
        which silently omitted three real CONSTRAINTS.md entries -- the long
        '[New info — ...]' corrections, i.e. exactly the claims that record a
        previous claim going wrong. Undercounting inflates the checked ratio,
        so the omission would have made the numbers look better than reality."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            long_tag = (
                "**[New info — the wording above ran ahead of the code, "
                "corrected 2026-07-24]** body text.\n"
            )
            (root / "CONSTRAINTS.md").write_text(long_tag, encoding="utf-8")
            claims = crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md")
            self.assertEqual(len(claims), 1, "long status tag was dropped")
            self.assertTrue(
                claims[0].status.startswith("New info"), claims[0].status
            )

    def test_a_tag_does_not_match_across_a_newline(self) -> None:
        """The bound that replaced the length cap. Without it an unterminated
        `**[` would swallow the rest of the document as one giant status."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "CONSTRAINTS.md").write_text(
                "**[Unterminated tag\nspanning lines]** and more.\n", encoding="utf-8"
            )
            self.assertEqual(
                crc.extract_bracket_tag_claims(root, root / "CONSTRAINTS.md"), []
            )
