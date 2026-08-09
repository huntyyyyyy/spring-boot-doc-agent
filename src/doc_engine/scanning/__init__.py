"""Stage 0 scanning package.

Heavy scanners and sqllineage stay behind ``__getattr__`` / local imports so
lightweight tool CLIs (secrets heuristics, walk helpers) do not cold-start
sqlfluff on every ``python -m`` invocation.
"""

from typing import Any, Dict, List, Optional

__all__ = [
    "scan",
    "scan_repository",
    "run_scan",
    "get_scanner",
    "resolve_scanner_names",
    "SpringSignalMerger",
    "SpringLineageResolver",
]


def __getattr__(name: str) -> Any:
    if name == "scan":
        from doc_engine.scanning.spring import scan

        return scan
    if name == "run_scan":
        from doc_engine.scanning._orchestrator import run_scan

        return run_scan
    if name in ("get_scanner", "resolve_scanner_names"):
        from doc_engine.scanning import _scanner_registry as registry

        return getattr(registry, name)
    if name == "SpringSignalMerger":
        from doc_engine.scanning._merge_signals import SpringSignalMerger

        return SpringSignalMerger
    if name == "SpringLineageResolver":
        from doc_engine.scanning._resolve_lineage import SpringLineageResolver

        return SpringLineageResolver
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def scan_repository(
    repo_path: str,
    sql_dialect: str = "ansi",
    respect_gitignore: bool = False,
    build_command: Optional[str] = None,
    db_path: Optional[str] = None,
    scanners: Optional[List[str]] = None,
    scan_context: Optional[Any] = None,
    allow_codeql_build: bool = False,
) -> Dict[str, Any]:
    """Run Stage 0 signal extraction for a Spring Boot repository."""
    return __getattr__("scan")(
        repo_path,
        sql_dialect=sql_dialect,
        respect_gitignore=respect_gitignore,
        build_command=build_command,
        db_path=db_path,
        scanners=scanners,
        scan_context=scan_context,
        allow_codeql_build=allow_codeql_build,
    )
