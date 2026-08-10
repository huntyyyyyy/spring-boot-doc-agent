"""E-COH1: public-surface fitness fails closed on private ``__all__`` / residual bins."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from doc_engine.ci import public_surface_policy as policy

REPO = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.domain_ci_meta


def test_curated_modules_export_no_private_all_names() -> None:
    for module_name in policy.PUBLIC_ONLY_MODULES:
        privates = policy.module_private_all_exports(module_name)
        assert privates == [], f"{module_name} still exports {privates!r}"


def test_support_and_inventory_drift_absent() -> None:
    assert policy.forbidden_residual_paths(REPO) == []
    phases = REPO / "src/doc_engine/pipeline/local_runner_phases"
    assert not (phases / "support.py").exists()
    assert not (phases / "inventory_drift.py").exists()


def test_check_public_surface_script_exits_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts/ci/check_public_surface.py")],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_module_private_all_exports_detects_underscore(monkeypatch) -> None:
    fake = SimpleNamespace(__all__=["Log", "_secret"])
    monkeypatch.setattr(importlib, "import_module", lambda _n: fake)
    assert policy.module_private_all_exports("fake.mod") == ["_secret"]


def test_forbidden_residual_paths_finds_support(tmp_path: Path) -> None:
    root = tmp_path / "src/doc_engine/pipeline/local_runner_phases"
    root.mkdir(parents=True)
    (root / "support.py").write_text("# residual\n", encoding="utf-8")
    hits = policy.forbidden_residual_paths(tmp_path)
    assert hits == ["src/doc_engine/pipeline/local_runner_phases/support.py"]
