"""Argparse surface for product commands (scan / docs / pipeline / query).

Gate-command parsers live in ``cli_gate_parsers``. Handlers stay in ``cli``.
"""

from __future__ import annotations

import argparse
from typing import Any, Callable

from doc_engine.cli_gate_parsers import add_quality_gate_parsers


def add_scan_parser(sub: Any, *, cmd_scan: Callable[..., int]) -> None:
    scan_ap = sub.add_parser("scan", help="Scan a repository and produce signals")
    scan_ap.add_argument("repo")
    scan_ap.add_argument(
        "--out",
        default="spring_signals.json",
        help=(
            "output path (default: spring_signals.json, same as Stage 0 / "
            "python -m doc_engine.tools.spring_signal_scan)"
        ),
    )
    scan_ap.add_argument(
        "--scanners",
        default=None,
        help="Comma-separated scanner names (overrides .doc-engine.yml)",
    )
    scan_ap.add_argument("--sql-dialect", default="ansi")
    scan_ap.add_argument("--respect-gitignore", action="store_true")
    scan_ap.add_argument("--build-command", default=None)
    scan_ap.add_argument("--db-path", default=None)
    scan_ap.add_argument(
        "--trust-repo-config",
        action="store_true",
        help=(
            "honor security-sensitive keys from the target repo's "
            ".doc-engine.yml (build_command, db_path, scanners, weakened "
            "compliance_profile). Default: treat that file as untrusted."
        ),
    )
    scan_ap.add_argument(
        "--allow-codeql-build",
        action="store_true",
        help=(
            "permit CodeQL database create --command against this tree. "
            "Required when --scanners includes codeql; only use for first-party "
            "repos or a sandboxed host."
        ),
    )
    scan_ap.set_defaults(func=cmd_scan)


def add_docs_site_parsers(
    sub: Any, *, cmd_docs: Callable[..., int], cmd_site: Callable[..., int]
) -> None:
    docs_ap = sub.add_parser(
        "docs",
        help="Placeholder docs bundle from signals (prefer: doc-engine pipeline run)",
    )
    docs_ap.add_argument("signals")
    docs_ap.add_argument("--out", default="docs.json")
    docs_ap.add_argument("--interview", default=None, help="Path to interview answers JSON")
    docs_ap.set_defaults(func=cmd_docs)

    site_ap = sub.add_parser("site", help="Build a static site from a docs bundle")
    site_ap.add_argument("docs")
    site_ap.add_argument("--out-dir", required=True)
    site_ap.add_argument("--site-name", default="Documentation")
    site_ap.set_defaults(func=cmd_site)


def add_pipeline_parsers(
    sub: Any,
    *,
    cmd_pipeline_run: Callable[..., int],
    cmd_pipeline_gates: Callable[..., int],
    add_run_arguments: Callable[[argparse.ArgumentParser], None],
) -> None:
    pipeline_ap = sub.add_parser(
        "pipeline",
        help="Run the document-spring-repo pipeline (deterministic + optional gates)",
    )
    pipeline_sub = pipeline_ap.add_subparsers(dest="pipeline_command", required=True)
    run_ap = pipeline_sub.add_parser(
        "run",
        help="Run locally against one target repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Deterministic stages use the package/scripts toolchain; "
            "Stages 1–4 are mocked unless you drive generative work via an "
            "external adapter (Claude, Cursor, etc.). Use --until STAGE to "
            "truncate the graph from build_stage_specs()."
        ),
    )
    add_run_arguments(run_ap)
    run_ap.set_defaults(func=cmd_pipeline_run)

    gates_ap = pipeline_sub.add_parser(
        "gates",
        help="Run mechanical gates on an existing run dir after live generative stages",
    )
    gates_ap.add_argument("--out-dir", required=True)
    gates_ap.add_argument("--target-repo", required=True)
    gates_ap.add_argument("--docs-dir", default=None)
    gates_ap.add_argument(
        "--compliance-profile",
        choices=["scan_only", "deterministic_only", "certified"],
        default=None,
        help=(
            "compliance profile (default: certified, or .doc-engine.yml). "
            "certified enables strict citation_coverage."
        ),
    )
    gates_ap.add_argument("--strict-citations", action="store_true")
    gates_ap.add_argument("--no-write-check", action="store_true")
    gates_ap.set_defaults(func=cmd_pipeline_gates)


def add_cert_query_parsers(
    sub: Any,
    *,
    cmd_certification_verify: Callable[..., int],
    cmd_query: Callable[..., int],
) -> None:
    cert_ap = sub.add_parser(
        "certification",
        help="Certification gate utilities",
    )
    cert_sub = cert_ap.add_subparsers(dest="certification_command", required=True)
    verify_ap = cert_sub.add_parser(
        "verify",
        help="Exit 0 only when certification.json reports certified: true",
    )
    verify_ap.add_argument(
        "path",
        nargs="?",
        default="certification.json",
        help="path to certification.json",
    )
    verify_ap.add_argument(
        "--allow-mock",
        action="store_true",
        help="accept generative_executor none/mock (default: require live)",
    )
    verify_ap.set_defaults(func=cmd_certification_verify)

    query_ap = sub.add_parser(
        "query",
        help=(
            "Typed read views over Stage-0 artifacts "
            "(evidence|routes|facts|entity|dependents|route-trace)"
        ),
    )
    query_ap.add_argument(
        "query_argv",
        nargs=argparse.REMAINDER,
        help="kind and flags — see: python -m doc_engine.tools.query_artifacts -h",
    )
    query_ap.set_defaults(func=cmd_query)


def build_parser(
    *,
    description: str,
    cmd_scan: Callable[..., int],
    cmd_docs: Callable[..., int],
    cmd_site: Callable[..., int],
    cmd_pipeline_run: Callable[..., int],
    cmd_pipeline_gates: Callable[..., int],
    cmd_certification_verify: Callable[..., int],
    cmd_query: Callable[..., int],
    cmd_quality_gates: Callable[..., int],
    cmd_coverage_gap_average: Callable[..., int],
    cmd_coverage_measure: Callable[..., int],
    cmd_complexipy_ratchet: Callable[..., int],
    cmd_size_ratchet: Callable[..., int],
    add_run_arguments: Callable[[argparse.ArgumentParser], None],
) -> argparse.ArgumentParser:
    """Build the top-level ``doc-engine`` argparse tree."""
    ap = argparse.ArgumentParser(prog="doc-engine", description=description)
    sub = ap.add_subparsers(dest="command", required=True)
    add_scan_parser(sub, cmd_scan=cmd_scan)
    add_docs_site_parsers(sub, cmd_docs=cmd_docs, cmd_site=cmd_site)
    add_pipeline_parsers(
        sub,
        cmd_pipeline_run=cmd_pipeline_run,
        cmd_pipeline_gates=cmd_pipeline_gates,
        add_run_arguments=add_run_arguments,
    )
    add_cert_query_parsers(
        sub,
        cmd_certification_verify=cmd_certification_verify,
        cmd_query=cmd_query,
    )
    add_quality_gate_parsers(
        sub,
        cmd_quality_gates=cmd_quality_gates,
        cmd_coverage_gap_average=cmd_coverage_gap_average,
        cmd_coverage_measure=cmd_coverage_measure,
        cmd_complexipy_ratchet=cmd_complexipy_ratchet,
        cmd_size_ratchet=cmd_size_ratchet,
    )
    return ap
