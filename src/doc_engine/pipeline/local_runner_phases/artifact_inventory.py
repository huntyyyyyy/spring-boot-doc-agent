"""Log artifact inventory under a local-runner output directory."""

from __future__ import annotations

import os


def artifact_inventory(log, out_dir) -> None:
    log.rule("ARTIFACT INVENTORY")
    for root, dirs, files in os.walk(out_dir):
        dirs.sort()
        for name in sorted(files):
            abspath = os.path.join(root, name)
            rel = os.path.relpath(abspath, out_dir).replace(os.sep, "/")
            log(f"  {os.path.getsize(abspath):>9,} B  {rel}")
