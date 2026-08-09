"""CodeQL query pack execution and BQRS decode.

Behavioral strategy for running every ``.ql`` in a pack and normalizing rows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from doc_engine.core.timeouts import tool_timeout_seconds
from doc_engine.scanning.support import _codeql_cli as cli
from doc_engine.scanning.support._codeql_cli import CodeQLError


def discover_queries(pack_dir: Path) -> List[Path]:
    """Return all .ql files in the pack directory, sorted."""
    return sorted(pack_dir.glob("*.ql"))

def run_query(
    codeql_path: Path,
    db_path: Path,
    query_file: Path,
    bqrs_path: Path,
) -> None:
    """Run a single .ql query against a database, writing a BQRS file."""
    proc = cli._invoke_codeql(
        codeql_path,
        ("query", "run"),
        f"--database={db_path}",
        f"--output={bqrs_path}",
        str(query_file),
        timeout=tool_timeout_seconds(),
    )
    if proc.returncode != 0:
        raise CodeQLError(
            f"codeql query run failed for {query_file.name} "
            f"(exit {proc.returncode}):\n{proc.stderr}\n{proc.stdout}"
        )

def decode_bqrs(
    codeql_path: Path,
    bqrs_path: Path,
) -> List[Dict[str, Any]]:
    """Decode a BQRS file to a list of dicts keyed by column name.

    CodeQL's JSON output is:
      {"#select": {"columns": [{"name": "file", "kind": "String"}, ...],
                   "tuples": [[...], ...]}}
    We map each tuple to a dict using the column names. Columns without a
    name get synthetic names (col_0, col_1, ...).
    """
    proc = cli._invoke_codeql(
        codeql_path,
        ("bqrs", "decode"),
        "--format=json",
        # Include source locations and strings as plain values.
        "--entities=string,url",
        str(bqrs_path),
        timeout=tool_timeout_seconds(),
    )
    if proc.returncode != 0:
        raise CodeQLError(
            f"codeql bqrs decode failed for {bqrs_path} "
            f"(exit {proc.returncode}):\n{proc.stderr}\n{proc.stdout}"
        )
    return _rows_from_bqrs_json(json.loads(proc.stdout))

def _column_names_from_bqrs(columns: List[Dict[str, Any]]) -> List[str]:
    names = []
    for i, col in enumerate(columns):
        name = col.get("name") or f"col_{i}"
        names.append(name)
    return names

def _rows_from_bqrs_json(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    select = raw.get("#select", {})
    names = _column_names_from_bqrs(select.get("columns", []))
    return [
        {names[i]: value for i, value in enumerate(row)}
        for row in select.get("tuples", [])
    ]

def run_all_queries(
    codeql_path: Path,
    db_path: Path,
    pack_dir: Path,
    tmp_dir: Path,
) -> List[Dict[str, Any]]:
    """Run every .ql query in the pack and return merged decoded results."""
    queries = discover_queries(pack_dir)
    if not queries:
        raise CodeQLError(f"no .ql queries found in {pack_dir}")

    all_rows: List[Dict[str, Any]] = []
    for query in queries:
        bqrs_path = tmp_dir / f"{query.stem}.bqrs"
        run_query(codeql_path, db_path, query, bqrs_path)
        rows = decode_bqrs(codeql_path, bqrs_path)
        for row in rows:
            # Tag every row with the query file that produced it, useful for
            # debugging and drift-check provenance.
            row["_query_file"] = query.name
        all_rows.extend(rows)
    return all_rows

