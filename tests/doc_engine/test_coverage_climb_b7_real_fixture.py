"""Coverage climb B7: real_fixture truthy / path-file / require edges.

Q2 adequacy witness: mutmut_slice on doc_engine.real_fixture — asserts bite
truthy live-scan, path-file OSError, require_real_repo dir checks, and legacy
live env (not padding).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine import real_fixture as rf

pytestmark = pytest.mark.domain_climb_sensor


def test_truthy_accepts_yes_and_true() -> None:
    assert rf._truthy("YES") is True
    assert rf._truthy("true") is True
    assert rf._truthy("1") is True
    assert rf._truthy("no") is False


def test_read_path_file_oserror(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path_file = tmp_path / "local-runs" / "real-repo.path"
    path_file.parent.mkdir(parents=True)
    path_file.write_text("/somewhere\n", encoding="utf-8")
    monkeypatch.setattr(rf, "repo_root", lambda: tmp_path)

    def boom(*_a: object, **_k: object) -> str:
        raise OSError("io")

    monkeypatch.setattr(Path, "read_text", boom)
    assert rf._read_path_file() is None


def test_require_real_repo_missing_and_not_dir(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv(rf.ENV_REAL_REPO, raising=False)
    for name in rf._LEGACY_REPO_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(rf, "_read_path_file", lambda: None)
    with pytest.raises(FileNotFoundError, match="unset"):
        rf.require_real_repo()

    missing = tmp_path / "nope"
    monkeypatch.setenv(rf.ENV_REAL_REPO, str(missing))
    with pytest.raises(FileNotFoundError, match="not a directory"):
        rf.require_real_repo()

    good = tmp_path / "repo"
    good.mkdir()
    monkeypatch.setenv(rf.ENV_REAL_REPO, str(good))
    assert rf.require_real_repo() == good


def test_live_scan_enabled_via_legacy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(rf.ENV_LIVE_SCAN, raising=False)
    for name in rf._LEGACY_LIVE_VARS:
        monkeypatch.delenv(name, raising=False)
    assert rf.live_scan_enabled() is False
    monkeypatch.setenv(rf._LEGACY_LIVE_VARS[0], "yes")
    assert rf.live_scan_enabled() is True
