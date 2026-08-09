"""Tee log for the local pipeline runner."""

from __future__ import annotations

import sys


def reconfigure_stdio_utf8() -> None:
    """Prefer UTF-8 on console streams so tag grammar em dashes do not crash."""
    for stream in (sys.stdout, sys.stderr):
        if not hasattr(stream, "reconfigure"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


class Log:
    """Tee to stdout and run.log.

    Everything this script prints goes to both, so the log file is a complete
    transcript rather than a summary — the user asked to see the logs, and a
    log that omits what scrolled past is worse than no log.
    """

    def __init__(self, path):
        self.path = path
        self.fh = open(path, "w", encoding="utf-8")
        # Console encoding on Windows is frequently cp1252, which cannot
        # represent the em dash the tag grammar requires. Replace on the
        # console rather than crash; the log file is UTF-8 and keeps it.
        reconfigure_stdio_utf8()

    def __call__(self, msg=""):
        text = str(msg)
        print(text)
        self.fh.write(text + "\n")
        self.fh.flush()

    def rule(self, title):
        self("")
        self("=" * 78)
        self(title)
        self("=" * 78)

    def close(self):
        self.fh.close()
