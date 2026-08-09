"""Cohesive suite from tests/ci/test_run_manifest.py: _fake_completed, validate_manifest_shape."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
from doc_engine.tools import run_manifest, spring_signal_scan
SCRIPT_DIR = SCRIPTS_DIR
RUN_MANIFEST_CMD = [sys.executable, "-m", "doc_engine.tools.run_manifest"]
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "schemas", "run_manifest.schema.json")

with open(SCHEMA_PATH, encoding="utf-8") as _f:
    _SCHEMA = json.load(_f)


def _fake_completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(args=["git"], returncode=returncode, stdout=stdout, stderr=stderr)


def validate_manifest_shape(data):
    """Structural check against run_manifest.schema.json's documented shape —
    the equivalent of tests/doc_engine/test_pipeline_stages.py's own structural validators,
    deliberately not a jsonschema-library-enforced check (no new dependency).
    Required-key sets are read from the schema file itself (via _SCHEMA)
    rather than restated here, so the two can't silently diverge. Returns a
    list of problem strings; empty means the shape is valid."""
    problems = []
    required_top = set(_SCHEMA["required"])
    missing = required_top - data.keys()
    if missing:
        problems.append(f"missing top-level keys: {sorted(missing)}")
        return problems

    if data["schema_version"] != 1:
        problems.append(f"schema_version {data['schema_version']!r} != 1")
    if data["status"] not in ("running", "complete", "failed", "partial"):
        problems.append(f"unrecognized top-level status {data['status']!r}")

    tr = data["target_repo"]
    required_target_repo = set(_SCHEMA["properties"]["target_repo"]["required"])
    for key in required_target_repo:
        if key not in tr:
            problems.append(f"target_repo missing key {key!r}")

    required_stage = set(_SCHEMA["properties"]["stages"]["items"]["required"])
    for i, stage in enumerate(data["stages"]):
        stage_missing = required_stage - stage.keys()
        if stage_missing:
            problems.append(f"stage[{i}] missing keys: {sorted(stage_missing)}")
            continue
        if stage["status"] not in run_manifest.STAGE_STATUSES:
            problems.append(f"stage[{i}] unrecognized status {stage['status']!r}")

    return problems
