"""CLI adapter for partition_repo (argv → groups.json)."""

from __future__ import annotations

import argparse
import json
import sys

from doc_engine.core.excludes import DEFAULT_EXCLUDED_DIRS, load_gitignore_spec
from doc_engine.paths import PathValidationError, checked_output_path, checked_path
from doc_engine.tools.partition_repo_constants import (
    DEFAULT_EXCLUDED_EXTS,
    DEFAULT_EXCLUDED_FILES,
)
from doc_engine.tools.partition_repo_groups import build_groups
from doc_engine.tools.partition_repo_tokens import estimate_tokens, relpath_posix
from doc_engine.tools.partition_repo_walk import dfs_file_list


def _collect_file_tokens(repo_path, all_files, max_file_bytes):
    file_tokens = []
    skipped = []
    for full_path in all_files:
        rel = relpath_posix(full_path, repo_path)
        tokens, reason = estimate_tokens(full_path, max_file_bytes)
        if reason:
            skipped.append({"file": rel, "reason": reason})
            continue
        file_tokens.append((rel, tokens))
    return file_tokens, skipped


def _groups_output_payload(repo_path, max_tokens, overlap, file_tokens, skipped, groups_raw):
    return {
        "repo_path": repo_path,
        "max_tokens_per_group": max_tokens,
        "overlap": overlap,
        "total_files_considered": len(file_tokens),
        "total_files_skipped": len(skipped),
        "skipped": skipped,
        "num_groups": len(groups_raw),
        "groups": [
            {
                "id": index,
                "files": [path for path, _ in group],
                "est_tokens": sum(tokens for _, tokens in group),
            }
            for index, group in enumerate(groups_raw)
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo_path", help="Path to the repository root")
    ap.add_argument("--max-tokens", type=int, default=120000,
                    help="Target max tokens per group (default: 120000; leave headroom under the model's context window)")
    ap.add_argument("--overlap", type=float, default=0.10,
                    help="Fraction of a group's trailing tokens carried into the next group (default: 0.10)")
    ap.add_argument("--out", default="groups.json", help="Output JSON path (default: groups.json)")
    ap.add_argument("--exclude-dir", action="append", default=[],
                    help="Additional directory name to exclude (repeatable)")
    ap.add_argument("--max-file-bytes", type=int, default=2_000_000,
                    help="Skip files larger than this many bytes (default: 2,000,000)")
    ap.add_argument("--respect-gitignore", action="store_true", default=False,
                    help="Additionally exclude paths matched by the repo's own .gitignore, "
                         "on top of the hardcoded exclude list (default: off; requires the "
                         "pathspec library)")
    args = ap.parse_args()

    try:
        repo_path = str(checked_path(args.repo_path, want="dir"))
        out_path = checked_output_path(args.out)
    except PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    excluded_dirs = DEFAULT_EXCLUDED_DIRS | set(args.exclude_dir)
    gitignore_spec = load_gitignore_spec(repo_path) if args.respect_gitignore else None
    all_files = dfs_file_list(
        repo_path,
        excluded_dirs,
        DEFAULT_EXCLUDED_EXTS,
        DEFAULT_EXCLUDED_FILES,
        gitignore_spec=gitignore_spec,
    )
    file_tokens, skipped = _collect_file_tokens(repo_path, all_files, args.max_file_bytes)
    groups_raw = build_groups(file_tokens, args.max_tokens, args.overlap)
    output = _groups_output_payload(
        repo_path, args.max_tokens, args.overlap, file_tokens, skipped, groups_raw
    )

    with open(out_path, "w") as handle:
        json.dump(output, handle, indent=2)

    print(
        f"Wrote {out_path}: {output['num_groups']} groups, "
        f"{output['total_files_considered']} files considered, "
        f"{output['total_files_skipped']} skipped."
    )

