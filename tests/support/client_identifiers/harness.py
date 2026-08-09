"""Cohesive suite from tests/ci/test_check_no_client_identifiers.py: findings, run_main."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import check_no_client_identifiers as gate

def findings(payload: object) -> List[str]:
    result: List[str] = []
    gate._walk(payload, "", None, result)
    return result


def run_main(args: List[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = gate.main(args)
    return code, out.getvalue(), err.getvalue()
