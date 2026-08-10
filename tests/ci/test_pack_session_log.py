"""Unit tests for session-log LOC packer (no nest rewrite).

Run: ``python3 -m pytest tests/ci/test_pack_session_log.py -q``.
"""

from __future__ import annotations

import unittest

from scripts.process.pack_session_log import (
    Entry,
    pack_entries,
    parse_entries,
    shard_filename,
    shard_sort_key,
    slugify,
)


class PackSessionLogTests(unittest.TestCase):
    def test_parse_preserves_order(self) -> None:
        text = (
            "## 2026-07-25 — later heading\n\nbody\n\n"
            "## 2026-07-24 — earlier date after (history quirk)\n\nbody\n"
        )
        entries = parse_entries(text)
        self.assertEqual([e.date for e in entries], ["2026-07-25", "2026-07-24"])
        self.assertEqual(entries[0].title, "later heading")

    def test_slugify_content(self) -> None:
        self.assertEqual(
            slugify("E-MDC0 optimized MDC DevEx (activation algebra)"),
            "e-mdc0-optimized-mdc-devex-activation-algebra",
        )

    def test_sort_key_date_then_slug(self) -> None:
        shard = [
            Entry(
                "2026-07-23",
                "## 2026-07-23 — Stray scaffolding on wrong branch\n\nbody\n",
            )
        ]
        self.assertEqual(
            shard_sort_key(shard),
            "2026-07-23__stray-scaffolding-on-wrong-branch",
        )

    def test_filename_collision_numeric_suffix(self) -> None:
        used: set[str] = set()
        a = [Entry("2026-08-10", "## 2026-08-10 — Same title\n\n")]
        b = [Entry("2026-08-10", "## 2026-08-10 — Same title\n\n")]
        self.assertTrue(shard_filename(a, used).endswith("same-title.md"))
        self.assertTrue(shard_filename(b, used).endswith("same-title-2.md"))

    def test_greedy_respects_target(self) -> None:
        entries = [
            Entry("2026-08-01", "## 2026-08-01 — a\n" + ("x\n" * 40)),
            Entry("2026-08-01", "## 2026-08-01 — b\n" + ("y\n" * 40)),
            Entry("2026-08-02", "## 2026-08-02 — c\n" + ("z\n" * 40)),
        ]
        shards = pack_entries(entries, target=90)
        self.assertGreaterEqual(len(shards), 2)
        from scripts.process.pack_session_log import header_line_count

        for shard in shards:
            lines = header_line_count(shard, target=90) + sum(e.lines for e in shard)
            if len(shard) > 1:
                self.assertLessEqual(lines, 90)


if __name__ == "__main__":
    unittest.main()
