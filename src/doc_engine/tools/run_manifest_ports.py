"""Hexagonal ports for run_manifest persistence and lifecycle."""

from __future__ import annotations

from typing import Any, Protocol


class RunManifestStore(Protocol):
    """Port: load and atomically persist a run_manifest JSON document."""

    def load(self, path: str) -> dict:
        ...

    def write(self, path: str, data: dict) -> None:
        ...


class RunManifestLifecycle(Protocol):
    """Port: init / start-stage / end-stage / finalize mutations."""

    def build_init_manifest(self, repo_path: str, now_ms: int | None = None) -> dict:
        ...

    def start_stage(
        self,
        manifest: dict,
        name: str,
        fanout: int | None = None,
        now_ms: int | None = None,
    ) -> dict:
        ...

    def end_stage(
        self,
        manifest: dict,
        name: str,
        status: str,
        error: str | None = None,
        now_ms: int | None = None,
    ) -> dict:
        ...

    def finalize_manifest(self, manifest: dict, *args: Any, **kwargs: Any) -> tuple:
        ...


def default_manifest_store() -> RunManifestStore:
    """Filesystem adapter using façade atomic write + core jsonio load."""
    from doc_engine.core.jsonio import load_json
    from doc_engine.tools import run_manifest as rm

    class _FsStore:
        def load(self, path: str) -> dict:
            return load_json(path)

        def write(self, path: str, data: dict) -> None:
            rm._write_json_atomic(path, data)

    return _FsStore()
