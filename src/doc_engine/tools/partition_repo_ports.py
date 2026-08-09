"""Ports separating pure grouping from filesystem walk I/O."""

from __future__ import annotations

from typing import Any, Protocol


class RepoFileLister(Protocol):
    """Port: list files under a repo root for token estimation."""

    def dfs_file_list(self, *args: Any, **kwargs: Any) -> list:
        ...


class GroupBuilder(Protocol):
    """Port: pure grouping of (path, tokens) into overlapping groups."""

    def build_groups(self, *args: Any, **kwargs: Any) -> list:
        ...
