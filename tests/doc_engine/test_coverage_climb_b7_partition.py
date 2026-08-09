"""Coverage climb B7: partition_repo decode/read/classify/main edges.

Q2 adequacy witness: mutmut_slice on doc_engine.tools.partition_repo — asserts
bite latin-1 decode, read OSError, exclude/gitignore filters, odd dir entries,
zero-progress carry clear, and main PathValidationError exit.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from doc_engine.tools import partition_repo as pr

pytestmark = pytest.mark.domain_climb_sensor


def test_decode_file_bytes_latin1_and_undecodable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    text, reason = pr._decode_file_bytes(b"caf\xe9")
    assert reason is None
    assert "caf" in text
    assert pr._decode_file_bytes(b"\x00" + b"x" * 100)[1] == "binary"

    class BadChunk(bytes):
        def decode(self, encoding: str = "utf-8", errors: str = "strict") -> str:
            if encoding == "utf-8":
                raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad")
            raise RuntimeError("latin-1 also fails")

    out, err = pr._decode_file_bytes(BadChunk(b"\xff\xfe"))
    assert out is None
    assert err == "undecodable"


def test_read_file_bytes_oserror(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "f.bin"
    target.write_bytes(b"abc")

    def boom(*_a: object, **_k: object):
        raise OSError("io")

    monkeypatch.setattr("builtins.open", boom)
    data, err = pr._read_file_bytes(str(target), 10)
    assert data is None
    assert err == "read-failed"


def test_estimate_tokens_stat_failed(tmp_path: Path) -> None:
    tokens, reason = pr.estimate_tokens(str(tmp_path / "missing"), 1000)
    assert tokens == 0
    assert reason == "stat-failed"


def test_should_include_file_excludes_and_gitignore(tmp_path: Path) -> None:
    root = str(tmp_path)
    repo = str(tmp_path)
    assert (
        pr._should_include_file(
            "secret.key",
            str(tmp_path / "secret.key"),
            repo,
            root,
            {"secret.key"},
            {".class"},
            None,
            lambda *_a: True,
        )
        is False
    )
    assert (
        pr._should_include_file(
            "A.class",
            str(tmp_path / "A.class"),
            repo,
            root,
            set(),
            {".class"},
            None,
            lambda *_a: True,
        )
        is False
    )

    class Spec:
        def match_file(self, rel: str) -> bool:
            return rel.endswith("ignored.java")

    assert (
        pr._should_include_file(
            "ignored.java",
            str(tmp_path / "ignored.java"),
            repo,
            root,
            set(),
            set(),
            Spec(),
            lambda *_a: True,
        )
        is False
    )


def test_classify_and_partition_dir_entries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = tmp_path / "sub"
    d.mkdir()
    f = tmp_path / "f.txt"
    f.write_text("x", encoding="utf-8")
    assert pr._classify_dir_entry("sub", str(d)) == "directory"
    assert pr._classify_dir_entry("f.txt", str(f)) == "file"

    def neither(path: str) -> bool:
        return False

    monkeypatch.setattr(os.path, "isdir", lambda p: False)
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(os.path, "islink", lambda p: False)
    assert pr._classify_dir_entry("odd", str(tmp_path / "odd")) is None

    monkeypatch.setattr(os, "listdir", lambda _p: (_ for _ in ()).throw(OSError("x")))
    assert pr._partition_dir_entries(str(tmp_path)) == ([], [])


def test_guard_zero_progress_carry_clears() -> None:
    carry, carried = pr._guard_zero_progress_carry(
        ["a"],
        100,
        100,
        50,
        groups_closed_so_far=0,
        num_groups=3,
        max_tokens=120,
        target_per_group=50.0,
    )
    assert carry == []
    assert carried == 0


def test_main_path_validation_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["partition_repo", "/no/such/repo", "--out", "/tmp/out.json"],
    )
    with pytest.raises(SystemExit) as exc:
        pr.main()
    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err
