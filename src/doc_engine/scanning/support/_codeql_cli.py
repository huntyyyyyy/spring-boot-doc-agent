"""CodeQL CLI adapter: discovery, allowlisted invoke, version parsing.

Port to the CodeQL binary — no scan orchestration or cache policy.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from doc_engine.core.timeouts import tool_timeout_seconds

class CodeQLError(RuntimeError):
    """Any CodeQL CLI failure that should not silently kill the process."""

class CodeQLNotFoundError(CodeQLError):
    """Raised when the CodeQL CLI cannot be found on PATH or DOC_ENGINE_CODEQL."""

def find_codeql() -> Path:
    """Return the CodeQL CLI executable path.

    Resolution order: ``DOC_ENGINE_CODEQL`` (if set to an existing file), then
    ``PATH``. No machine-local fallback paths are consulted.
    """
    env = os.environ.get("DOC_ENGINE_CODEQL")
    if env and str(env).strip():
        candidate = Path(env)
        if candidate.is_file():
            return candidate
        raise CodeQLNotFoundError(
            f"error: DOC_ENGINE_CODEQL={env!r} is not an existing file"
        )
    path = shutil.which("codeql")
    if path:
        return Path(path)
    raise CodeQLNotFoundError(
        "error: the 'codeql' binary is not on PATH. Install the CodeQL CLI "
        "(e.g. from https://github.com/github/codeql-cli-binaries/releases), "
        "add it to PATH, or set DOC_ENGINE_CODEQL to the executable."
    )

_CODEQL_SUBCOMMANDS: frozenset[tuple[str, ...]] = frozenset({
    ("--version",),
    ("database", "create"),
    ("pack", "install"),
    ("query", "run"),
    ("bqrs", "decode"),
})

def _resolve_codeql_exe(codeql_path: Path) -> Path:
    exe = Path(codeql_path).resolve()
    if not exe.is_file():
        raise CodeQLError(f"codeql executable is not a file: {exe}")
    return exe

def _reject_unsafe_option(opt: str) -> None:
    if not isinstance(opt, str) or not opt:
        raise CodeQLError("codeql option must be a non-empty string")
    if "\x00" in opt or "\n" in opt or "\r" in opt:
        raise CodeQLError("codeql option must be a single-line string without NUL")

def _invoke_codeql(
    codeql_path: Path,
    subcommand: tuple[str, ...],
    *options: str,
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    """Invoke one allowlisted CodeQL subcommand (never a free-form argv list).

    Executable comes only from ``codeql_path`` (resolved to a real file).
    ``subcommand`` must be a member of ``_CODEQL_SUBCOMMANDS``. Callers build
    options from typed paths / already-validated build commands — they cannot
    pick a different binary or invent a new verb.
    """
    if subcommand not in _CODEQL_SUBCOMMANDS:
        raise CodeQLError(
            f"refusing non-allowlisted codeql subcommand {subcommand!r}; "
            f"allowed: {sorted(_CODEQL_SUBCOMMANDS)}"
        )
    for opt in options:
        _reject_unsafe_option(opt)

    exe = _resolve_codeql_exe(codeql_path)
    argv = [str(exe), *subcommand, *options]
    try:
        return subprocess.run(
            argv,
            shell=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise CodeQLError(
            f"codeql timed out after {timeout}s: {' '.join(argv[:4])}…"
        ) from exc

def _version_token_from_line(line: str) -> Optional[str]:
    """Return a dotted version token from one ``codeql --version`` line, if any."""
    if "release" not in line:
        return None
    for part in line.split():
        if part and part[0].isdigit():
            return part.rstrip(".")
    return None

def _parse_codeql_version_stdout(stdout: str) -> str:
    """Parse ``codeql --version`` stdout into a dotted version string."""
    for line in stdout.splitlines():
        token = _version_token_from_line(line)
        if token is not None:
            return token
    raise CodeQLError(f"could not parse codeql version from: {stdout}")

def codeql_version(codeql_path: Path) -> str:
    """Return the CodeQL CLI version string, e.g. '2.26.0'."""
    proc = _invoke_codeql(
        codeql_path,
        ("--version",),
        timeout=tool_timeout_seconds(),
    )
    if proc.returncode != 0:
        raise CodeQLError(f"codeql --version failed: {proc.stderr}")
    return _parse_codeql_version_stdout(proc.stdout)

