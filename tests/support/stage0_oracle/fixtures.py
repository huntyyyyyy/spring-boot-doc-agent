"""Cohesive suite from tests/doc_engine/test_stage0_oracle_compare.py: OracleFixture, skip_if_no_astgrep."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
import stage0_oracle_compare as oracle

class OracleFixture:
    """Manages a minimal but realistic Java fixture + oracle.json for testing."""

    def __init__(self, tmp_dir: Path):
        self.root = tmp_dir
        self.source_root = tmp_dir / "src" / "main" / "java" / "com" / "example"
        self.source_root.mkdir(parents=True)
        self.salt = b"test_salt_16_bytes_" + b"x" * 31  # 48 bytes total

        # Create .pseudonym-salt in the repo root (oracle.load_salt looks here)
        (tmp_dir / ".pseudonym-salt").write_bytes(self.salt)

    def pseudonym(self, fqcn: str) -> str:
        return oracle.pseudonym(self.salt, "iface", fqcn)

    def write_java_file(self, class_name: str, content: str):
        """Write a Java file to src/main/java hierarchy."""
        path = self.source_root / f"{class_name}.java"
        path.write_text(content)
        return path

    def write_oracle_json(self, rows: List[dict]) -> Path:
        """Write oracle.json to the fixture root."""
        oracle_path = self.root / "oracle.json"
        oracle_path.write_text(json.dumps({"entities": rows}, indent=2))
        return oracle_path

    def oracle_row(self, fqcn: str, via_intermediate: bool = False,
                   matches_scan_list: bool = True) -> dict:
        """Create a properly-shaped oracle row for testing."""
        return {
            "entity_pseudonym": self.pseudonym(fqcn),
            "via_intermediate_only": via_intermediate,
            "matches_signal_scan_name_list": matches_scan_list,
        }


def skip_if_no_astgrep(test_case):
    """Decorator to skip tests if ast-grep is not available."""
    if not shutil.which("ast-grep"):
        return unittest.skip("ast-grep not found in PATH")(test_case)
    return test_case
