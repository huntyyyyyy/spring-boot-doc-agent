"""E-MD0 markdown frontmatter closed-schema gate."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.domain_ci_meta

_SCRIPTS_CI = Path(__file__).resolve().parents[2] / "scripts" / "ci"
if str(_SCRIPTS_CI) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_CI))

import check_md_frontmatter as cmf  # noqa: E402
from md_frontmatter_kinds import classify  # noqa: E402
from md_frontmatter_validate import validate_doc  # noqa: E402


def test_classify_root_exempt(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("# hi\n", encoding="utf-8")
    kind, skip = classify(tmp_path, tmp_path / "CLAUDE.md")
    assert kind == "exempt"
    assert skip == "root_sot"


def test_research_requires_core_keys(tmp_path: Path) -> None:
    memo = tmp_path / "docs" / "research" / "process" / "x.md"
    memo.parent.mkdir(parents=True)
    memo.write_text(
        "---\ntitle: T\nstatus: draft\ndate: 2026-08-10\nclaim_tiers: Evidenced\n"
        "related:\n  - docs/research/README.md\n---\n\nbody\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "research" / "README.md").write_text("# r\n", encoding="utf-8")
    result = validate_doc(tmp_path, memo)
    assert result.kind == "research_memo"
    assert not any(f.level == "hard" for f in result.findings)


def test_deprecated_claim_tiers_fails_until_fix(tmp_path: Path) -> None:
    memo = tmp_path / "docs" / "research" / "process" / "y.md"
    memo.parent.mkdir(parents=True)
    memo.write_text(
        "---\ntitle: T\nstatus: draft\ndate: 2026-08-10\nclaim tiers: Evidenced\n"
        "related: []\n---\n\nbody\n",
        encoding="utf-8",
    )
    bad = validate_doc(tmp_path, memo)
    assert any("deprecated" in f.message for f in bad.findings if f.level == "hard")
    fixed = validate_doc(tmp_path, memo, fix=True)
    assert fixed.fixed_text is not None
    memo.write_text(fixed.fixed_text, encoding="utf-8")
    good = validate_doc(tmp_path, memo)
    assert not any("deprecated" in f.message for f in good.findings)


def test_bloom_gate_requires_sources(tmp_path: Path) -> None:
    memo = tmp_path / "docs" / "research" / "process" / "z.md"
    memo.parent.mkdir(parents=True)
    memo.write_text(
        "---\ntitle: T\nstatus: draft\ndate: 2026-08-10\nclaim_tiers: Evidenced\n"
        "related: []\nbloom_gate: required-through-create\nbloom_mcp:\n  - x\n---\n\nb\n",
        encoding="utf-8",
    )
    result = validate_doc(tmp_path, memo)
    assert any("sources" in f.message for f in result.findings)


def test_cli_ok_on_minimal_tree(tmp_path: Path) -> None:
    memo = tmp_path / "docs" / "research" / "process" / "ok.md"
    memo.parent.mkdir(parents=True)
    memo.write_text(
        "---\ntitle: T\nstatus: draft\ndate: 2026-08-10\nclaim_tiers: Evidenced\n"
        "related: []\n---\n\nbody\n",
        encoding="utf-8",
    )
    assert cmf.main(["--root", str(tmp_path), "--write-index"]) == 0
    assert (tmp_path / "docs" / "research" / "_frontmatter_index.yaml").is_file()
