"""Append markdown to a GitHub Actions step-summary file.

Validates the output path before I/O (Sonar S2083 / CLI-tainted paths) and
appends without read-modify-write of prior file contents.
"""

from __future__ import annotations

import sys
from pathlib import Path

from doc_engine.paths import PathValidationError, checked_output_path


def append_markdown(markdown: str, summary_path: str | Path) -> None:
    """Append *markdown* to *summary_path*, inserting a leading newline if needed."""
    path = checked_output_path(summary_path)
    needs_leading_newline = False
    if path.is_file() and path.stat().st_size > 0:
        with path.open("rb") as handle:
            handle.seek(-1, 2)
            needs_leading_newline = handle.read(1) != b"\n"
    with path.open("a", encoding="utf-8") as handle:
        if needs_leading_newline:
            handle.write("\n")
        handle.write(markdown)


def append_markdown_cli(
    markdown: str, summary_path: str | Path, *, ok_message: str
) -> int:
    """CLI-facing append: validate path, print status, return process exit code."""
    try:
        append_markdown(markdown, summary_path)
    except PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(ok_message)
    return 0
