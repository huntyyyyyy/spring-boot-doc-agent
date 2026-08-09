"""Coverage climb B9: scanner_base repr, cert JSON-object, capacity path-val.

Q2 adequacy witness: mutmut_slice on _scanner_base, certification, capacity —
asserts bite backend repr, non-object cert, failures mismatch, __main__, and
inner PathValidationError on capacity main.
"""

from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.paths import PathValidationError
from doc_engine.scanning._scanner_base import ScannerBackend
from doc_engine.tools import capacity_preflight as cp
from doc_engine.tools import certification as cert

pytestmark = pytest.mark.domain_climb_sensor

class _TinyBackend(ScannerBackend):
    @property
    def name(self) -> str:
        return "tiny"

    def version_hash(self) -> str:
        return "0" * 16

    def scan(self, repo_path: str, **kwargs):
        return {}

def test_scanner_backend_repr() -> None:
    assert "tiny" in repr(_TinyBackend())

def test_load_certification_rejects_non_object(tmp_path: Path) -> None:
    path = tmp_path / "certification.json"
    path.write_text(json.dumps([1, 2]), encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        cert.load_certification(path)

def test_refold_mismatch_failures_list() -> None:
    refold = SimpleNamespace(certified=True, failures=["a"])
    err = cert._refold_mismatch_error(True, ["b"], refold)
    assert err is not None
    assert "failures list" in err

def test_certification_dunder_main(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["certification", "/no/such/cert.json"])
    with pytest.raises(SystemExit) as exc:
        runpy.run_path(cert.__file__, run_name="__main__")
    assert exc.value.code in (1, 2)

def test_capacity_inner_path_validation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        ["capacity_preflight", str(tmp_path)],
    )

    def boom(*_a, **_k):
        raise PathValidationError("bad nested path")

    monkeypatch.setattr(cp, "_run_stage0_preflight", boom)
    with pytest.raises(SystemExit) as exc:
        cp.main()
    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err
