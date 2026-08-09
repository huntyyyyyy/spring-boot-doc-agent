#!/usr/bin/env python3
"""Adaptive token-bounded DFS file grouping façade.

Run with: python -m doc_engine.tools.partition_repo

Concept modules: ``partition_repo_constants``, ``_tokens``, ``_walk``,
``_groups``, ``_cli``, ``_ports``. Implements ArchAgent-style adaptive
grouping (arXiv:2601.13007 §3) with overlap for merge context.
"""

from __future__ import annotations

from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS
from doc_engine.tools.partition_repo_cli import (
    _collect_file_tokens,
    _groups_output_payload,
    main,
)
from doc_engine.tools.partition_repo_constants import (
    CHARS_PER_TOKEN_DEFAULT,
    CHARS_PER_TOKEN_DENSE,
    DEFAULT_EXCLUDED_EXTS,
    DEFAULT_EXCLUDED_FILES,
    DENSE_EXTS,
)
from doc_engine.tools.partition_repo_groups import (
    _carry_forward_overlap,
    _close_group_and_seed_next,
    _guard_zero_progress_carry,
    _should_close_group,
    _should_skip_carry_candidate,
    _step_group_assignment,
    build_groups,
)
from doc_engine.tools.partition_repo_ports import GroupBuilder, RepoFileLister
from doc_engine.tools.partition_repo_tokens import (
    _decode_file_bytes,
    _read_file_bytes,
    estimate_tokens,
    relpath_posix,
    to_posix,
)
from doc_engine.tools.partition_repo_walk import (
    _append_included_files,
    _classify_dir_entry,
    _collect_descendable_dirs,
    _partition_dir_entries,
    _relpath_under_repo,
    _should_descend_directory,
    _should_include_file,
    _walk_repo_collecting_files,
    dfs_file_list,
)

__all__ = [
    "CHARS_PER_TOKEN_DEFAULT",
    "CHARS_PER_TOKEN_DENSE",
    "DEFAULT_EXCLUDED_DIRS",
    "DEFAULT_EXCLUDED_EXTS",
    "DEFAULT_EXCLUDED_FILES",
    "DENSE_EXTS",
    "GroupBuilder",
    "RepoFileLister",
    "_append_included_files",
    "_carry_forward_overlap",
    "_classify_dir_entry",
    "_close_group_and_seed_next",
    "_collect_descendable_dirs",
    "_collect_file_tokens",
    "_decode_file_bytes",
    "_groups_output_payload",
    "_guard_zero_progress_carry",
    "_partition_dir_entries",
    "_read_file_bytes",
    "_relpath_under_repo",
    "_should_close_group",
    "_should_descend_directory",
    "_should_include_file",
    "_should_skip_carry_candidate",
    "_step_group_assignment",
    "_walk_repo_collecting_files",
    "build_groups",
    "dfs_file_list",
    "estimate_tokens",
    "main",
    "relpath_posix",
    "to_posix",
]

if __name__ == "__main__":
    raise SystemExit(main())
