"""Local pre_pr telemetry store — extract suite logs under ``.git/``.

Owns run directory layout and index.json transform. Never touches Cover% SoT.
"""

from __future__ import annotations

import json
import re
import sys
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Iterator, TextIO


def telemetry_root(repo: Path) -> Path:
    return repo / ".git" / "pre-pr-telemetry"


@dataclass
class SuiteTelemetry:
    name: str
    kind: str
    status: str
    exit_code: int
    duration_ms: int
    log_relpath: str
    error_excerpt: str = ""


@dataclass
class TelemetryIndex:
    schema_version: int = 1
    git_sha: str = ""
    mode: str = ""
    started_at: str = ""
    suites: list[SuiteTelemetry] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "git_sha": self.git_sha,
            "mode": self.mode,
            "started_at": self.started_at,
            "suites": [asdict(s) for s in self.suites],
        }


class TelemetryRun:
    """Active extract session for one pre_pr invocation."""

    def __init__(self, repo: Path, git_sha: str, mode: str) -> None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        short = (git_sha or "unknown")[:12]
        self.dir = telemetry_root(repo) / f"{short}-{mode}-{stamp}"
        self.suites_dir = self.dir / "suites"
        self.index = TelemetryIndex(
            git_sha=git_sha,
            mode=mode,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self.suites_dir.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        *,
        name: str,
        kind: str,
        status: str,
        exit_code: int,
        duration_ms: int,
        body: str,
    ) -> None:
        safe = re.sub(r"[^\w.-]+", "_", name)
        log_path = self.suites_dir / f"{safe}.log"
        log_path.write_text(body, encoding="utf-8")
        excerpt = _error_excerpt(body, exit_code)
        rel = str(log_path.relative_to(self.dir))
        self.index.suites.append(
            SuiteTelemetry(
                name=name,
                kind=kind,
                status=status,
                exit_code=exit_code,
                duration_ms=duration_ms,
                log_relpath=rel,
                error_excerpt=excerpt,
            )
        )

    def flush(self) -> Path:
        path = self.dir / "index.json"
        path.write_text(
            json.dumps(self.index.as_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        root = self.dir.parent
        latest = root / "latest"
        try:
            if latest.is_symlink() or latest.exists():
                latest.unlink()
            latest.symlink_to(self.dir.name, target_is_directory=True)
        except OSError:
            latest.write_text(self.dir.name + "\n", encoding="utf-8")
        return path


def _is_error_line(line: str) -> bool:
    lowered = line.lower()
    return "error" in lowered or "traceback" in line


def _error_excerpt(body: str, exit_code: int) -> str:
    if exit_code == 0 or not body.strip():
        return ""
    lines = body.strip().splitlines()
    for idx, line in enumerate(lines):
        if _is_error_line(line):
            return "\n".join(lines[idx : idx + 12])[:1200]
    return "\n".join(lines[-20:])[:1200]


class _Tee(StringIO):
    def __init__(self, primary: TextIO) -> None:
        super().__init__()
        self._primary = primary

    def write(self, s: str) -> int:  # type: ignore[override]
        self._primary.write(s)
        return super().write(s)

    def flush(self) -> None:
        self._primary.flush()
        super().flush()


def _append_tee_buffers(combined: StringIO, out_buf: _Tee, err_buf: _Tee) -> None:
    combined.write(out_buf.getvalue())
    err_text = err_buf.getvalue()
    if not err_text:
        return
    if combined.getvalue():
        combined.write("\n")
    combined.write(err_text)


@contextmanager
def tee_stdio() -> Iterator[StringIO]:
    """Tee stdout/stderr to a buffer while still printing live."""
    out_buf = _Tee(sys.stdout)
    err_buf = _Tee(sys.stderr)
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out_buf, err_buf
    combined = StringIO()
    try:
        yield combined
    finally:
        sys.stdout, sys.stderr = old_out, old_err
        _append_tee_buffers(combined, out_buf, err_buf)


def _index_from_symlink(root: Path, latest: Path) -> Path | None:
    target = (root / latest.readlink()).resolve()
    idx = target / "index.json"
    return idx if idx.is_file() else None


def _index_from_pointer_file(root: Path, latest: Path) -> Path | None:
    name = latest.read_text(encoding="utf-8").strip()
    idx = root / name / "index.json"
    return idx if idx.is_file() else None


def latest_index(repo: Path) -> Path | None:
    root = telemetry_root(repo)
    latest = root / "latest"
    if latest.is_symlink():
        return _index_from_symlink(root, latest)
    if latest.is_file():
        return _index_from_pointer_file(root, latest)
    return None
