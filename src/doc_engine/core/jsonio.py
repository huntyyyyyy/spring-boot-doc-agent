"""UTF-8 JSON file load/dump for kernel artifact I/O.

Concept home for the repeated ``open`` + ``json.load`` / ``json.dump``
patterns across CLI, pipeline, and Stage-0 tools. Not a grab-bag utils
module: only JSON file I/O belongs here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Parse a UTF-8 JSON file."""
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: str | Path, data: Any, *, indent: int = 2) -> None:
    """Write *data* as UTF-8 JSON (stdlib ``json.dump``; no trailing newline)."""
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=indent)
