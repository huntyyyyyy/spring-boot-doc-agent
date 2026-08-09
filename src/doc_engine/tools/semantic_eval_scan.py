"""Scan artifacts dir + CLI for semantic-eval mechanical helpers."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from doc_engine.paths import (
    PathValidationError,
    checked_output_path,
    checked_path,
)
from doc_engine.tools.semantic_eval_confirmed import (
    DEFAULT_OVERLAP_THRESHOLD,
    find_unmatched_confirmed_tags,
)
from doc_engine.tools.semantic_eval_mermaid import (
    check_mermaid_syntax,
    extract_mermaid_block,
)


def _facade():
    """Lazy façade bind so monkeypatch.setattr(seh, 'join_under', …) still bites."""
    from doc_engine.tools import semantic_eval_helpers as facade

    return facade


def load_interview_answers(artifacts_dir):
    path = os.path.join(artifacts_dir, "interview_answers.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def is_safe_markdown_basename(docs_dir: str, name: str) -> bool:
    if not name.endswith(".md") or Path(name).name != name:
        return False
    try:
        _facade().join_under(docs_dir, name)
    except PathValidationError:
        return False
    return True


def markdown_names(docs_dir: str):
    return [n for n in sorted(os.listdir(docs_dir)) if is_safe_markdown_basename(docs_dir, n)]


def confirmed_findings_for_doc(docs_dir, name, interview_answers, overlap_threshold):
    path = _facade().join_under(docs_dir, name)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    return find_unmatched_confirmed_tags(text, interview_answers, overlap_threshold)


def scan_confirmed_docs(artifacts_dir, interview_answers, overlap_threshold):
    confirmed_findings = {}
    docs_dir = _facade().join_under(artifacts_dir, "docs")
    if not docs_dir.is_dir():
        return confirmed_findings
    for name in markdown_names(str(docs_dir)):
        findings = confirmed_findings_for_doc(
            str(docs_dir), name, interview_answers, overlap_threshold
        )
        if findings:
            confirmed_findings[name] = findings
    return confirmed_findings


def resolve_architecture_path(artifacts_dir: str) -> str | None:
    for parts in (("docs", "architecture.md"), ("architecture.md",)):
        try:
            candidate = _facade().join_under(artifacts_dir, *parts)
        except PathValidationError:
            continue
        if candidate.is_file():
            return str(candidate)
    return None


def scan_mermaid(artifacts_dir: str):
    arch_path = resolve_architecture_path(artifacts_dir)
    if arch_path is None:
        return []
    with open(arch_path, encoding="utf-8") as handle:
        arch_text = handle.read()
    mermaid = extract_mermaid_block(arch_text)
    if mermaid is None:
        return []
    return check_mermaid_syntax(mermaid)


def run(artifacts_dir, overlap_threshold=DEFAULT_OVERLAP_THRESHOLD):
    artifacts_dir = str(checked_path(artifacts_dir, want="dir"))
    interview_answers = load_interview_answers(artifacts_dir)
    return {
        "artifacts_dir": os.path.abspath(artifacts_dir),
        "unmatched_confirmed_tags_by_file": scan_confirmed_docs(
            artifacts_dir, interview_answers, overlap_threshold
        ),
        "mermaid_syntax_findings": scan_mermaid(artifacts_dir),
    }


def _print_summary(report) -> None:
    total_confirmed = sum(len(v) for v in report["unmatched_confirmed_tags_by_file"].values())
    print(
        f"semantic_eval_helpers: {total_confirmed} unmatched [Confirmed] tag(s) across "
        f"{len(report['unmatched_confirmed_tags_by_file'])} file(s); "
        f"{len(report['mermaid_syntax_findings'])} Mermaid syntax finding(s)."
    )


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "artifacts_dir",
        help="Directory containing a completed pipeline run's output",
    )
    ap.add_argument("--target-repo", default=None, help="Reserved; unused here")
    ap.add_argument(
        "--overlap-threshold",
        type=float,
        default=DEFAULT_OVERLAP_THRESHOLD,
        help=f"Jaccard threshold (default: {DEFAULT_OVERLAP_THRESHOLD})",
    )
    ap.add_argument("--out", default=None, help="Optional path to write findings as JSON")
    args = ap.parse_args()

    try:
        report = run(args.artifacts_dir, args.overlap_threshold)
    except PathValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.out:
        try:
            out_path = checked_output_path(args.out)
        except PathValidationError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    _print_summary(report)
