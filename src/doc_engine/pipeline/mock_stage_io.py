"""Filesystem helpers for mock generative stage artifacts."""

from __future__ import annotations

import os

from doc_engine.core.jsonio import dump_json, load_json


def _write_json(path, obj):
    # Mock fixtures historically used indent=1; keep wire bytes stable for diffs.
    dump_json(path, obj, indent=1)


def _write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text if text.endswith("\n") else text + "\n")


def _read_json(path):
    return load_json(path)


def find_existing_readme(repo_path):
    for name in ("README.md", "readme.md", "README.MD"):
        if os.path.isfile(os.path.join(repo_path, name)):
            return name
    return None
