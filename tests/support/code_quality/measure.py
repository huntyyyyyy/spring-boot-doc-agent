"""Cohesive suite from tests/ci/test_check_code_quality.py: measure_one."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
SCRIPT_DIR = SCRIPTS_DIR
import check_code_quality as checker

def measure_one(source: str):
    """Measure a single synthetic module named mod.py."""
    return checker.measure_source(source, "mod.py")
