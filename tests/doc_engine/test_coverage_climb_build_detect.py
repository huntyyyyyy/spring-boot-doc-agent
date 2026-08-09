"""Coverage climb: build-command detect and CodeQL prepare."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping
from unittest.mock import MagicMock
import pytest
from doc_engine.core import excludes as excludes_mod
from doc_engine.core import timeouts as timeouts_mod
from doc_engine.pipeline.local_runner_phases import support as phase_support
from doc_engine.query import kinds as kinds_mod
from doc_engine.query.protocols import FreshnessPolicy, PacketProvider
from doc_engine.scanning import spring as spring_mod
from doc_engine.scanning._scanner_codeql import CodeQLBackend
from doc_engine.scanning.support import _codeql_runner as runner
import doc_engine.scanning.support._codeql_cache as cache_mod
import doc_engine.scanning.support._codeql_cli as cli_mod
import doc_engine.scanning.support._codeql_database as db_mod
import doc_engine.scanning.support._codeql_queries as queries_mod

pytestmark = pytest.mark.domain_climb_sensor

def test_detect_build_command_prefers_gradlew(tmp_path: Path) -> None:
    (tmp_path / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "gradlew" in cmd
    assert "compileJava" in cmd

def test_detect_build_command_maven_wrapper(tmp_path: Path) -> None:
    (tmp_path / "mvnw").write_text("#!/bin/sh\n", encoding="utf-8")
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "mvnw" in cmd

def test_detect_build_command_gradle_on_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "build.gradle").write_text("plugins {}\n", encoding="utf-8")
    monkeypatch.setattr(spring_mod.shutil, "which", lambda name: f"/bin/{name}" if name == "gradle" else None)
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "gradle" in cmd

def test_detect_build_command_maven_on_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "pom.xml").write_text("<project/>\n", encoding="utf-8")
    monkeypatch.setattr(spring_mod.shutil, "which", lambda name: f"/bin/{name}" if name == "mvn" else None)
    cmd = spring_mod.detect_build_command(str(tmp_path))
    assert cmd is not None
    assert "mvn" in cmd

def test_detect_build_command_returns_none_without_markers(tmp_path: Path) -> None:
    assert spring_mod.detect_build_command(str(tmp_path)) is None

def test_prepare_codeql_build_skips_when_codeql_absent(tmp_path: Path) -> None:
    assert (
        spring_mod._prepare_codeql_build_command(["filesystem"], str(tmp_path), "gradlew build")
        == "gradlew build"
    )

def test_prepare_codeql_build_detects_or_raises(tmp_path: Path) -> None:
    with pytest.raises(spring_mod.CodeQLScannerError, match="Could not detect"):
        spring_mod._prepare_codeql_build_command(["codeql"], str(tmp_path), None)
    (tmp_path / "gradlew").write_text("x", encoding="utf-8")
    cmd = spring_mod._prepare_codeql_build_command(["codeql"], str(tmp_path), None)
    assert "gradlew" in cmd

def test_prepare_codeql_build_wraps_validation_error(tmp_path: Path) -> None:
    with pytest.raises(spring_mod.CodeQLScannerError):
        spring_mod._prepare_codeql_build_command(
            ["codeql"], str(tmp_path), "bash -c 'evil'"
        )
