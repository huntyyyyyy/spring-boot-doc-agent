#!/usr/bin/env python3
"""Optional local SonarQube advisory scan (never merge SoT).

Usage:
    python3 scripts/ci/sonar_local_advisory.py

When ``SONAR_HOST_URL`` and ``SONAR_TOKEN`` are set and ``docker`` is on PATH,
runs ``sonarsource/sonar-scanner-cli`` against this repo. Otherwise prints a
skip reason and exits 0 (advisory). See scripts/ci/sonar-local/README.md.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    host = (os.environ.get("SONAR_HOST_URL") or "").strip()
    token = (os.environ.get("SONAR_TOKEN") or "").strip()
    if not host or not token:
        print(
            "sonar_local_advisory: skip "
            "(set SONAR_HOST_URL + SONAR_TOKEN; see scripts/ci/sonar-local/)"
        )
        return 0
    if shutil.which("docker") is None:
        print("sonar_local_advisory: skip (docker not on PATH)")
        return 0
    root = Path(__file__).resolve().parents[2]
    cmd = [
        "docker",
        "run",
        "--rm",
        "--network",
        "host",
        "-e",
        f"SONAR_HOST_URL={host}",
        "-e",
        f"SONAR_TOKEN={token}",
        "-v",
        f"{root}:/usr/src",
        "sonarsource/sonar-scanner-cli",
    ]
    print("sonar_local_advisory: running scanner (advisory; not fail_under SoT)")
    completed = subprocess.run(cmd, cwd=root, check=False)
    # Advisory: never fail the pre_pr gate on scanner exit.
    if completed.returncode != 0:
        print(
            f"sonar_local_advisory: scanner exit={completed.returncode} "
            "(recorded advisory only)",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
