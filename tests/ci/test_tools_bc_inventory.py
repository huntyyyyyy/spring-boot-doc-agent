"""CI: tools_bc_inventory.json covers every doc_engine.tools module."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPTS_CI = REPO / "scripts" / "ci"
if str(SCRIPTS_CI) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_CI))

from tools_bc_inventory_gate import (  # noqa: E402
    INVENTORY_REL,
    check_tools_bc_inventory,
    tools_modules,
)

pytestmark = pytest.mark.domain_ci_meta



def test_inventory_file_exists() -> None:
    assert (REPO / INVENTORY_REL).is_file()


def test_tools_bc_inventory_covers_all_modules() -> None:
    ok, detail = check_tools_bc_inventory(REPO)
    assert ok, detail


def test_domain_map_exists_and_points_at_inventory() -> None:
    domain_map = REPO / "DOMAIN_MAP.md"
    assert domain_map.is_file()
    text = domain_map.read_text(encoding="utf-8")
    assert "tools_bc_inventory.json" in text
    assert "quality-backlog.md" in text


def test_tools_tree_non_empty() -> None:
    assert tools_modules(REPO), "expected tools/*.py modules"
