"""Covering receipts and empty-inventory helpers for ast-grep."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from doc_engine.scanning.astgrep.errors import AstGrepError
from doc_engine.scanning.covering import build_receipt, subset_root


def inventory_root_empty() -> str:
    from doc_engine.scanning.covering import inventory_root

    return inventory_root({})


def covering_receipt(
    backend: Any,
    *,
    expected_root: str,
    acked_root: str,
    covered_count: int,
    batches: int,
    error: Optional[str] = None,
    winerror_206_bisects: int = 0,
) -> Dict[str, Any]:
    """Build a covering receipt and raise when status is failed."""
    status = "complete" if acked_root == expected_root else "failed"
    if status == "failed" and error is None:
        error = "acked java subset does not match ScanContext inventory"
    receipt = build_receipt(
        scanner=backend.name,
        version_hash=backend.version_hash(),
        scope="java",
        expected_subset_root=expected_root,
        acked_subset_root=acked_root,
        status=status,
        covered_count=covered_count,
        batches=batches,
        winerror_206_bisects=winerror_206_bisects,
        error=error if status == "failed" else None,
    )
    if status == "failed":
        raise AstGrepError(error or "ast-grep covering receipt failed")
    return receipt


def empty_java_inventory_result(
    backend: Any,
    *,
    sigs: Dict[str, str],
    expected_root: str,
) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Covering result when ScanContext supplies an empty java_files list."""
    acked_root = subset_root(sigs, []) if sigs else expected_root
    error = (
        None
        if acked_root == expected_root
        else "empty java_files inventory does not cover ScanContext java signatures"
    )
    receipt = covering_receipt(
        backend,
        expected_root=expected_root,
        acked_root=acked_root,
        covered_count=0,
        batches=0,
        error=error,
    )
    return [], receipt
