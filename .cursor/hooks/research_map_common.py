"""Shared helpers for research-map look-first hooks (DOC7)."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
MAP_REL = "docs/research/README.md"
RECEIPT_DIR = Path(os.environ.get("XDG_RUNTIME_DIR") or "/tmp") / "cursor-doc1"
PATH_KEYS = ("path", "file_path", "target_file", "target_notebook")


def receipt_path() -> Path:
    key = hashlib.sha256(str(REPO_ROOT.resolve()).encode()).hexdigest()[:16]
    return RECEIPT_DIR / f"research-map-{key}.ok"


def tool_input_dict(raw: Dict[str, Any]) -> Dict[str, Any]:
    value = raw.get("tool_input")
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            return {}
    return value if isinstance(value, dict) else {}


def paths_from_payload(raw: Dict[str, Any]) -> List[str]:
    tool_input = tool_input_dict(raw)
    out: List[str] = []
    for key in PATH_KEYS:
        value = tool_input.get(key) or raw.get(key)
        if isinstance(value, str) and value.strip():
            out.append(value.strip().replace("\\", "/"))
    return out


def repo_relative(path: str) -> str:
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT.resolve())).replace(
            "\\", "/"
        )
    except Exception:
        return path.replace("\\", "/").lstrip("./")


def is_research_map(path: str) -> bool:
    norm = path.replace("\\", "/")
    return norm.endswith(MAP_REL)
