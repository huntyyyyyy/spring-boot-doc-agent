"""Emit the ABI domain×paths×python GitHub Actions matrix.

Usage:
    python -m doc_engine.ci.emit_abi_matrix
    python -m doc_engine.ci.emit_abi_matrix --python-versions 3.10,3.12

Writes compact JSON to ``GITHUB_OUTPUT`` (multiline ``matrix``) when that
env var is set; always prints the pretty matrix on stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from doc_engine.ci.test_path_shards import github_matrix_include
from doc_engine.paths import repo_root

DEFAULT_PYTHON_VERSIONS = ("3.10", "3.12")


def build_abi_matrix(
    repo: Path,
    python_versions: tuple[str, ...],
) -> dict[str, list[dict[str, str]]]:
    """Cartesian product of interpreter cells and discovered domain path groups."""
    rows: list[dict[str, str]] = []
    for python_version in python_versions:
        for row in github_matrix_include(repo):
            rows.append(
                {
                    "python-version": python_version,
                    "id": row["id"],
                    "marker": row["marker"],
                    "paths": row["paths"],
                }
            )
    if not rows:
        raise SystemExit("domain_path_matrix produced zero ABI rows")
    return {"include": rows}


def write_github_output(matrix: dict[str, list[dict[str, str]]]) -> None:
    """Append ``matrix`` to ``GITHUB_OUTPUT`` using the multiline EOF form."""
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    payload = json.dumps(matrix, separators=(",", ":"))
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write("matrix<<EOF\n")
        handle.write(payload)
        handle.write("\nEOF\n")


def main(argv: list[str] | None = None) -> int:
    """CLI entry for ABI matrix emission."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--python-versions",
        default=",".join(DEFAULT_PYTHON_VERSIONS),
        help="Comma-separated CPython versions (default: 3.10,3.12)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: doc_engine.paths.repo_root())",
    )
    args = parser.parse_args(argv)
    versions = tuple(
        part.strip() for part in args.python_versions.split(",") if part.strip()
    )
    root = (args.repo_root or repo_root()).resolve()
    matrix = build_abi_matrix(root, versions)
    write_github_output(matrix)
    print(json.dumps(matrix, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
