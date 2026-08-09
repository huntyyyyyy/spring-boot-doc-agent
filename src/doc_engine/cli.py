"""CLI entry point for the doc-engine package."""

import argparse
import sys

from doc_engine import Engine
from doc_engine.cli_scan_config import scan_config
from doc_engine.core.jsonio import dump_json, load_json
from doc_engine.pipeline.local_run import add_run_arguments, run_pipeline


def cmd_scan(args: argparse.Namespace) -> int:
    config = scan_config(args.repo, args)
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
    dump_json(args.out, signals)
    print(f"Wrote signals to {args.out}")
    return 0


def cmd_docs(args: argparse.Namespace) -> int:
    signals = load_json(args.signals)
    interview = load_json(args.interview) if args.interview else {}
    engine = Engine()
    bundle = engine.generate_docs(signals, interview_answers=interview)
    dump_json(args.out, bundle)
    print(f"Wrote docs bundle to {args.out}")
    return 0


def cmd_site(args: argparse.Namespace) -> int:
    bundle = load_json(args.docs)
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


def _coverage_measure_argv(args: argparse.Namespace) -> list[str]:
    """Build argv for ``coverage_measure_cli.main`` from the thin CLI facade."""
    argv: list[str] = []
    if getattr(args, "mode", None):
        argv.extend(["--mode", str(args.mode)])
    if getattr(args, "scope", None):
        argv.extend(["--scope", str(args.scope)])
    if args.floor is not None:
        argv.extend(["--floor", str(args.floor)])
    if args.worst is not None:
        argv.extend(["--worst", str(args.worst)])
    if args.skip_pytest:
        argv.append("--skip-pytest")
    if args.no_gap_report:
        argv.append("--no-gap-report")
    if args.pytest_args:
        argv.extend(args.pytest_args)
    return argv


def cmd_coverage_measure(args: argparse.Namespace) -> int:
    """Facade: ``doc-engine coverage-measure`` — oracle SoT or climb sensor."""
    from doc_engine.ci.coverage_measure_cli import main as measure_main

    return measure_main(_coverage_measure_argv(args))


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


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level ``doc-engine`` argparse tree."""
    from doc_engine.cli_parsers import build_parser as build_cli_parser

    return build_cli_parser(
        description=__doc__ or "",
        cmd_scan=cmd_scan,
        cmd_docs=cmd_docs,
        cmd_site=cmd_site,
        cmd_pipeline_run=cmd_pipeline_run,
        cmd_pipeline_gates=cmd_pipeline_gates,
        cmd_certification_verify=cmd_certification_verify,
        cmd_query=cmd_query,
        cmd_quality_gates=cmd_quality_gates,
        cmd_coverage_gap_average=cmd_coverage_gap_average,
        cmd_coverage_measure=cmd_coverage_measure,
        cmd_complexipy_ratchet=cmd_complexipy_ratchet,
        cmd_size_ratchet=cmd_size_ratchet,
        add_run_arguments=add_run_arguments,
    )


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
