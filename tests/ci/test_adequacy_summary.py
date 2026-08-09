"""TDD coverage for adequacy markdown presenter + CLI façade (E-QA1)."""

from __future__ import annotations

from pathlib import Path

import adequacy_summary as cli
import pytest

from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_METAMORPHIC_VACUITY,
    SLICE_KIND_MUTATOR_SURVIVORS,
    SLICE_KIND_STRUCTURAL,
    AdequacyReport,
    AdequacySlice,
)
from doc_engine.ci.adequacy.github_adequacy_summary import (
    append_github_summary,
    build_adequacy_report,
    format_adequacy_markdown,
    render_adequacy_report,
)

pytestmark = pytest.mark.domain_ci_meta


def _mini_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "scripts" / "ratchets").mkdir(parents=True)
    (root / "tests" / "spring_signals").mkdir(parents=True)
    (root / "scripts" / "coverage" / "rule_fixtures").mkdir(parents=True)
    baseline = root / "scripts" / "ratchets" / "mutation_baseline.json"
    baseline.write_text(
        '{"schema_version": 1, "accepted_survivors": {}}\n',
        encoding="utf-8",
    )
    (root / "scripts" / "ratchets" / "mutate.py").write_text(
        "ENFORCE = False\n", encoding="utf-8"
    )
    (root / "tests" / "spring_signals" / "mutation_driver.py").write_text(
        "ENFORCE = False\n", encoding="utf-8"
    )
    (root / "scripts" / "coverage" / "rule_fixtures" / "A.java").write_text(
        "class A {}", encoding="utf-8"
    )
    return root


def test_format_adequacy_markdown_lists_slices() -> None:
    report = AdequacyReport(
        slices=(
            AdequacySlice(
                kind=SLICE_KIND_STRUCTURAL,
                title="Structural coverage (sensor)",
                body_lines=("XML line-rate: **99.00%**.",),
                present=True,
            ),
            AdequacySlice(
                kind=SLICE_KIND_MUTATOR_SURVIVORS,
                title="Mutator survivors (hermetic inventory)",
                body_lines=("registry count: **3**.",),
                present=True,
            ),
            AdequacySlice(
                kind=SLICE_KIND_METAMORPHIC_VACUITY,
                title="Metamorphic vacuity (hermetic pointers)",
                body_lines=("fixture count: **10**.",),
                present=True,
            ),
        )
    )
    markdown = format_adequacy_markdown(report)
    assert "### Adequacy sensors (E-QA1)" in markdown
    assert "Structural coverage" in markdown
    assert "Mutator survivors" in markdown
    assert "Metamorphic vacuity" in markdown
    assert "Q2 witness" in markdown


def test_render_adequacy_report_hermetic_tmp_repo(tmp_path: Path) -> None:
    root = _mini_repo(tmp_path)
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.95"/>', encoding="utf-8")
    fixtures = root / "scripts" / "coverage" / "rule_fixtures"
    markdown = render_adequacy_report(
        coverage_xml=coverage,
        floor_echo="98.7",
        repo=root,
        registry_count=4,
        fixtures_dir=fixtures,
    )
    assert "95.00%" in markdown
    assert "registry count: **4**" in markdown or "**4**" in markdown
    assert "HarnessIsNotVacuousTest" in markdown
    report = build_adequacy_report(
        coverage_xml=coverage,
        repo=root,
        registry_count=4,
        fixtures_dir=fixtures,
    )
    assert report.slice_kinds() == (
        SLICE_KIND_STRUCTURAL,
        SLICE_KIND_MUTATOR_SURVIVORS,
        SLICE_KIND_METAMORPHIC_VACUITY,
    )


def test_append_github_summary_appends(tmp_path: Path) -> None:
    summary = tmp_path / "summary.md"
    summary.write_text("### prior\n", encoding="utf-8")
    append_github_summary("### Adequacy sensors (E-QA1)\n", summary)
    text = summary.read_text(encoding="utf-8")
    assert "### prior" in text
    assert "Adequacy sensors" in text


def test_append_github_summary_rejects_dotdot(tmp_path: Path) -> None:
    from doc_engine.paths import PathValidationError

    with pytest.raises(PathValidationError, match=r"\.\."):
        append_github_summary("x", tmp_path / ".." / "nope.md")


def test_adequacy_summary_cli_appends(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _mini_repo(tmp_path)
    coverage = tmp_path / "coverage.xml"
    coverage.write_text('<coverage line-rate="0.99"/>', encoding="utf-8")
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    assert (
        cli.main(
            [
                "--github-summary",
                "--coverage-xml",
                str(coverage),
                "--repo-root",
                str(root),
                "--registry-count",
                "2",
                "--fixtures-dir",
                str(root / "scripts" / "coverage" / "rule_fixtures"),
            ]
        )
        == 0
    )
    text = summary.read_text(encoding="utf-8")
    assert "Adequacy sensors" in text
    assert "99.00%" in text


def test_adequacy_summary_requires_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    assert cli.main(["--github-summary"]) == 2
