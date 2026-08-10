#!/usr/bin/env python3
"""Fail closed when curated façades export private ``_`` names or residual bins.

E-COH1 fitness (tach/Nx/Packwerk public-interface pattern).

Run::

    python3 scripts/ci/check_public_surface.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from doc_engine.ci.public_surface_policy import (  # noqa: E402
    PUBLIC_ONLY_MODULES,
    forbidden_residual_paths,
    module_private_all_exports,
)


def _private_export_errors() -> list[str]:
    errors: list[str] = []
    for module_name in PUBLIC_ONLY_MODULES:
        privates = module_private_all_exports(module_name)
        if privates:
            errors.append(
                f"{module_name}: __all__ exports private names {privates!r}"
            )
    return errors


def _residual_path_errors() -> list[str]:
    return [
        f"residual bin path present: {rel}"
        for rel in forbidden_residual_paths(REPO_ROOT)
    ]


def main() -> int:
    errors = _private_export_errors() + _residual_path_errors()
    if not errors:
        print(
            f"public-surface fitness OK "
            f"({len(PUBLIC_ONLY_MODULES)} modules, no residual bins)"
        )
        return 0
    print("public-surface fitness FAILED:", file=sys.stderr)
    for line in errors:
        print(f"  - {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
