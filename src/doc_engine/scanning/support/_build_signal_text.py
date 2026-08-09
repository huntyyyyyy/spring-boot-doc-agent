"""Comment-strip and line helpers for build-script signal extraction."""

from __future__ import annotations

import re


def read_text_compat(text: str) -> str:
    """Return text with a single trailing newline; input may already have one."""
    return text.rstrip("\n") + "\n"


def strip_comments(text: str) -> str:
    """Remove Groovy/Kotlin block and line comments, preserving line numbers.

    Comments are replaced with spaces so line indices stay valid. This is
    intentionally simple: it does not handle nested block comments or string
    literals that happen to contain /*, but it is enough to avoid the common
    false-positive of a commented-out dependency becoming a signal.
    """
    # Block comments /* ... */ (non-greedy, may span lines)
    text = re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), text, flags=re.DOTALL)
    # Line comments // ... (to end of line, but not inside URLs like http://)
    lines = text.splitlines(keepends=True)
    out = []
    for line in lines:
        # Find // not preceded by :
        pos = line.find("//")
        if pos >= 0 and (pos == 0 or line[pos - 1] != ":"):
            line = line[:pos] + " " * (len(line) - pos)
        out.append(line)
    return "".join(out)


def line_number(text: str, pos: int) -> int:
    """1-based line number for character position pos in text."""
    return text.count("\n", 0, pos) + 1


def capture_line(text: str, match: re.Match) -> int:
    """Line number of the match start, using the original (unstripped) text."""
    return text.count("\n", 0, match.start()) + 1


def safe_match(text: str, line_no: int) -> str:
    """Return the line at line_no (1-based) from text, stripped."""
    lines = text.splitlines()
    if 1 <= line_no <= len(lines):
        return lines[line_no - 1].strip()[:200]
    return ""
