"""Cohesive suite from tests/doc_engine/test_spring_drift_check.py: _fixture_build_command, _make_scratch_copy, _edit, _by_source."""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import spring_drift_check, spring_signal_scan
SCRIPT_DIR = SCRIPTS_DIR
FIXTURE_JAVA_PREFIX = "src/main/java/com/example/billing/"
DRIFT_CHECK_CMD = [sys.executable, "-m", "doc_engine.tools.spring_drift_check"]
FAST_MODE = os.environ.get("SPRING_DRIFT_FAST_MODE", "").lower() in ("1", "true", "yes")

def _fixture_build_command():
    # Drift tests only exercise main-source citations, so compileTestJava is
    # omitted to keep the per-test CodeQL database creation as fast as possible.
    gradlew = os.path.join(FIXTURE_DIR, "gradlew.bat" if os.name == "nt" else "gradlew")
    return f"{gradlew} --no-daemon clean compileJava"


def _make_scratch_copy():
    scratch = tempfile.mkdtemp(prefix="drift_check_test_")
    dest = os.path.join(scratch, "repo")
    shutil.copytree(FIXTURE_DIR, dest)
    return dest


def _edit(path, old, new):
    with open(path) as f:
        text = f.read()
    assert old in text, f"expected to find {old!r} in {path}"
    text = text.replace(old, new)
    with open(path, "w") as f:
        f.write(text)


def _by_source(report, source_suffix):
    """First result entry whose `source` ends with the given suffix — lets
    tests address e.g. "entity_table_map.LegacyAudit" or a specific bucket
    entry without depending on list order."""
    for r in report["results"]:
        if r["source"].endswith(source_suffix):
            return r
    return None
