"""Aggregate citation-coverage report + prose formatting."""

from __future__ import annotations

import os

from doc_engine.tools.citation_coverage_anchors import find_weak_anchors
from doc_engine.tools.citation_coverage_claims import (
    find_miscased_tags,
    find_untagged_claims,
)
from doc_engine.tools.citation_coverage_constants import DEFAULT_ANCHOR_WINDOW


def check_docs(docs_dir, target_repo, window=DEFAULT_ANCHOR_WINDOW):
    """Run both checks over every .md in docs_dir."""
    report = {}
    for name in sorted(os.listdir(docs_dir)):
        if not name.endswith(".md"):
            continue
        text = open(os.path.join(docs_dir, name), encoding="utf-8").read()
        entry = {
            "untagged_claims": find_untagged_claims(text),
            "miscased_tags": find_miscased_tags(text),
            "weak_anchors": [],
        }
        if target_repo is not None:
            entry["weak_anchors"] = find_weak_anchors(text, target_repo, window)
        report[name] = entry
    return report


def total_findings(report):
    return sum(
        len(v["untagged_claims"]) + len(v["miscased_tags"]) + len(v["weak_anchors"])
        for v in report.values()
    )


def _format_untagged_lines(findings):
    lines = []
    for finding in findings:
        lines.append(
            f"  [untagged_claim] line {finding['line']}: {finding['claim'][:110]}"
        )
        lines.append(
            f"      names {', '.join(finding['named_artifacts'][:5])} — no evidence tag"
        )
    return lines


def _format_miscased_lines(findings):
    lines = []
    for finding in findings:
        lines.append(f"  [miscased_tag] {finding['tag']}")
        lines.append(f"      {finding['reason']}")
    return lines


def _format_weak_anchor_lines(findings):
    lines = []
    for finding in findings:
        lines.append(f"  [{finding['kind']}] {finding['citation']}")
        lines.append(f"      claim: {finding['claim'][:110]}")
        lines.append(f"      {finding['reason']}")
    return lines


def _format_file_findings(name, entry):
    items = entry["untagged_claims"] + entry["miscased_tags"] + entry["weak_anchors"]
    if not items:
        return []
    lines = [f"{name}:"]
    lines.extend(_format_untagged_lines(entry["untagged_claims"]))
    lines.extend(_format_miscased_lines(entry["miscased_tags"]))
    lines.extend(_format_weak_anchor_lines(entry["weak_anchors"]))
    return lines


def format_report(report, target_repo):
    lines = []
    for name in sorted(report):
        lines.extend(_format_file_findings(name, report[name]))
    if target_repo is None:
        lines.append(
            "NOTE: no --target-repo given, so the weak-anchor check did not run. "
            "Only untagged-claim coverage was checked."
        )
    if not lines:
        lines.append("No citation-coverage findings.")
    return "\n".join(lines)
