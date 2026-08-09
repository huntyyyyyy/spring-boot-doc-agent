"""SDK facade: ``scan_repository`` → Stage-0 ``spring.scan``.

Kept out of ``scanning/__init__.py`` so the package can stay import-lazy
(no sqlfluff on every tool CLI) without calling ``__getattr__`` from a
public function body.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from doc_engine.scanning.spring import scan


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
    return scan(
        repo_path,
        sql_dialect=sql_dialect,
        respect_gitignore=respect_gitignore,
        build_command=build_command,
        db_path=db_path,
        scanners=scanners,
        scan_context=scan_context,
        allow_codeql_build=allow_codeql_build,
    )
