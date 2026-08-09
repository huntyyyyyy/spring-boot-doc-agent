"""Cohesive suite from tests/spring_signals/test_check_assertions.py: TestSpecLoading, TestQueryNameHygiene, TestAssertedExact, TestMinimums, TestFailClosed."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
import pytest
REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_PATH = REPO_ROOT / "spring-signals" / "harness" / "check-assertions.py"
HARNESS_DIR = ENGINE_PATH.parent
spec = importlib.util.spec_from_file_location("check_assertions", ENGINE_PATH)
ca = importlib.util.module_from_spec(spec)
sys.modules["check_assertions"] = ca
from tests.support.spring_signals.assertion_harness import (
    base_spec,
    row,
    run,
    write_csv,
    write_spec,
)

class TestSpecLoading:
    def test_missing_expectations_file_rejected(self, tmp_path):
        (tmp_path / "out").mkdir()
        with pytest.raises(SystemExit):
            run(tmp_path / "nope.json", tmp_path / "out")

    def test_malformed_json_rejected(self, tmp_path):
        (tmp_path / "out").mkdir()
        spec_path = tmp_path / "s.json"
        spec_path.write_text("{not json", encoding="utf-8")
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "out")

    def test_empty_spec_exits_2(self, tmp_path):
        (tmp_path / "out").mkdir()
        spec_path = write_spec(tmp_path / "s.json", base_spec())
        assert run(spec_path, tmp_path / "out") == 2

    def test_allow_empty_passes(self, tmp_path):
        (tmp_path / "out").mkdir()
        spec_path = write_spec(tmp_path / "s.json", base_spec())
        assert run(spec_path, tmp_path / "out", "--allow-empty") == 0

    def test_cli_path_with_dotdot_rejected(self, tmp_path):
        write_csv(tmp_path / "out", "A", [])
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 0}}))
        with pytest.raises(SystemExit):
            ca.main(["--out", str(tmp_path / "out" / ".." / "out"), "--expectations", str(spec_path)])


class TestQueryNameHygiene:
    @pytest.mark.parametrize(
        "bad",
        ["../etc", "x;rm -rf", "has space", "", "x/y", "..", ".hidden", "9leading",
         # \w without re.ASCII would admit these into path construction.
         "Ångström", "日本語"],
    )
    def test_rejected_names(self, tmp_path, bad):
        (tmp_path / "out").mkdir()
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={bad: {"_rows": 0}}))
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "out")

    @pytest.mark.parametrize("good", ["ApiSurface", "Messaging", "A", "q_1"])
    def test_valid_names_accepted(self, tmp_path, good):
        write_csv(tmp_path / "out", good, [])
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={good: {"_rows": 0}}))
        assert run(spec_path, tmp_path / "out") == 0


class TestAssertedExact:
    def test_asserted_exact_passes(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 3)
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 3}}))
        assert run(spec_path, tmp_path / "out") == 0

    def test_asserted_fails_high(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 4)
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 3}}))
        assert run(spec_path, tmp_path / "out") == 1

    def test_asserted_fails_low(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 2)
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 3}}))
        assert run(spec_path, tmp_path / "out") == 1

    def test_per_rule_counts_only_matching_rule_id(self, tmp_path):
        rows = [row("api_surface__controller", "g")] * 3 + [row("api_surface__endpoint", "h")] * 10
        write_csv(tmp_path / "out", "ApiSurface", rows)
        spec_path = write_spec(
            tmp_path / "s.json",
            base_spec(asserted={"ApiSurface": {"api_surface__controller": 4}}),
        )
        # 13 rows total; only 3 carry the pinned rule_id.
        assert run(spec_path, tmp_path / "out") == 1

    def test_boolean_count_rejected(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")])
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": True}}))
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "out")


class TestMinimums:
    def test_minimum_passes_at_equality(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 5)
        spec_path = write_spec(tmp_path / "s.json", base_spec(minimums={"A": {"_rows": 5}}))
        assert run(spec_path, tmp_path / "out") == 0

    def test_minimum_passes_above(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 6)
        spec_path = write_spec(tmp_path / "s.json", base_spec(minimums={"A": {"_rows": 5}}))
        assert run(spec_path, tmp_path / "out") == 0

    def test_minimum_fails_below(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 4)
        spec_path = write_spec(tmp_path / "s.json", base_spec(minimums={"A": {"_rows": 5}}))
        assert run(spec_path, tmp_path / "out") == 1


class TestFailClosed:
    def test_missing_csv_fails_not_zero(self, tmp_path):
        (tmp_path / "out").mkdir()
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"Ghost": {"_rows": 0}}))
        assert run(spec_path, tmp_path / "out") == 1

    def test_missing_out_dir_rejected(self, tmp_path):
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 0}}))
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "gone")

    def test_unexpected_csv_exits_2(self, tmp_path):
        write_csv(tmp_path / "out", "A", [])
        write_csv(tmp_path / "out", "Stale", [row("r", "g")])
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 0}}))
        with pytest.raises(SystemExit) as exc:
            run(spec_path, tmp_path / "out")
        assert exc.value.code == 2

    def test_utf16_csv_is_a_miss_not_a_traceback(self, tmp_path):
        # A PowerShell `>` re-decode produces UTF-16, which utf-8-sig cannot
        # read. The documented contract is fail-closed-as-missing (exit 1 via
        # MISS), never an uncaught UnicodeDecodeError.
        import codecs

        (tmp_path / "out").mkdir()
        (tmp_path / "out" / "A.csv").write_bytes(
            codecs.BOM_UTF16_LE + HEADER.encode("utf-16-le")
        )
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 0}}))
        assert run(spec_path, tmp_path / "out") == 1

    def test_utf8_bom_csv_reads_normally(self, tmp_path):
        import codecs

        (tmp_path / "out").mkdir()
        (tmp_path / "out" / "A.csv").write_bytes(
            codecs.BOM_UTF8 + (HEADER + row("r", "g")).encode("utf-8")
        )
        spec_path = write_spec(tmp_path / "s.json", base_spec(asserted={"A": {"_rows": 1}}))
        assert run(spec_path, tmp_path / "out") == 0
