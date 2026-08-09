"""GitHub step-summary presenter for adequacy sensors (E-QA1).

OCP: additional sinks belong in sibling modules — do not grow a parser here.

Usage:
    from doc_engine.ci.adequacy.github_adequacy_summary import (
        format_adequacy_markdown,
        render_adequacy_report,
    )
"""

from __future__ import annotations

from pathlib import Path

from doc_engine.ci.adequacy.criterion_ports import AdequacyReport, AdequacySlice
from doc_engine.ci.adequacy.metamorphic_vacuity import (
    load_metamorphic_vacuity_inventory,
    metamorphic_vacuity_slice,
)
from doc_engine.ci.adequacy.mutator_survivors import (
    default_paths,
    load_mutator_survivor_inventory,
    mutator_survivors_slice,
)
from doc_engine.ci.adequacy.structural_summary import structural_slice


def format_adequacy_markdown(report: AdequacyReport) -> str:
    """Assemble markdown sections for each adequacy sensor slice."""
    sections: list[str] = ["### Adequacy sensors (E-QA1)\n"]
    sections.append(
        "Sensors only — do not claim fail_under / Cover% floor. "
        "Climb Archive still needs a Q2 witness "
        "(incident mutant / mutmut slice / metamorphic relation).\n"
    )
    for item in report.slices:
        sections.append(_format_slice(item))
    return "\n".join(sections)


def _format_slice(item: AdequacySlice) -> str:
    lines = [f"#### {item.title}\n"]
    for body in item.body_lines:
        lines.append(f"- {body}")
    lines.append("")
    return "\n".join(lines)


def build_adequacy_report(
    *,
    coverage_xml: Path,
    floor_echo: str = "98.7",
    repo: Path | None = None,
    registry_count: int | None = None,
    fixtures_dir: Path | None = None,
) -> AdequacyReport:
    """Compose the three hermetic adequacy slices into one report."""
    baseline, gate, assertion = default_paths(repo)
    inventory = load_mutator_survivor_inventory(
        baseline_path=baseline,
        gate_mutate_path=gate,
        assertion_driver_path=assertion,
        registry_count=registry_count,
    )
    meta = load_metamorphic_vacuity_inventory(fixtures_dir=fixtures_dir)
    return AdequacyReport(
        slices=(
            structural_slice(coverage_xml, floor_echo=floor_echo),
            mutator_survivors_slice(inventory),
            metamorphic_vacuity_slice(meta),
        )
    )


def render_adequacy_report(
    *,
    coverage_xml: Path,
    floor_echo: str = "98.7",
    repo: Path | None = None,
    registry_count: int | None = None,
    fixtures_dir: Path | None = None,
) -> str:
    """Build markdown for the composed adequacy report."""
    report = build_adequacy_report(
        coverage_xml=coverage_xml,
        floor_echo=floor_echo,
        repo=repo,
        registry_count=registry_count,
        fixtures_dir=fixtures_dir,
    )
    return format_adequacy_markdown(report)


def append_github_summary(markdown: str, summary_path: Path) -> None:
    """Append markdown to an existing GitHub step summary file."""
    previous = ""
    if summary_path.is_file():
        previous = summary_path.read_text(encoding="utf-8")
    if previous and not previous.endswith("\n"):
        previous += "\n"
    summary_path.write_text(previous + markdown, encoding="utf-8")
