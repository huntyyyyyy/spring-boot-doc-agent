"""Coverage climb B6: adequacy sensors remaining edges.

Q2 adequacy witness: mutmut_slice on doc_engine.ci.adequacy.* — asserts bite
default_fixtures_dir roots, ENFORCE/survivor ValueErrors, default_paths(root),
structural missing/present XML, and github summary append (not padding).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doc_engine.ci.adequacy import github_adequacy_summary as gas
from doc_engine.ci.adequacy import metamorphic_vacuity as meta
from doc_engine.ci.adequacy import mutator_survivors as ms
from doc_engine.ci.adequacy import structural_summary as structural
from doc_engine.ci.adequacy.criterion_ports import (
    SLICE_KIND_MUTATOR_SURVIVORS,
    SLICE_KIND_STRUCTURAL,
)
from doc_engine.ci.adequacy.mutator_survivors import MutatorSurvivorInventory

pytestmark = pytest.mark.domain_climb_sensor


def test_default_fixtures_dir_none_and_root(tmp_path: Path) -> None:
    defaulted = meta.default_fixtures_dir(None)
    assert defaulted.as_posix().endswith("scripts/coverage/rule_fixtures")
    rooted = meta.default_fixtures_dir(tmp_path)
    assert rooted == tmp_path / "scripts" / "coverage" / "rule_fixtures"


def test_mutator_enforce_and_survivors_errors(tmp_path: Path) -> None:
    bare = tmp_path / "no_enforce.py"
    bare.write_text("OTHER = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ENFORCE assignment not found"):
        ms.read_enforce_flag(bare)

    bad = tmp_path / "mutation_baseline.json"
    bad.write_text(
        '{"schema_version": 1, "accepted_survivors": ["not-an-object"]}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="accepted_survivors must be an object"):
        ms.read_accepted_survivors(bad)

    baseline, gate, assertion = ms.default_paths(tmp_path)
    assert baseline == tmp_path / "scripts" / "ratchets" / "mutation_baseline.json"
    assert gate.name == "mutate.py"
    assert assertion.name == "mutation_driver.py"


def test_mutator_slice_empty_names_and_path_insert(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    inventory = MutatorSurvivorInventory(
        registry_count=2,
        accepted_survivor_names=(),
        gate_enforce=False,
        assertion_enforce=False,
    )
    slice_row = ms.mutator_survivors_slice(inventory)
    assert slice_row.kind == SLICE_KIND_MUTATOR_SURVIVORS
    assert "(none" in " ".join(slice_row.body_lines)

    # Force path-insert branch when entry missing from sys.path.
    entry = str(tmp_path / "scripts_meta")
    Path(entry).mkdir()
    monkeypatch.setattr(ms, "scripts_meta_path_entries", lambda: [entry])
    # Registry import still resolves from real repo path entries or fails —
    # inject a stub module via sys.modules after ensuring insert ran.
    import sys
    import types

    stub = types.ModuleType("mutator_registry")
    stub.all_mutators = lambda: ["a", "b", "c"]  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "mutator_registry", stub)
    assert ms.registry_mutator_count() == 3
    assert entry in sys.path


def test_structural_slice_missing_and_present(tmp_path: Path) -> None:
    missing = structural.structural_slice(tmp_path / "gone.xml")
    assert missing.kind == SLICE_KIND_STRUCTURAL
    assert missing.present is False
    assert "missing" in missing.body_lines[0]

    xml = tmp_path / "coverage.xml"
    xml.write_text(
        '<coverage line-rate="0.955" branch-rate="0.9"></coverage>\n',
        encoding="utf-8",
    )
    present = structural.structural_slice(xml, floor_echo="98.7")
    assert present.present is True
    assert "95.50%" in present.body_lines[0]


def test_github_adequacy_report_and_append(tmp_path: Path) -> None:
    fixtures = tmp_path / "rule_fixtures"
    fixtures.mkdir()
    (fixtures / "One.java").write_text("class One {}", encoding="utf-8")
    scripts = tmp_path / "scripts" / "ratchets"
    scripts.mkdir(parents=True)
    (scripts / "mutation_baseline.json").write_text(
        '{"schema_version": 1, "accepted_survivors": {}}\n',
        encoding="utf-8",
    )
    (scripts / "mutate.py").write_text("ENFORCE = False\n", encoding="utf-8")
    driver = tmp_path / "tests" / "spring_signals"
    driver.mkdir(parents=True)
    (driver / "mutation_driver.py").write_text("ENFORCE = False\n", encoding="utf-8")
    xml = tmp_path / "coverage.xml"
    xml.write_text('<coverage line-rate="0.99"></coverage>\n', encoding="utf-8")

    md = gas.render_adequacy_report(
        coverage_xml=xml,
        repo=tmp_path,
        registry_count=4,
        fixtures_dir=fixtures,
    )
    assert "Adequacy sensors" in md
    assert "Structural coverage" in md
    assert "Mutator survivors" in md
    assert "Metamorphic vacuity" in md

    summary = tmp_path / "summary.md"
    summary.write_text("### prior", encoding="utf-8")
    gas.append_github_summary(md, summary)
    body = summary.read_text(encoding="utf-8")
    assert body.startswith("### prior\n")
    assert "Adequacy sensors" in body
