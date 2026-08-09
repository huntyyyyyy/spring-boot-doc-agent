"""Cohesive suite from tests/ci/test_run_manifest.py: _fake_completed, validate_manifest_shape."""

from __future__ import annotations

import json
import os
import subprocess
import sys

from doc_engine.tools import run_manifest
from tests.conftest import SCRIPTS_DIR

SCRIPT_DIR = SCRIPTS_DIR
RUN_MANIFEST_CMD = [sys.executable, "-m", "doc_engine.tools.run_manifest"]
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "schemas", "run_manifest.schema.json")
with open(SCHEMA_PATH, encoding="utf-8") as _f:
    _SCHEMA = json.load(_f)


def _fake_completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=["git"], returncode=returncode, stdout=stdout, stderr=stderr,
    )


def _missing_top_level_keys(data):
    required_top = set(_SCHEMA["required"])
    missing = required_top - data.keys()
    if not missing:
        return []
    return [f"missing top-level keys: {sorted(missing)}"]


def _status_and_version_problems(data):
    problems = []
    if data["schema_version"] != 1:
        problems.append(f"schema_version {data['schema_version']!r} != 1")
    if data["status"] not in ("running", "complete", "failed", "partial"):
        problems.append(f"unrecognized top-level status {data['status']!r}")
    return problems


def _target_repo_key_problems(data):
    problems = []
    tr = data["target_repo"]
    required_target_repo = set(_SCHEMA["properties"]["target_repo"]["required"])
    for key in required_target_repo:
        if key not in tr:
            problems.append(f"target_repo missing key {key!r}")
    return problems


def _top_level_manifest_problems(data):
    """Return (problems, early_exit). early_exit when required keys are missing."""
    missing = _missing_top_level_keys(data)
    if missing:
        return missing, True
    problems = _status_and_version_problems(data)
    problems.extend(_target_repo_key_problems(data))
    return problems, False


def _stage_manifest_problems(data, problems):
    required_stage = set(_SCHEMA["properties"]["stages"]["items"]["required"])
    for i, stage in enumerate(data["stages"]):
        stage_missing = required_stage - stage.keys()
        if stage_missing:
            problems.append(f"stage[{i}] missing keys: {sorted(stage_missing)}")
            continue
        if stage["status"] not in run_manifest.STAGE_STATUSES:
            problems.append(f"stage[{i}] unrecognized status {stage['status']!r}")
    return problems


def validate_manifest_shape(data):
    """Structural check against run_manifest.schema.json's documented shape —
    the equivalent of tests/doc_engine/test_pipeline_stages.py's own structural validators,
    deliberately not a jsonschema-library-enforced check (no new dependency).
    Required-key sets are read from the schema file itself (via _SCHEMA)
    rather than restated here, so the two can't silently diverge. Returns a
    list of problem strings; empty means the shape is valid."""
    problems, early_exit = _top_level_manifest_problems(data)
    if early_exit:
        return problems
    return _stage_manifest_problems(data, problems)
