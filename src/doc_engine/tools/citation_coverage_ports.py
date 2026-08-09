"""Hexagonal port for citation-coverage report computation."""

from __future__ import annotations

from typing import Protocol


class CitationCoveragePort(Protocol):
    """Port: run untagged / miscased / weak-anchor checks over a docs dir."""

    def check_docs(
        self,
        docs_dir: str,
        target_repo: str | None,
        window: int = ...,
    ) -> dict:
        ...

    def total_findings(self, report: dict) -> int:
        ...
