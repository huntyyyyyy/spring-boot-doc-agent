#!/usr/bin/env python3
"""E-MD0 kind map + closed frontmatter allowlists (corpus C)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, FrozenSet, Optional, Tuple

Kind = str

DEPRECATED_KEYS: Dict[str, str] = {
    "claim tiers": "claim_tiers",
    "research date": "date",
}

RESEARCH_REQUIRED: FrozenSet[str] = frozenset(
    {"title", "status", "date", "claim_tiers", "related"}
)
RESEARCH_ALLOWED: FrozenSet[str] = RESEARCH_REQUIRED | frozenset(
    {
        "epic",
        "epic_seed",
        "category",
        "product",
        "synthesis",
        "parent",
        "siblings",
        "wave",
        "segment",
        "backlog",
        "do_not",
        "spec_gate",
        "bloom_gate",
        "bloom_mcp",
        "sources",
        "last_reviewed",
        "freshness",
        "superseded_by",
        "aliases",
        "stars_as_of",
        "arxiv_verified",
        "gh_sor_bar",
        "human_review_floor",
        "research_window",
        "ledger_archive",
        "rule",
        "note",
        "epics",
        "deepwiki",
        "skill",
        "tools",
        "implement_now",
        "approved_decisions",
        "approved_policies",
        "artifact_policy",
        "research",
        "kind",
        "id",
        "completeness",
        "last_refined",
        "tags",
        "path",
        "epub_anchors",
        "prefer_sources",
        "design",
        "branch",
        "depends_on",
        "awaiting_merge",
        "approved_by",
        "bar_raise",
        "stack_rescope",
        "critique",
        "epic_ids",
        "invariants",
        "sources_of_future",
        "ci_run",
        "tip_at_detection",
        "gh_discernment",
        "gh_api_stamp",
        "spec_feeds",
        "amends",
        "doctrine",
        "supersedes_partial",
        "supersedes",
        "base_sha",
    }
)

DDIA_REQUIRED: FrozenSet[str] = frozenset(
    {"id", "kind", "completeness", "last_refined"}
)
DDIA_ALLOWED: FrozenSet[str] = DDIA_REQUIRED | frozenset(
    {"title", "tags", "related", "path", "epub_anchors", "aliases"}
)

ROOT_EXEMPT = frozenset(
    {
        "AGENTS.md",
        "CLAUDE.md",
        "CONSTRAINTS.md",
        "CONTRIBUTING.md",
        "DOMAIN_MAP.md",
        "MATURITY_ASSESSMENT.md",
        "README.md",
        "STATUS.md",
    }
)

SOURCE_NEST_KEYS = frozenset(
    {"llms_txt", "deepwiki_ask", "arxiv", "github", "mcp", "web"}
)


def classify(repo: Path, path: Path) -> Tuple[Kind, Optional[str]]:
    """Return (kind, skip_reason). skip_reason set ⇒ checker ignores file."""
    rel = path.resolve().relative_to(repo.resolve()).as_posix()
    name = path.name
    if name.startswith("_") and name.endswith((".yaml", ".yml", ".md")):
        return "exempt", "generated_or_private"
    if name in ROOT_EXEMPT and "/" not in rel:
        return "exempt", "root_sot"
    if rel.endswith("/README.md") or name == "README.md":
        return "exempt", "readme_index"
    if "docs/process/session-log/" in rel or rel == "docs/process/session-log.md":
        return "session_pack", "packer_owned"
    if "/archive/" in rel or rel.startswith("docs/research/archive/"):
        return "exempt", "archive"
    if name in {"COMPLETENESS.md", "INDEX.md", "_TEMPLATE.md"}:
        return "exempt", "ddia_meta"
    if "docs/design/ddia-north-star/meta/" in rel:
        return "exempt", "ddia_meta"
    if "docs/design/ddia-north-star/" in rel:
        return "ddia_page", None
    if rel.startswith("docs/research/") and rel.endswith(".md"):
        return "research_memo", None
    if rel.startswith("docs/design/") and rel.count("/") == 2 and rel.endswith(".md"):
        return "design_epic", None
    if "docs/process/steering-prompts/" in rel:
        return "steering", None
    if name == "SKILL.md" or "/agents/" in rel:
        return "skill_agent", None
    return "exempt", "outside_gated_kinds"


def required_keys(kind: Kind) -> FrozenSet[str]:
    if kind in {"research_memo", "design_epic"}:
        return RESEARCH_REQUIRED
    if kind == "ddia_page":
        return DDIA_REQUIRED
    return frozenset()


def allowed_keys(kind: Kind) -> FrozenSet[str]:
    if kind in {"research_memo", "design_epic"}:
        return RESEARCH_ALLOWED
    if kind == "ddia_page":
        return DDIA_ALLOWED
    if kind == "steering":
        return frozenset(
            {"status", "verify", "related", "note", "category", "authored", "title"}
        )
    if kind == "skill_agent":
        return frozenset(
            {"name", "description", "tools", "related", "title", "status", "date"}
        )
    return frozenset()


def unknown_keys_hard(kind: Kind) -> bool:
    return kind in {"research_memo", "design_epic", "ddia_page"}
