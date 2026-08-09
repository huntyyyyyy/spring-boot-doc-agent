"""Portable resolution of quality-gate CLIs (Python + jscpd).

Prefer ``sys.executable -m …`` for Python tools and a local ``node_modules``
jscpd install (native binary or ``run-jscpd.js``) over ``npx`` / shell wrappers.
Never use ``shell=True``.

``REPO_ROOT`` is the *git checkout* being gated (via ``git rev-parse``), not
``doc_engine.paths.repo_root()`` which follows the editable-install source tree
and can point at a different worktree.
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

JSCPD_VERSION = "5.0.14"

# Git rev-parse / diff range left-hand side from CLI (argv list, never shell).
# Allows HEAD~N, origin/main, abbreviated SHAs, and @{upstream}-style specs.
_GIT_REV_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/\-~^@{}]*$")

# (platform.system(), arch_token) → optional native package names under node_modules.
_JSCPD_NATIVE_PACKAGES: dict[tuple[str, str], tuple[str, ...]] = {
    ("Windows", "x64"): ("jscpd-windows-x64-msvc",),
    ("Darwin", "arm64"): ("jscpd-darwin-arm64",),
    ("Darwin", "x64"): ("jscpd-darwin-x64",),
    ("Linux", "x64"): ("jscpd-linux-x64-gnu", "jscpd-linux-x64-musl"),
    ("Linux", "arm64"): ("jscpd-linux-arm64-gnu",),
}


def _git_show_toplevel(cwd: Path) -> Path | None:
    completed = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    top = completed.stdout.strip()
    return Path(top) if top else None


def _pyproject_doc_engine_root(cwd: Path) -> Path | None:
    for candidate in (cwd, *cwd.parents):
        has_pyproject = (candidate / "pyproject.toml").is_file()
        has_package = (candidate / "src" / "doc_engine").is_dir()
        if has_pyproject and has_package:
            return candidate
    return None


def checkout_root(start: Path | None = None) -> Path:
    """Return the git worktree / repo root for the tree under *start* (or cwd).

    Quality gates must bind to the checkout the operator is in, not the path of
    the installed ``doc_engine`` sources (editable installs + worktrees diverge).
    """
    cwd = (start or Path.cwd()).resolve()
    from_git = _git_show_toplevel(cwd)
    if from_git is not None:
        return from_git
    from_markers = _pyproject_doc_engine_root(cwd)
    if from_markers is not None:
        return from_markers
    return cwd


# Mutable so tests can patch; refreshed at import from the invoking checkout.
REPO_ROOT = checkout_root()


def validate_git_rev(ref: str) -> str:
    """Reject option-like or metacharacter-laden git revisions from CLI."""
    if not ref or ref.startswith("-") or not _GIT_REV_RE.fullmatch(ref):
        print(f"error: unsafe git revision: {ref!r}", file=sys.stderr)
        raise SystemExit(2)
    return ref


def checked_path_under_repo(path: Path) -> Path:
    """Resolve *path* and require it stay inside this checkout's REPO_ROOT."""
    if ".." in Path(path).parts:
        print(f"error: path must not contain '..': {path}", file=sys.stderr)
        raise SystemExit(2)
    try:
        resolved = path.resolve()
        root = REPO_ROOT.resolve()
    except OSError as exc:
        print(f"error: cannot resolve path {path}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    try:
        resolved.relative_to(root)
    except ValueError:
        print(
            f"error: path escapes repository root {root}: {resolved}",
            file=sys.stderr,
        )
        raise SystemExit(2) from None
    return resolved


def _executable_name_aliases(name: str) -> list[str]:
    names = [name]
    if os.name == "nt":
        names.extend((f"{name}.exe", f"{name}.cmd", f"{name}.bat"))
    return names


def _first_existing_executable(base: Path, names: list[str]) -> str | None:
    for candidate_name in names:
        candidate = base / candidate_name
        if candidate.is_file():
            return str(candidate)
    return None


def _find_next_to_interpreter(name: str) -> str | None:
    sibling_dir = Path(sys.executable).resolve().parent
    names = _executable_name_aliases(name)
    for base in (sibling_dir, sibling_dir / "Scripts"):
        found = _first_existing_executable(base, names)
        if found is not None:
            return found
    return None


def require_on_path(name: str) -> str:
    """Return an absolute executable path for *name*, or exit 2."""
    resolved = shutil.which(name)
    if resolved:
        return resolved
    sibling = _find_next_to_interpreter(name)
    if sibling:
        return sibling
    print(
        f"error: {name!r} is not on PATH (install requirements-dev.txt / Node)",
        file=sys.stderr,
    )
    raise SystemExit(2)


def python_module_command(module: str, *args: str) -> list[str]:
    """Build ``[sys.executable, '-m', module, …]`` — OS-native argv list."""
    return [sys.executable, "-m", module, *args]


def require_venv_script(name: str) -> str:
    """Resolve a pip console_script next to the active interpreter."""
    return require_on_path(name)


def _arch_token() -> str:
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return "x64"
    if machine in ("aarch64", "arm64"):
        return "arm64"
    return machine


def _jscpd_native_binary_name(system: str) -> str:
    return "jscpd.exe" if system == "Windows" else "jscpd"


def _jscpd_native_candidates() -> list[Path]:
    """Platform optional-dependency binaries shipped with jscpd@5."""
    arch = _arch_token()
    system = platform.system()
    root = REPO_ROOT / "node_modules"
    binary = _jscpd_native_binary_name(system)
    packages = _JSCPD_NATIVE_PACKAGES.get((system, arch), ())
    return [root / pkg / "bin" / binary for pkg in packages]


def jscpd_command(*args: str) -> list[str]:
    """Argv to run pinned local jscpd (no npx)."""
    for candidate in _jscpd_native_candidates():
        if candidate.is_file():
            return [str(candidate), *args]

    wrapper = REPO_ROOT / "node_modules" / "jscpd" / "run-jscpd.js"
    if wrapper.is_file():
        node = require_on_path("node")
        return [node, str(wrapper), *args]

    print(
        "error: jscpd is not installed locally.\n"
        f"  Run once from the repo root (Mac/Windows/Linux): npm ci\n"
        f"  Expected pin: jscpd@{JSCPD_VERSION} (see package.json).",
        file=sys.stderr,
    )
    raise SystemExit(2)
