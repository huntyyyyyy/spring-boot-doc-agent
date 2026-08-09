"""DFS walk of a repo collecting files under exclude / gitignore rules."""

from __future__ import annotations

import os


def _relpath_under_repo(full_path: str, repo_path: str) -> str:
    return os.path.relpath(full_path, repo_path).replace("\\", "/")


def _should_descend_directory(
    name: str,
    full_path: str,
    repo_path: str,
    excluded_dirs,
    gitignore_spec,
) -> bool:
    if name in excluded_dirs or name.startswith("."):
        return False
    if gitignore_spec is None:
        return True
    return not gitignore_spec.match_file(_relpath_under_repo(full_path, repo_path) + "/")


def _should_include_file(
    name: str,
    full_path: str,
    repo_path: str,
    root: str,
    excluded_files,
    excluded_exts,
    gitignore_spec,
    is_path_inside_root,
) -> bool:
    if name in excluded_files:
        return False
    _, extension = os.path.splitext(name)
    if extension.lower() in excluded_exts:
        return False
    if gitignore_spec is not None and gitignore_spec.match_file(
        _relpath_under_repo(full_path, repo_path)
    ):
        return False
    return is_path_inside_root(full_path, root)


def _classify_dir_entry(name: str, full_path: str):
    """Return 'directory', 'file', or None for ignored entry kinds."""
    if os.path.isdir(full_path) and not os.path.islink(full_path):
        return "directory"
    if os.path.isfile(full_path) or os.path.islink(full_path):
        return "file"
    return None


def _partition_dir_entries(dir_path: str):
    """Split sorted directory entries into real dirs vs files/symlinks."""
    try:
        entries = sorted(os.listdir(dir_path))
    except OSError:
        return [], []
    directories, regular_files = [], []
    for name in entries:
        full_path = os.path.join(dir_path, name)
        kind = _classify_dir_entry(name, full_path)
        if kind == "directory":
            directories.append((name, full_path))
        elif kind == "file":
            regular_files.append((name, full_path))
    return directories, regular_files


def _collect_descendable_dirs(
    directories,
    repo_path: str,
    excluded_dirs,
    gitignore_spec,
):
    return [
        full_path
        for name, full_path in directories
        if _should_descend_directory(
            name, full_path, repo_path, excluded_dirs, gitignore_spec
        )
    ]


def _append_included_files(
    files: list,
    regular_files,
    *,
    repo_path: str,
    root: str,
    excluded_files,
    excluded_exts,
    gitignore_spec,
    is_path_inside_root,
) -> None:
    for name, full_path in regular_files:
        if _should_include_file(
            name,
            full_path,
            repo_path,
            root,
            excluded_files,
            excluded_exts,
            gitignore_spec,
            is_path_inside_root,
        ):
            files.append(full_path)


def _walk_repo_collecting_files(
    dir_path: str,
    files: list,
    *,
    repo_path: str,
    root: str,
    excluded_dirs,
    excluded_exts,
    excluded_files,
    gitignore_spec,
    is_path_inside_root,
) -> None:
    directories, regular_files = _partition_dir_entries(dir_path)
    descendable = _collect_descendable_dirs(
        directories, repo_path, excluded_dirs, gitignore_spec
    )
    _append_included_files(
        files,
        regular_files,
        repo_path=repo_path,
        root=root,
        excluded_files=excluded_files,
        excluded_exts=excluded_exts,
        gitignore_spec=gitignore_spec,
        is_path_inside_root=is_path_inside_root,
    )
    for full_path in descendable:
        _walk_repo_collecting_files(
            full_path,
            files,
            repo_path=repo_path,
            root=root,
            excluded_dirs=excluded_dirs,
            excluded_exts=excluded_exts,
            excluded_files=excluded_files,
            gitignore_spec=gitignore_spec,
            is_path_inside_root=is_path_inside_root,
        )


def dfs_file_list(repo_path, excluded_dirs, excluded_exts, excluded_files, gitignore_spec=None):
    """Depth-first, deterministically-ordered walk of the repo, yielding
    absolute file paths. Directories and files are sorted at each level so
    the ordering is stable across runs (important since overlap depends on
    a consistent DFS order).

    File symlinks that resolve outside ``repo_path`` are skipped (untrusted
    trees). Directory symlinks are not followed (``os.path.isdir`` on the
    link itself without walking through it via ``os.listdir`` of the target
    as a root — we only recurse into real directories under the walk).

    gitignore_spec, if given, is a pathspec.PathSpec (see
    _shared_excludes.load_gitignore_spec) additionally consulted against
    each entry's path relative to repo_path — opt-in, off by default, on
    top of the hardcoded excluded_dirs/excluded_exts/excluded_files floor,
    not a replacement for it."""
    from doc_engine.core.walk import is_path_inside_root

    files = []
    root = os.path.abspath(repo_path)
    _walk_repo_collecting_files(
        repo_path,
        files,
        repo_path=repo_path,
        root=root,
        excluded_dirs=excluded_dirs,
        excluded_exts=excluded_exts,
        excluded_files=excluded_files,
        gitignore_spec=gitignore_spec,
        is_path_inside_root=is_path_inside_root,
    )
    return files

