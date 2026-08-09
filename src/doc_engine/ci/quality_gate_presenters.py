"""Presenters for quality-gates rollup (text + GitHub step-summary markdown).

OCP: orchestration stays in ``quality_gates``; this module only formats sinks
and Actions log-group wrappers (E-UX1).
"""

from __future__ import annotations

import os

from doc_engine.ci.github_step_summary import append_markdown


def begin_grouped_run(label: str, command: list[str]) -> bool:
    """Print gate banner; return True when an Actions ``::group::`` was opened."""
    grouped = os.environ.get("GITHUB_ACTIONS") == "true"
    if grouped:
        print(f"::group::{label}", flush=True)
    print(f"\n=== {label} ===", flush=True)
    print("+", " ".join(command), flush=True)
    return grouped


def end_grouped_run(grouped: bool) -> None:
    """Close an Actions log group opened by :func:`begin_grouped_run`."""
    if grouped:
        print("::endgroup::", flush=True)


def gate_status_phrase(name: str, ran: set[str], results: list[tuple[str, int]]) -> str:
    """Return PASS / FAIL / SKIPPED label for one planned gate."""
    if name not in ran:
        return "SKIPPED (fail-fast)"
    code = next(code for gate_name, code in results if gate_name == name)
    return "PASS" if code == 0 else f"FAIL (exit {code})"


def format_gates_text(
    planned_names: list[str], results: list[tuple[str, int]]
) -> str:
    """Plain stdout summary block."""
    ran = {name for name, _ in results}
    lines = ["=== quality-gates summary ==="]
    for name in planned_names:
        lines.append(f"- {name}: {gate_status_phrase(name, ran, results)}")
    return "\n".join(lines)


def format_gates_markdown(
    planned_names: list[str], results: list[tuple[str, int]]
) -> str:
    """GitHub step-summary markdown: headline table + fail-fast note."""
    ran = {name for name, _ in results}
    lines = [
        "### Quality gates\n",
        "| Gate | Status |",
        "| --- | --- |",
    ]
    for name in planned_names:
        lines.append(f"| `{name}` | {gate_status_phrase(name, ran, results)} |")
    skipped = [name for name in planned_names if name not in ran]
    if skipped:
        lines.append("")
        lines.append(
            "<details><summary>Fail-fast skipped gates</summary>\n\n"
            + ", ".join(f"`{name}`" for name in skipped)
            + "\n\n</details>\n"
        )
    lines.append("")
    return "\n".join(lines)


def publish_gates_summary(
    planned_names: list[str], results: list[tuple[str, int]]
) -> None:
    """Print text summary; append markdown when ``GITHUB_STEP_SUMMARY`` is set."""
    print("\n" + format_gates_text(planned_names, results), flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary:
        return
    append_markdown(format_gates_markdown(planned_names, results), summary)
