"""Regression: mutation_driver entrypoint bootstrap (E-TEL / remote red).

Remote failed with ModuleNotFoundError: No module named 'tests' when running
``python3 tests/spring_signals/mutation_driver.py``. Local pre_pr treated that
as advisory and stayed green — this suite fails closed on that bug.

Entrypoint probes use ``--import-only`` (bootstrap + import). Full mutant kill
loops stay in CI / ``pre_pr``, not in these unit tests.
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
_IMPORT_ONLY = "--import-only"


def _run_import_only(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=repo_root(),
        capture_output=True,
        text=True,
        check=False,
    )


def _assert_import_probe(completed: subprocess.CompletedProcess[str]) -> None:
    combined = f"{completed.stdout}\n{completed.stderr}"
    assert "ModuleNotFoundError" not in combined, combined[-2000:]
    assert "No module named 'tests'" not in combined, combined[-2000:]
    assert completed.returncode == 0, combined[-2000:]
    assert "import-ok" in completed.stdout, combined[-2000:]


def test_mutation_driver_script_entrypoint_no_module_not_found() -> None:
    """Legacy script argv must bootstrap before ``from tests.spring_signals…``."""
    _assert_import_probe(
        _run_import_only([sys.executable, str(_CI_SCRIPT), _IMPORT_ONLY])
    )


def test_mutation_driver_module_entrypoint_imports() -> None:
    """CI SoT argv (``python -m …``) must import cleanly without the kill loop."""
    _assert_import_probe(
        _run_import_only([sys.executable, "-m", _MODULE, _IMPORT_ONLY])
    )


def test_workflow_and_pre_pr_prefer_module_entrypoint() -> None:
    """CI / pre_pr must use ``-m`` so script-path pollution is not the SoT."""
    root = repo_root()
    workflow = (root / ".github/workflows/python-gates.yml").read_text(encoding="utf-8")
    assert "-m tests.spring_signals.mutation_driver" in workflow
    import pre_pr

    names = {name: kind for name, kind, _ in pre_pr.build_suites("full")}
    assert "mutation_driver" in names or "mutation_driver_advisory" in names
    # Tool crashes must be hard — survivors remain ENFORCE=False → exit 0.
    key = "mutation_driver" if "mutation_driver" in names else "mutation_driver_advisory"
    assert names[key] == "hard", f"{key} must be hard so local fails before remote"
