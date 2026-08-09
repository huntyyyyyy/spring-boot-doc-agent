"""Argparse builders for query_artifacts CLI kinds."""

from __future__ import annotations

import argparse
from typing import Any

from doc_engine.query.envelope import DEFAULT_LIMIT


def build_common_parent() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--root",
        default=None,
        help="containment root (default: parent of artifact path, or DOC_ENGINE_ROOT)",
    )
    common.add_argument(
        "--unsafe-no-root",
        action="store_true",
        help="CLI-only escape hatch — refuse on MCP; not recommended",
    )
    common.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"max rows (default {DEFAULT_LIMIT}; hard-clamped)",
    )
    return common


def add_evidence_and_routes(sub: Any, common: argparse.ArgumentParser) -> None:
    ev = sub.add_parser(
        "evidence",
        parents=[common],
        help="filter spring_signals evidence buckets",
    )
    ev.add_argument("--signals", required=True)
    ev.add_argument("--bucket", default=None)
    ev.add_argument("--rule-id", default=None)
    ev.add_argument("--file", dest="file_contains", default=None)
    ev.add_argument("--match", dest="match_contains", default=None)

    rt = sub.add_parser("routes", parents=[common], help="api_surface evidence filter")
    rt.add_argument("--signals", required=True)
    rt.add_argument("--path-contains", default=None)
    rt.add_argument("--rule-id", default=None)
    rt.add_argument("--file", dest="file_contains", default=None)


def add_facts_and_entity(sub: Any, common: argparse.ArgumentParser) -> None:
    fa = sub.add_parser("facts", parents=[common], help="filter facts.jsonl")
    fa.add_argument("--facts", required=True)
    fa.add_argument("--predicate", default=None)
    fa.add_argument("--file", dest="file_contains", default=None)
    fa.add_argument("--fqcn", default=None)
    fa.add_argument("--subject-contains", default=None)

    en = sub.add_parser("entity", parents=[common], help="entity_table_map lookup")
    en.add_argument("--signals", required=True)
    en.add_argument("--class", dest="class_name", default=None)
    en.add_argument("--table", default=None)
    en.add_argument("--fqcn", default=None)


def add_dependents_and_route_trace(sub: Any, common: argparse.ArgumentParser) -> None:
    dep = sub.add_parser(
        "dependents",
        parents=[common],
        help="import dependents / importers",
    )
    dep.add_argument("--signals", required=True)
    dep.add_argument("--file", dest="target_file", default=None)
    dep.add_argument("--type", dest="target_type", default=None)
    dep.add_argument("--edges", default=None, help="optional cross_group_edges.json")
    dep.add_argument("--group", dest="group_id", default=None)

    tr = sub.add_parser(
        "route-trace",
        parents=[common],
        help="api_surface × same-file security",
    )
    tr.add_argument("--signals", required=True)
    tr.add_argument("--path-contains", default=None)
    tr.add_argument("--file", dest="file_contains", default=None)


def add_context_packet(sub: Any, common: argparse.ArgumentParser) -> None:
    cp = sub.add_parser(
        "context-packet",
        parents=[common],
        help="ranked Mako-class packet over a Stage-0 run dir",
    )
    cp.add_argument("--run-dir", required=True, help="directory with spring_signals.json")
    cp.add_argument("--request", required=True, help="natural-language or keyword request")
    cp.add_argument(
        "--budget-tokens",
        type=int,
        default=None,
        help="token budget (chars/4 proxy; default 4000, hard-clamped)",
    )
    cp.add_argument(
        "--repo", dest="repo_path", default=None, help="optional target repo for freshness"
    )
    cp.add_argument("--drift-report", default=None, help="optional drift_report.json")


def build_query_artifacts_parser() -> argparse.ArgumentParser:
    common = build_common_parent()
    p = argparse.ArgumentParser(
        description="Query Stage-0 artifacts (capped typed read views).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="kind", required=True)
    add_evidence_and_routes(sub, common)
    add_facts_and_entity(sub, common)
    add_dependents_and_route_trace(sub, common)
    add_context_packet(sub, common)
    return p
