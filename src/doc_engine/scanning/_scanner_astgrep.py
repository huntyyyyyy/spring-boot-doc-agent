#!/usr/bin/env python3
"""ast-grep scanner façade — stable AstGrepBackend + poke / test re-exports.

Concept modules under ``scanning.astgrep``; ``version_hash`` hashes façade + package + rules.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from doc_engine.core.context import ScanContext
from doc_engine.core.excludes import load_gitignore_spec
from doc_engine.scanning._paths import ast_grep_rules_path
from doc_engine.scanning._scanner_base import ScannerBackend
from doc_engine.scanning.astgrep import argv as astgrep_argv
from doc_engine.scanning.astgrep import covering_scan as astgrep_covering
from doc_engine.scanning.astgrep import ingest as astgrep_ingest
from doc_engine.scanning.astgrep import invoke as astgrep_invoke
from doc_engine.scanning.astgrep.errors import AstGrepError, AstGrepNotFoundError
from doc_engine.scanning.astgrep.ports import DEFAULT_RUNNER, AstGrepRunner
from doc_engine.scanning.covering import COVERING_RECEIPT_KEY
from doc_engine.scanning.java_extract import extract_entity, read_source_lines

RULE_FILE = ast_grep_rules_path()
_PATH_LIST_CHAR_LIMIT = astgrep_argv._PATH_LIST_CHAR_LIMIT
chunk_paths_for_argv = astgrep_argv.chunk_paths_for_argv
_enrich_query_entry = astgrep_ingest.enrich_query_entry
_is_windows_cmdline_too_long = astgrep_argv.is_windows_cmdline_too_long
inventory_root_empty = astgrep_covering.inventory_root_empty
_parse_ast_grep_stdout = astgrep_invoke.parse_ast_grep_stdout


def _astgrep_errors():
    return AstGrepError, AstGrepNotFoundError


def _version_hash_paths() -> List[str]:
    """Hash façade + every ``astgrep/*.py`` sibling + rule file."""
    self_file = Path(__file__).resolve()
    package = self_file.parent / "astgrep"
    paths = [str(self_file), str(RULE_FILE)]
    paths.extend(sorted(map(str, package.glob("*.py"))))
    return paths


class AstGrepBackend(ScannerBackend):
    """Scanner backend that extracts Java structural signals via ast-grep."""

    def __init__(self, runner: Optional[AstGrepRunner] = None) -> None:
        self._runner = runner if runner is not None else DEFAULT_RUNNER

    @property
    def name(self) -> str:
        return "ast-grep"

    def version_hash(self) -> str:
        digest = hashlib.sha256()
        for path in sorted(self._version_hash_paths()):
            try:
                with open(path, "rb") as handle:
                    for chunk in iter(lambda: handle.read(1 << 20), b""):
                        digest.update(chunk)
            except OSError:
                pass
        return digest.hexdigest()[:16]

    @staticmethod
    def _version_hash_paths() -> List[str]:
        return _version_hash_paths()

    def _find_ast_grep(self) -> Optional[str]:
        return shutil.which("ast-grep")

    def _scan_base_argv(self, ast_grep_path: str) -> List[str]:
        return astgrep_invoke.scan_base_argv(ast_grep_path, RULE_FILE)

    def _require_ast_grep_ready(self) -> str:
        return astgrep_invoke.require_ast_grep_ready(self._find_ast_grep, RULE_FILE)

    def _invoke_ast_grep(self, cmd: List[str]) -> List[Dict[str, Any]]:
        return astgrep_invoke.invoke_ast_grep(cmd, runner=self._runner)

    def _bisect_oversized_chunk(
        self,
        base_argv: List[str],
        chunk: List[str],
        char_limit: int,
    ) -> tuple[List[Dict[str, Any]], int]:
        return astgrep_invoke.bisect_oversized_chunk(
            self, base_argv, chunk, char_limit
        )

    def _scan_one_chunk(
        self,
        base_argv: List[str],
        chunk: List[str],
        char_limit: int,
    ) -> tuple[List[Dict[str, Any]], int]:
        return astgrep_invoke.scan_one_chunk(self, base_argv, chunk, char_limit)

    def _invoke_ast_grep_chunked(
        self,
        base_argv: List[str],
        paths: List[str],
        *,
        limit: Optional[int] = None,
    ) -> tuple[List[Dict[str, Any]], int, int]:
        return astgrep_invoke.invoke_ast_grep_chunked(
            self, base_argv, paths, limit=limit
        )

    def _covering_receipt(self, **kwargs: Any) -> Dict[str, Any]:
        return astgrep_covering.covering_receipt(self, **kwargs)

    def _empty_java_inventory_result(self, **kwargs: Any):
        return astgrep_covering.empty_java_inventory_result(self, **kwargs)

    def _record_entity_match(self, **kwargs: Any) -> None:
        astgrep_ingest.record_entity_match(**kwargs)

    def _record_bucket_match(self, **kwargs: Any) -> None:
        astgrep_ingest.record_bucket_match(**kwargs)

    def _ingest_ast_grep_match(self, **kwargs: Any) -> None:
        astgrep_ingest.ingest_ast_grep_match(**kwargs)

    def _run_ast_grep(
        self,
        repo_path: str,
        java_files: Optional[list] = None,
        *,
        file_signatures: Optional[Dict[str, str]] = None,
    ):
        # Inventory guard + chunked path stay on the class so
        # behavior:astgrep_inventory_never_widens_to_repo_root resolves.
        if java_files is None:
            raise AstGrepError(
                "java_files inventory not supplied; "
                "repo-root scan cannot prove covering"
            )
        from doc_engine.scanning.covering import java_scope_paths, subset_root

        base_argv = self._scan_base_argv(self._require_ast_grep_ready())
        sigs = file_signatures or {}
        expected_paths = java_scope_paths(sigs) if sigs else []
        expected_root = (
            subset_root(sigs, expected_paths) if sigs else inventory_root_empty()
        )
        if not java_files:
            return self._empty_java_inventory_result(
                sigs=sigs, expected_root=expected_root
            )
        paths = [entry.full_path for entry in java_files]
        acked_rels = [entry.rel_path for entry in java_files]
        matches, batches, bisects = self._invoke_ast_grep_chunked(base_argv, paths)
        acked_root = subset_root(sigs, acked_rels) if sigs else expected_root
        receipt = self._covering_receipt(
            expected_root=expected_root,
            acked_root=acked_root,
            covered_count=len(acked_rels),
            batches=batches,
            winerror_206_bisects=bisects,
        )
        return matches, receipt

    def scan(
        self,
        repo_path: str,
        sql_dialect: str = "ansi",
        respect_gitignore: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        repo_path = os.path.abspath(repo_path)
        scan_context: Optional[ScanContext] = kwargs.get("scan_context")
        java_files = scan_context.java_files if scan_context is not None else None
        file_signatures = (
            dict(scan_context.file_signatures) if scan_context is not None else {}
        )
        matches, receipt = self._run_ast_grep(
            repo_path,
            java_files=java_files,
            file_signatures=file_signatures,
        )
        gitignore_spec = load_gitignore_spec(repo_path) if respect_gitignore else None
        evidence: Dict[str, List[Dict[str, Any]]] = {}
        entity_table_map_candidates: Dict[str, List[Dict[str, Any]]] = {}
        seen: set = set()
        for match in matches:
            self._ingest_ast_grep_match(
                match=match,
                repo_path=repo_path,
                gitignore_spec=gitignore_spec,
                evidence=evidence,
                entity_table_map_candidates=entity_table_map_candidates,
                seen=seen,
            )
        for bucket in evidence.values():
            bucket.sort(key=lambda entry: (entry["file"], entry.get("line", 0)))
        return {
            "evidence": evidence,
            "entity_table_map_candidates": entity_table_map_candidates,
            COVERING_RECEIPT_KEY: receipt,
        }


__all__ = [
    "AstGrepBackend",
    "AstGrepError",
    "AstGrepNotFoundError",
    "RULE_FILE",
    "_PATH_LIST_CHAR_LIMIT",
    "chunk_paths_for_argv",
    "_enrich_query_entry",
    "extract_entity",
    "read_source_lines",
    "subprocess",
    "os",
    "shutil",
]
