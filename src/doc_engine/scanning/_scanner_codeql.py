#!/usr/bin/env python3
"""CodeQL ``ScannerBackend`` port.

Orchestrates Stage-0 CodeQL: run queries (``support/_codeql_runner``), project
rows into evidence + entity_table_map candidates (``support/_codeql_evidence``,
``support/_codeql_entity_map``), and emit a covering receipt for the Java scope.
"""

from __future__ import annotations

import glob
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from doc_engine.core.context import ScanContext
from doc_engine.scanning._paths import codeql_pack_dir
from doc_engine.scanning._scanner_base import ScannerBackend
from doc_engine.scanning.covering import COVERING_RECEIPT_KEY
from doc_engine.scanning.support._codeql_evidence import project_codeql_rows
from doc_engine.scanning.support._codeql_runner import CodeQLError, scan_with_codeql


def _acked_java_paths(
    scan_context: Optional[ScanContext],
    expected_paths: List[str],
) -> List[str]:
    """Java paths CodeQL covering treats as acknowledged for this scan."""
    if scan_context is None:
        return expected_paths
    return sorted({entry.rel_path for entry in scan_context.java_files})


class CodeQLBackend(ScannerBackend):
    """Scanner backend that extracts Java structural signals via CodeQL."""

    @property
    def name(self) -> str:
        return "codeql"

    @staticmethod
    def _version_hash_paths() -> List[str]:
        """Hash this port + every ``support/_codeql_*.py`` sibling + query pack."""
        self_file = Path(__file__).resolve()
        support = self_file.parent / "support"
        paths = [str(self_file)]
        paths.extend(sorted(map(str, support.glob("_codeql_*.py"))))
        pack_dir = codeql_pack_dir()
        if pack_dir.is_dir():
            paths.extend(sorted(glob.glob(str(pack_dir / "*.ql"))))
        return paths

    @staticmethod
    def _update_digest_from_path(digest: Any, path: str) -> None:
        try:
            with open(path, "rb") as handle:
                for chunk in iter(lambda: handle.read(1 << 20), b""):
                    digest.update(chunk)
        except OSError:
            return

    def version_hash(self) -> str:
        digest = hashlib.sha256()
        for path in sorted(self._version_hash_paths()):
            self._update_digest_from_path(digest, path)
        return digest.hexdigest()[:16]

    def scan(
        self,
        repo_path: str,
        build_command: Optional[str] = None,
        db_path: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        repo_path = os.path.abspath(repo_path)
        scan_context: Optional[ScanContext] = kwargs.get("scan_context")

        if build_command is None:
            raise CodeQLError(
                "CodeQL backend requires a build command. "
                "Pass --build-command or use detect_build_command()."
            )

        rows = scan_with_codeql(
            Path(repo_path),
            build_command,
            pack_dir=codeql_pack_dir(),
            db_path=Path(db_path) if db_path else None,
            keep_database=True,
            scanner_version=self.version_hash(),
            scan_context=scan_context,
        )

        evidence, entity_candidates = project_codeql_rows(
            repo_path=repo_path,
            rows=rows,
            scan_context=scan_context,
        )
        receipt = self._covering_receipt_for_scan(scan_context)
        return {
            "evidence": evidence,
            "entity_table_map_candidates": entity_candidates,
            COVERING_RECEIPT_KEY: receipt,
        }

    def _covering_receipt_for_scan(
        self,
        scan_context: Optional[ScanContext],
    ) -> Dict[str, Any]:
        from doc_engine.scanning.covering import (
            build_receipt,
            java_scope_paths,
            subset_root,
        )

        sigs = dict(scan_context.file_signatures) if scan_context is not None else {}
        expected_paths = java_scope_paths(sigs)
        expected_root = subset_root(sigs, expected_paths)
        acked = _acked_java_paths(scan_context, expected_paths)
        acked_root = subset_root(sigs, acked)
        status = "complete" if acked_root == expected_root else "failed"
        receipt = build_receipt(
            scanner=self.name,
            version_hash=self.version_hash(),
            scope="java",
            expected_subset_root=expected_root,
            acked_subset_root=acked_root,
            status=status,
            covered_count=len(acked),
            batches=1,
            error=None if status == "complete" else "codeql acked java subset mismatch",
        )
        if status == "failed":
            raise CodeQLError(receipt["error"] or "codeql covering receipt failed")
        return receipt
