"""Pre-pytest cascade note when coverage.xml is missing (E-RUN1 / D17).

Sensor-only: missing XML usually means an earlier gate failed before the
oracle pytest cell wrote Cobertura — not a fail_under miss by itself.

Usage:
    from doc_engine.ci.suite_timing.pre_pytest_cascade import cascade_markdown
"""

from __future__ import annotations

from pathlib import Path

# Gate classes that run before the 3.11 cov cell in python-gates.yml.
_PRE_PYTEST_GATE_CLASSES: tuple[str, ...] = (
    "ruff",
    "check_code_quality",
    "check_repo_claims",
    "check_workflow_yaml / verify_tool_pins",
    "rule_coverage / domain markers",
)


def coverage_xml_present(coverage_xml: Path) -> bool:
    return coverage_xml.is_file()


def cascade_markdown(*, coverage_xml: Path) -> str:
    """Markdown explaining missing coverage.xml as a pre-pytest cascade."""
    if coverage_xml_present(coverage_xml):
        return ""
    gates = ", ".join(_PRE_PYTEST_GATE_CLASSES)
    return (
        "### Pre-pytest cascade (D17)\n\n"
        "coverage.xml missing — pytest may have failed before writing it, "
        "or an earlier gate class failed so the cov cell never ran "
        f"(look for red steps among: {gates}). "
        "This summary is a sensor, not a fail_under / Cover% SoT claim.\n"
    )
