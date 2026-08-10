"""Build ``python -m`` argv lists for local-runner phases."""

from __future__ import annotations

import sys


def py_mod(module: str, *args: str) -> list[str]:
    return [sys.executable, "-m", module, *args]
