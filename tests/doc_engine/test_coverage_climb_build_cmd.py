"""Coverage climb: build_command allowlist + excludes gitignore load."""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.core import excludes
from doc_engine.scanning import build_command as bc


def test_validate_build_command_accepts_tools_and_wrappers() -> None:
    assert "gradlew" in bc.validate_build_command("./gradlew compileJava")
    assert "mvn" in bc.validate_build_command("mvn -q test")
    wrapped = bc.validate_build_command("bash ./gradlew compileJava")
    assert "gradlew" in wrapped.lower() or "bash" in wrapped.lower()


def test_validate_build_command_rejects_empty_meta_and_flags() -> None:
    with pytest.raises(bc.BuildCommandError, match="empty"):
        bc.validate_build_command("")
    with pytest.raises(bc.BuildCommandError, match="empty"):
        bc.validate_build_command(None)
    with pytest.raises(bc.BuildCommandError, match="metacharacters"):
        bc.validate_build_command("gradlew compileJava; rm -rf /")
    with pytest.raises(bc.BuildCommandError, match="not allowed"):
        bc.validate_build_command("gradlew --init-script evil.gradle")
    with pytest.raises(bc.BuildCommandError, match="known build tool"):
        bc.validate_build_command("python setup.py build")
    with pytest.raises(bc.BuildCommandError, match="followed by"):
        bc.validate_build_command("bash")
    with pytest.raises(bc.BuildCommandError, match="wrap a known"):
        bc.validate_build_command("bash python")


def test_flag_and_token_helpers() -> None:
    assert bc._token_basename(r"C:\tools\gradlew.bat") == "gradlew.bat"
    assert bc._flag_name("--settings=/tmp/s") == "--settings"
    assert bc._strip_outer_quotes("'x'") == "x"
    assert bc._strip_outer_quotes("plain") == "plain"
    bc._reject_dangerous_flags(["gradlew", "compileJava"])
    with pytest.raises(bc.BuildCommandError):
        bc._reject_dangerous_flags(["gradlew", "-I", "x.gradle"])


def test_load_gitignore_spec(tmp_path: Path) -> None:
    assert excludes.load_gitignore_spec(str(tmp_path)) is None
    (tmp_path / ".gitignore").write_text("*.class\nbuild/\n", encoding="utf-8")
    spec = excludes.load_gitignore_spec(str(tmp_path))
    assert spec is not None
    assert ".git" in excludes.DEFAULT_EXCLUDED_DIRS
