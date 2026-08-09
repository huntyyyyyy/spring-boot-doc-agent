"""Coverage for scripts/ci/verify_tool_pins.py."""

from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest
import verify_tool_pins as pins

pytestmark = pytest.mark.domain_ci_meta


def test_pin_major_minor_reads_requirements(tmp_path: Path) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("ast-grep-cli~=0.45.0\nsemgrep~=1.171.0\n", encoding="utf-8")
    assert pins._pin_major_minor(req, "ast-grep-cli") == ("0", "45")
    assert pins._pin_major_minor(req, "semgrep") == ("1", "171")


def test_verify_one_mismatch_exits(tmp_path: Path) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("semgrep~=1.171.0\n", encoding="utf-8")
    with mock.patch.object(
        pins,
        "_resolved_major_minor",
        return_value=("1", "100", "1.100.0", "/usr/bin/semgrep"),
    ):
        with pytest.raises(SystemExit):
            pins.verify_one(req, "semgrep", "semgrep")


def test_main_missing_requirements(tmp_path: Path) -> None:
    assert pins.main(["--requirements", str(tmp_path / "missing.txt")]) == 2
