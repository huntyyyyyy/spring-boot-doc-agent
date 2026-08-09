#!/usr/bin/env python3
"""Read-only typed queries over Stage-0 artifacts.

Run with: python -m doc_engine.tools.query_artifacts <kind> …

Kinds: evidence | routes | facts | entity | dependents | route-trace | context-packet
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from doc_engine.query.load import QueryError, require_server_root
from doc_engine.query.registry import run_query
from doc_engine.tools.query_artifacts_parsers import build_query_artifacts_parser


def _build_parser() -> argparse.ArgumentParser:
    return build_query_artifacts_parser()


def _artifact_parent_root(args: argparse.Namespace) -> Path:
    artifact = (
        getattr(args, "signals", None)
        or getattr(args, "facts", None)
        or getattr(args, "run_dir", None)
    )
    if artifact:
        return Path(artifact).resolve().parent
    return Path.cwd()


def _resolve_cli_root(args: argparse.Namespace) -> Path:
    """Pick containment root for a CLI invocation."""
    if getattr(args, "unsafe_no_root", False):
        # Explicit CLI-only; still need a root for _resolve — use artifact parent later
        return Path.cwd()
    if getattr(args, "root", None):
        return Path(args.root)
    if os.environ.get("DOC_ENGINE_ROOT") or os.environ.get("DOC_ENGINE_RUN_DIR"):
        return require_server_root()
    return _artifact_parent_root(args)


def _query_evidence(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "evidence",
        signals_path=args.signals,
        root=root,
        limit=args.limit,
        bucket=args.bucket,
        rule_id=args.rule_id,
        file_contains=args.file_contains,
        match_contains=args.match_contains,
    )


def _query_routes(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "routes",
        signals_path=args.signals,
        root=root,
        limit=args.limit,
        path_contains=args.path_contains,
        rule_id=args.rule_id,
        file_contains=args.file_contains,
    )


def _query_facts(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "facts",
        facts_path=args.facts,
        root=root,
        limit=args.limit,
        predicate=args.predicate,
        file_contains=args.file_contains,
        fqcn=args.fqcn,
        subject_contains=args.subject_contains,
    )


def _query_entity(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "entity",
        signals_path=args.signals,
        root=root,
        limit=args.limit,
        class_name=args.class_name,
        table=args.table,
        fqcn=args.fqcn,
    )


def _query_dependents(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "dependents",
        signals_path=args.signals,
        edges_path=args.edges,
        root=root,
        limit=args.limit,
        target_file=args.target_file,
        target_type=args.target_type,
        group_id=args.group_id,
    )


def _query_route_trace(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    return run_query(
        "route-trace",
        signals_path=args.signals,
        root=root,
        limit=args.limit,
        path_contains=args.path_contains,
        file_contains=args.file_contains,
    )


def _query_context_packet(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    from doc_engine.query.packet import run_context_packet

    return run_context_packet(
        args.request,
        run_dir=args.run_dir,
        budget_tokens=args.budget_tokens,
        root=root,
        repo_path=args.repo_path,
        drift_report_path=args.drift_report,
    )


_KIND_HANDLERS = {
    "evidence": _query_evidence,
    "routes": _query_routes,
    "facts": _query_facts,
    "entity": _query_entity,
    "dependents": _query_dependents,
    "route-trace": _query_route_trace,
    "context-packet": _query_context_packet,
}


def _execute_kind(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    """Dispatch a parsed CLI kind to the matching query handler."""
    handler = _KIND_HANDLERS.get(args.kind)
    if handler is None:
        raise QueryError(f"unknown kind {args.kind}")
    return handler(args, root)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    root = _resolve_cli_root(args)
    try:
        result = _execute_kind(args, root)
    except QueryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
