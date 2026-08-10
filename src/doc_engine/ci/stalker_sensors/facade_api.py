"""G3: façade poke-surface regress (wrap existing poke inventory)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from doc_engine.ci.stalker_sensors.finding_records import KIND_G3, StalkerFinding


def _load_poke_module(script: Path) -> ModuleType | None:
    spec = importlib.util.spec_from_file_location("facade_poke_surface", script)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _missing_attrs(mod: ModuleType) -> list[StalkerFinding]:
    unique: dict[tuple[str, str], str] = {}
    for path in mod._iter_test_files():
        for fac, attr, rel in mod._collect_needs(path):
            unique.setdefault((fac, attr), rel)
    return [
        StalkerFinding(
            KIND_G3,
            f"{fac} missing attribute {attr!r}",
            f"poked from {rel}; re-export on façade",
        )
        for (fac, attr), rel in sorted(unique.items())
        if not mod._module_has_attr(fac, attr)
    ]


def scan_facade_api(root: Path) -> list[StalkerFinding]:
    script = root / "scripts" / "ci" / "check_facade_poke_surface.py"
    if not script.is_file():
        return [StalkerFinding(KIND_G3, "check_facade_poke_surface.py missing", str(script))]
    mod = _load_poke_module(script)
    if mod is None:
        return [StalkerFinding(KIND_G3, "cannot load façade poke script", str(script))]
    return _missing_attrs(mod)
