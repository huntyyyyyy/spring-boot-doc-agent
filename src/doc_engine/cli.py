"""CLI entry point for the doc-engine package."""

import argparse
import json
import sys
from typing import Any, Dict  # Any used by parser-builder helpers

from doc_engine import Engine
from doc_engine.config import Config, load_repo_config, merge_config, sanitize_repo_settings, trust_from_flag
from doc_engine.pipeline.local_run import add_run_arguments, run_pipeline


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _split_scanner_names(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def _scan_cli_overrides(args: argparse.Namespace) -> Dict[str, Any]:
    """Map scan CLI flags onto Config override keys."""
    overrides: Dict[str, Any] = {}
    if args.scanners:
        overrides["scanners"] = _split_scanner_names(args.scanners)
    if args.sql_dialect != "ansi":
        overrides["sql_dialect"] = args.sql_dialect
    _apply_optional_scan_flags(args, overrides)
    return overrides


def _apply_optional_scan_flags(args: argparse.Namespace, overrides: Dict[str, Any]) -> None:
    if args.respect_gitignore:
        overrides["respect_gitignore"] = True
    if args.build_command:
        overrides["build_command"] = args.build_command
    if args.db_path:
        overrides["db_path"] = args.db_path


def _scan_config(repo: str, args: argparse.Namespace) -> Config:
    trust = trust_from_flag(bool(getattr(args, "trust_repo_config", False)))
    base = sanitize_repo_settings(load_repo_config(repo) or Config(), trust) or Config()
    return merge_config(base, _scan_cli_overrides(args))


def cmd_scan(args: argparse.Namespace) -> int:
    config = _scan_config(args.repo, args)
    engine = Engine(config)
    try:
        signals = engine.scan(
            args.repo,
            allow_codeql_build=bool(getattr(args, "allow_codeql_build", False)),
        )
    except Exception as exc:
        from doc_engine.scanning.spring import CodeQLScannerError

        if isinstance(exc, CodeQLScannerError):
            print(f"error: {exc}", file=sys.stderr)
            return 1
        raise
    _save_json(args.out, signals)
    print(f"Wrote signals to {args.out}")
    return 0


def cmd_docs(args: argparse.Namespace) -> int:
    signals = _load_json(args.signals)
    interview = _load_json(args.interview) if args.interview else {}
    engine = Engine()
    bundle = engine.generate_docs(signals, interview_answers=interview)
    _save_json(args.out, bundle)
    print(f"Wrote docs bundle to {args.out}")
    return 0


def cmd_site(args: argparse.Namespace) -> int:
    bundle = _load_json(args.docs)
    engine = Engine()
    site_path = engine.build_site(bundle, out_dir=args.out_dir, site_name=args.site_name)
    print(f"Built site at {site_path}")
    return 0


def cmd_pipeline_run(args: argparse.Namespace) -> int:
    return run_pipeline(args)


def cmd_pipeline_gates(args: argparse.Namespace) -> int:
    from doc_engine.pipeline.live_gates import main as gates_main

    argv = [
        "--out-dir",
        args.out_dir,
        "--target-repo",
        args.target_repo,
    ]
    if args.docs_dir:
        argv.extend(["--docs-dir", args.docs_dir])
    if getattr(args, "compliance_profile", None):
        argv.extend(["--compliance-profile", args.compliance_profile])
    if args.strict_citations:
        argv.append("--strict-citations")
    if args.no_write_check:
        argv.append("--no-write-check")
    return gates_main(argv)


def cmd_certification_verify(args: argparse.Namespace) -> int:
    from doc_engine.tools.certification import main as cert_main

    argv = [args.path]
    if getattr(args, "allow_mock", False):
        argv.append("--allow-mock")
    return cert_main(argv)


def cmd_query(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine query <kind> …`` → tools.query_artifacts."""
    from doc_engine.tools.query_artifacts import main as query_main

    argv = list(getattr(args, "query_argv", None) or [])
    return query_main(_without_argparse_separator(argv))


def cmd_quality_gates(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine quality-gates`` → ci.quality_gates."""
    from doc_engine.ci.quality_gates import main as quality_gates_main

    argv = ["--compare-ref", args.compare_ref]
    if args.coverage_xml is not None:
        argv.extend(["--coverage-xml", str(args.coverage_xml)])
    if args.skip_coverage:
        argv.append("--skip-coverage")
    if args.no_fail_fast:
        argv.append("--no-fail-fast")
    return quality_gates_main(argv)


def cmd_coverage_gap_average(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine coverage-gap-average``."""
    from doc_engine.ci.coverage_gap_average import main as gap_main

    argv: list[str] = []
    if args.coverage_xml is not None:
        argv.extend(["--coverage-xml", str(args.coverage_xml)])
    if args.floor is not None:
        argv.extend(["--floor", str(args.floor)])
    if args.worst is not None:
        argv.extend(["--worst", str(args.worst)])
    if args.markdown:
        argv.append("--markdown")
    if args.append_github_summary:
        argv.append("--append-github-summary")
    return gap_main(argv)


def cmd_complexipy_ratchet(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine complexipy-ratchet``."""
    from doc_engine.ci.complexipy_ratchet import main as ratchet_main

    argv: list[str] = []
    if args.baseline is not None:
        argv.extend(["--baseline", str(args.baseline)])
    if args.update:
        argv.append("--update")
    return ratchet_main(argv)


def cmd_size_ratchet(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine size-ratchet``."""
    from doc_engine.ci.size_ratchet import main as size_main

    argv: list[str] = []
    if args.baseline is not None:
        argv.extend(["--baseline", str(args.baseline)])
    if args.update:
        argv.append("--update")
    return size_main(argv)


def _without_argparse_separator(argv: list[str]) -> list[str]:
    """Drop a leading ``--`` left over from argparse ``REMAINDER``."""
    parts = iter(argv)
    first = next(parts, None)
    if first is None:
        return []
    if first == "--":
        return list(parts)
    return [first, *parts]


def _add_scan_parser(sub: Any) -> None:
    scan_ap = sub.add_parser("scan", help="Scan a repository and produce signals")
    scan_ap.add_argument("repo")
    scan_ap.add_argument(
        "--out",
        default="spring_signals.json",
        help="output path (default: spring_signals.json, same as Stage 0 / python -m doc_engine.tools.spring_signal_scan)",
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


def _add_docs_site_parsers(sub: Any) -> None:
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


def _add_pipeline_parsers(sub: Any) -> None:
    pipeline_ap = sub.add_parser(
        "pipeline",
        help="Run the document-spring-repo pipeline (deterministic + optional gates)",
    )
    pipeline_sub = pipeline_ap.add_subparsers(dest="pipeline_command", required=True)
    run_ap = pipeline_sub.add_parser(
        "run",
        help="Run locally against one target repo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Deterministic stages use the package/scripts toolchain; "
               "Stages 1–4 are mocked unless you drive generative work via an "
               "external adapter (Claude, Cursor, etc.). Use --until STAGE to "
               "truncate the graph from build_stage_specs().",
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
        help="compliance profile (default: certified, or .doc-engine.yml). "
             "certified enables strict citation_coverage.",
    )
    gates_ap.add_argument("--strict-citations", action="store_true")
    gates_ap.add_argument("--no-write-check", action="store_true")
    gates_ap.set_defaults(func=cmd_pipeline_gates)


def _add_cert_query_parsers(sub: Any) -> None:
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


def _add_quality_gate_parsers(sub: Any) -> None:
    qg_ap = sub.add_parser(
        "quality-gates",
        help=(
            "Hard in-repo gates: new-code coverage, jscpd, complexipy <=5, "
            "size ratchet, tach (same on Mac/Windows/Linux)"
        ),
    )
    qg_ap.add_argument(
        "--compare-ref",
        required=True,
        help="Git ref for new-code baseline (PR base SHA, origin/main, HEAD~1)",
    )
    qg_ap.add_argument(
        "--coverage-xml",
        default=None,
        help="Cobertura XML from pytest-cov (default: ./coverage.xml)",
    )
    qg_ap.add_argument(
        "--skip-coverage",
        action="store_true",
        help="Skip diff-cover (local debug only)",
    )
    qg_ap.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Run every gate even after a failure",
    )
    qg_ap.set_defaults(func=cmd_quality_gates)

    gap_ap = sub.add_parser(
        "coverage-gap-average",
        help="Report Cover% averaged only over files still below the floor",
    )
    gap_ap.add_argument("--coverage-xml", default=None)
    gap_ap.add_argument("--floor", type=float, default=None)
    gap_ap.add_argument("--worst", type=int, default=None)
    gap_ap.add_argument("--markdown", action="store_true")
    gap_ap.add_argument("--append-github-summary", action="store_true")
    gap_ap.set_defaults(func=cmd_coverage_gap_average)

    ratchet_ap = sub.add_parser(
        "complexipy-ratchet",
        help="Ratchet complexipy offender count vs scripts/ratchets baseline",
    )
    ratchet_ap.add_argument("--baseline", default=None)
    ratchet_ap.add_argument("--update", action="store_true")
    ratchet_ap.set_defaults(func=cmd_complexipy_ratchet)

    size_ap = sub.add_parser(
        "size-ratchet",
        help="Ratchet file LOC / function statement hard ceilings vs baseline",
    )
    size_ap.add_argument("--baseline", default=None)
    size_ap.add_argument("--update", action="store_true")
    size_ap.set_defaults(func=cmd_size_ratchet)


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level ``doc-engine`` argparse tree."""
    ap = argparse.ArgumentParser(prog="doc-engine", description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    _add_scan_parser(sub)
    _add_docs_site_parsers(sub)
    _add_pipeline_parsers(sub)
    _add_cert_query_parsers(sub)
    _add_quality_gate_parsers(sub)
    return ap


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
