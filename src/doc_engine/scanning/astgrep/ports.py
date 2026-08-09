"""Hexagonal port for running one ast-grep argv (no DI container)."""

from __future__ import annotations

import subprocess
from typing import List, Protocol, runtime_checkable


@runtime_checkable
class AstGrepRunner(Protocol):
    """Port: execute one ast-grep command line and return a CompletedProcess."""

    def run(self, argv: List[str]) -> subprocess.CompletedProcess[str]:
        ...


class SubprocessAstGrepRunner:
    """Default adapter: ``subprocess.run`` with fail-closed text capture."""

    def run(self, argv: List[str]) -> subprocess.CompletedProcess[str]:
        from doc_engine.scanning import _scanner_astgrep as facade

        return facade.subprocess.run(
            argv,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )


DEFAULT_RUNNER: AstGrepRunner = SubprocessAstGrepRunner()
