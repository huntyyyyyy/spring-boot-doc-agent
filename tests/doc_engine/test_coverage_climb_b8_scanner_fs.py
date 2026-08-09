"""Coverage climb B8: filesystem scanner OSError / ScanContext edges.

Q2 adequacy witness: mutmut_slice on doc_engine.scanning._scanner_filesystem —
asserts bite config/build read OSError, version_hash OSError skip, and
ScanContext.build when scan_context omitted.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.scanning import _scanner_filesystem as sfs

pytestmark = pytest.mark.domain_climb_sensor


def test_process_config_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "application.yml"
    target.write_text("a: 1\n", encoding="utf-8")

    def boom(*_a, **_k):
        raise OSError("io")

    monkeypatch.setattr("builtins.open", boom)
    zones: dict = {}
    keys: dict = {}
    sfs._process_config_deployment_file(str(target), "application.yml", zones, keys)
    assert zones == {}
    assert keys == {}


def test_read_build_text_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "pom.xml"
    target.write_text("<project/>", encoding="utf-8")

    def boom(*_a, **_k):
        raise OSError("io")

    monkeypatch.setattr("builtins.open", boom)
    assert sfs._read_build_text(str(target), "pom.xml") == ""
    assert "could not read" in capsys.readouterr().err


def test_version_hash_skips_oserror(monkeypatch: pytest.MonkeyPatch) -> None:
    real_open = open

    def selective_open(path, *a, **k):
        if "support" in str(path):
            raise OSError("io")
        return real_open(path, *a, **k)

    monkeypatch.setattr("builtins.open", selective_open)
    digest = sfs.FilesystemBackend().version_hash()
    assert isinstance(digest, str)
    assert len(digest) == 16


def test_scan_builds_context_when_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    built = {"n": 0}

    class FakeCtx:
        file_signatures: dict = {}
        java_files: list = []
        non_java_files: list = []

        @classmethod
        def build(cls, repo_path: str, respect_gitignore: bool = False):
            built["n"] += 1
            return cls()

    monkeypatch.setattr(sfs, "ScanContext", FakeCtx)
    monkeypatch.setattr(
        sfs.FilesystemBackend,
        "version_hash",
        lambda self: "0" * 16,
    )
    out = sfs.FilesystemBackend().scan(str(tmp_path))
    assert built["n"] == 1
    assert "evidence" in out
    assert out["files_scanned"]["java"] == 0
