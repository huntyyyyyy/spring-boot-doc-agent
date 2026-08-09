"""CLI adapter for spring_drift_check (argv → check_drift → JSON report).

Looks up ``check_drift`` / path helpers via the ``spring_drift_check`` façade so
characterization tests can monkeypatch the public module surface.
"""

from __future__ import annotations

import argparse
import json
import sys


def _require_path(path: str, *, expect_dir: bool) -> None:
    from doc_engine.tools import spring_drift_check as drift

    want = "dir" if expect_dir else "file"
    try:
        drift.checked_path(path, want=want)
    except drift.PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


def _validate_drift_cli_paths(args) -> None:
    _require_path(args.repo_path, expect_dir=True)
    _require_path(args.signals_path, expect_dir=False)
    if args.manifest is not None:
        _require_path(args.manifest, expect_dir=False)


def _print_drift_summary(out_path: str, report: dict) -> None:
    file_summary = report["file_summary"]
    print(
        f"Wrote {out_path}. Tier-1 baseline: {report['file_signatures_baseline']['source']}. "
        f"Citations checked: {report['citations_checked']}. "
        f"Status counts: {report['status_counts']}. "
        f"Files: {len(file_summary['unchanged'])} unchanged, {len(file_summary['changed'])} changed, "
        f"{len(file_summary['deleted'])} deleted, {len(file_summary['added'])} added (added files carry "
        f"no prior citations, so they're informational only)."
    )


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("repo_path")
    ap.add_argument(
        "signals_path",
        help="prior spring_signals.json to check for drift (schema_version >= 2)",
    )
    ap.add_argument("--out", default="drift_report.json")
    ap.add_argument(
        "--manifest",
        default=None,
        help=(
            "optional run_manifest.json (doc_engine.tools.run_manifest) whose "
            "file_signatures is used as the tier-1 baseline instead of "
            "signals_path's own — see module docstring's 'OPTIONAL --manifest' "
            "section. signals_path is still required, for tier-2 evidence "
            "run_manifest.json doesn't carry."
        ),
    )
    return ap


def _compute_drift_report(drift, args) -> dict:
    signals = drift.load_signals(args.signals_path)
    manifest = (
        drift.load_manifest(args.manifest) if args.manifest is not None else None
    )
    try:
        return drift.check_drift(args.repo_path, signals, manifest=manifest)
    except drift.spring_signal_scan.CodeQLScannerError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


def _write_drift_report(drift, out_arg: str, report: dict) -> None:
    try:
        out_path = drift.checked_output_path(out_arg)
    except drift.PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    with open(out_path, "w") as handle:
        json.dump(report, handle, indent=2)
    _print_drift_summary(str(out_path), report)


def main():
    from doc_engine.tools import spring_drift_check as drift

    args = _build_parser().parse_args()
    _validate_drift_cli_paths(args)
    report = _compute_drift_report(drift, args)
    _write_drift_report(drift, args.out, report)
