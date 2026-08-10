"""Regression: mutation_driver must run the way CI invokes it (E-TEL / remote red).

Remote failed with ModuleNotFoundError: No module named 'tests' when running
``python3 tests/spring_signals/mutation_driver.py``. Local pre_pr treated that
as advisory and stayed green — this suite fails closed on that bug.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from doc_engine.paths import repo_root

pytestmark = pytest.mark.domain_ci_meta

_CI_SCRIPT = Path("tests/spring_signals/mutation_driver.py")
_MODULE = "tests.spring_signals.mutation_driver"


def test_mutation_driver_script_entrypoint_no_module_not_found() -> None:
    """Exact CI argv shape must not crash on ``from tests.spring_signals…``."""
    root = repo_root()
    completed = subprocess.run(
        [sys.executable, str(_CI_SCRIPT)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = f"{completed.stdout}\n{completed.stderr}"
    assert "ModuleNotFoundError" not in combined, combined[-2000:]
    assert "No module named 'tests'" not in combined, combined[-2000:]
    assert completed.returncode == 0, combined[-2000:]


def test_mutation_driver_module_entrypoint_exits_zero() -> None:
    root = repo_root()
    completed = subprocess.run(
        [sys.executable, "-m", _MODULE],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, f"{completed.stdout}\n{completed.stderr}"[-2000:]


def test_workflow_and_pre_pr_use_module_or_fixed_script() -> None:
    """CI must not keep the bare broken script-only pattern without a fix path."""
    root = repo_root()
    workflow = (root / ".github/workflows/python-gates.yml").read_text(encoding="utf-8")
    assert "mutation_driver" in workflow
    # Prefer -m; script form is OK only if the regression above stays green.
    uses_module = "-m tests.spring_signals.mutation_driver" in workflow
    uses_script = "tests/spring_signals/mutation_driver.py" in workflow
    assert uses_module or uses_script
    import pre_pr

    names = {name: kind for name, kind, _ in pre_pr.build_suites("full")}
    assert "mutation_driver" in names or "mutation_driver_advisory" in names
    # Tool crashes must be hard — survivors remain ENFORCE=False → exit 0.
    key = "mutation_driver" if "mutation_driver" in names else "mutation_driver_advisory"
    assert names[key] == "hard", f"{key} must be hard so local fails before remote"
