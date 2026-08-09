"""In-process ``python -m doc_engine.tools.*`` invoke for kitchen-sink.

Each kitchen ``run_chain`` step used to ``subprocess`` a fresh interpreter.
Cold-import of ``doc_engine`` (historically Engine → scanning → sqllineage)
dominated wall time (~0.65s × 22 steps). Calling tool ``main()`` in-process
keeps the same argv/exit-code contract while paying the import once.
"""

from __future__ import annotations

import importlib
import io
import os
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from typing import Callable, Optional, Sequence


def _module_from_python_m_argv(argv: Sequence[str]) -> tuple[str, list[str]] | None:
    """Return ``(module, rest_argv)`` when argv is ``[python, -m, module, ...]``."""
    if len(argv) < 3 or argv[1] != "-m":
        return None
    return str(argv[2]), [str(x) for x in argv[3:]]


def _subprocess_run(argv: Sequence[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(argv),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        **kwargs,
    )


def _system_exit_code(exc: SystemExit) -> int:
    if exc.code is None:
        return 0
    if isinstance(exc.code, int):
        return exc.code
    return 1


def _invoke_main(main: Callable, module_name: str, rest: list[str], cwd: Optional[str]) -> tuple[int, str, str]:
    """Call ``main()`` with redirected stdio; return ``(code, stdout, stderr)``."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    old_argv = sys.argv
    old_cwd = os.getcwd()
    code = 0
    try:
        if cwd:
            os.chdir(cwd)
        sys.argv = [module_name, *rest]
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            result = main()
        if isinstance(result, int):
            code = result
    except SystemExit as exc:
        code = _system_exit_code(exc)
    finally:
        sys.argv = old_argv
        if cwd:
            os.chdir(old_cwd)
    return code, stdout_buf.getvalue(), stderr_buf.getvalue()


def _doc_engine_main(argv: Sequence[str]) -> Optional[tuple[str, list[str], Callable]]:
    parsed = _module_from_python_m_argv(argv)
    if parsed is None or not parsed[0].startswith("doc_engine."):
        return None
    module_name, rest = parsed
    main = getattr(importlib.import_module(module_name), "main", None)
    if main is None:
        return None
    return module_name, rest, main


def run_argv(argv: Sequence[str], **subprocess_kwargs) -> subprocess.CompletedProcess:
    """Run a tool argv in-process when it is ``python -m doc_engine…``; else subprocess.

    ``subprocess_kwargs`` match ``subprocess.run`` (cwd/env/…). Capture is always
    on for the in-process path so kitchen assertions can read stdout/stderr.
    """
    resolved = _doc_engine_main(argv)
    if resolved is None:
        return _subprocess_run(argv, **subprocess_kwargs)
    module_name, rest, main = resolved
    code, stdout, stderr = _invoke_main(
        main, module_name, rest, subprocess_kwargs.get("cwd"),
    )
    return subprocess.CompletedProcess(
        args=list(argv), returncode=code, stdout=stdout, stderr=stderr,
    )
