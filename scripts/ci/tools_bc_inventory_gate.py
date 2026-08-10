"""tools_bc_inventory_gate — set-equality over tools/*.py vs inventory JSON.

Wave-0 E-REPO bite: every product tool module must appear in
``docs/design/tools_bc_inventory.json``. Orphans and stale rows fail CI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Set, Tuple

INVENTORY_REL = Path("docs/design/tools_bc_inventory.json")
TOOLS_REL = Path("src/doc_engine/tools")


def tools_modules(root: Path) -> Set[str]:
    tools = root / TOOLS_REL
    return {p.name for p in tools.glob("*.py") if p.name != "__init__.py"}


def inventory_modules(root: Path) -> Set[str]:
    data = json.loads((root / INVENTORY_REL).read_text(encoding="utf-8"))
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("inventory missing entries list")
    modules: Set[str] = set()
    for row in entries:
        if not isinstance(row, dict) or "module" not in row:
            raise ValueError(f"bad inventory row: {row!r}")
        modules.add(str(row["module"]))
    return modules


def check_tools_bc_inventory(root: Path) -> Tuple[bool, str]:
    """Return (ok, explanation) for claims ``behavior:`` or pytest."""
    inv_path = root / INVENTORY_REL
    if not inv_path.is_file():
        return False, f"missing inventory {INVENTORY_REL.as_posix()}"
    try:
        on_disk = tools_modules(root)
        listed = inventory_modules(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return False, f"inventory unreadable: {exc}"
    missing = sorted(on_disk - listed)
    extra = sorted(listed - on_disk)
    if missing or extra:
        return False, (
            f"tools inventory drift missing={missing!r} extra={extra!r}"
        )
    return True, f"tools inventory covers {len(on_disk)} modules"
