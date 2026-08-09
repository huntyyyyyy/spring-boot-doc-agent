"""Cohesive suite from tests/spring_signals/test_check_assertions.py: TestSnapshots, TestSignals, TestKnownDefects, TestRecord, TestRealExpectations, TestEndToEnd."""

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

class TestSnapshots:
    def test_snapshot_match_passes(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 7)
        spec_path = write_spec(tmp_path / "s.json", base_spec(snapshot={"A": {"_rows": 7}}))
        assert run(spec_path, tmp_path / "out") == 0

    def test_snapshot_drift_fails(self, tmp_path):
        # Snapshots encode current behaviour, not intent; drift still fails the
        # gate here -- --record is the deliberate update path.
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 8)
        spec_path = write_spec(tmp_path / "s.json", base_spec(snapshot={"A": {"_rows": 7}}))
        assert run(spec_path, tmp_path / "out") == 1


class TestSignals:
    OPS = "org.springframework.kafka.core.KafkaOperations"
    TPL = "org.springframework.kafka.core.KafkaTemplate"

    def _spec(self, tmp_path: Path, signals: list[str]) -> Path:
        return write_spec(
            tmp_path / "s.json",
            base_spec(asserted={"Messaging": {"_signals": {"messaging__client_type": signals}}}),
        )

    def test_signals_exact_list_passes(self, tmp_path):
        write_csv(
            tmp_path / "out",
            "Messaging",
            [row("messaging__client_type", self.TPL), row("messaging__client_type", self.OPS)],
        )
        assert run(self._spec(tmp_path, [self.OPS, self.TPL]), tmp_path / "out") == 0

    def test_signals_wrong_survivor_fails_same_count(self, tmp_path):
        # Two rows either way: a count-only assertion could not tell.
        write_csv(
            tmp_path / "out",
            "Messaging",
            [row("messaging__client_type", self.TPL), row("messaging__client_type", self.TPL)],
        )
        assert run(self._spec(tmp_path, [self.OPS, self.TPL]), tmp_path / "out") == 1

    def test_signals_fanout_duplicate_fails(self, tmp_path):
        write_csv(
            tmp_path / "out",
            "Messaging",
            [row("messaging__client_type", self.OPS)] * 2
            + [row("messaging__client_type", self.TPL)],
        )
        assert run(self._spec(tmp_path, [self.OPS, self.TPL]), tmp_path / "out") == 1

    def test_signals_missing_rule_fails(self, tmp_path):
        write_csv(tmp_path / "out", "Messaging", [row("messaging__listener", "g")])
        assert run(self._spec(tmp_path, [self.OPS]), tmp_path / "out") == 1

    def test_signals_non_dict_rejected(self, tmp_path):
        write_csv(tmp_path / "out", "Messaging", [])
        spec_path = write_spec(
            tmp_path / "s.json",
            base_spec(asserted={"Messaging": {"_signals": [self.OPS]}}),
        )
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "out")


class TestKnownDefects:
    def test_defects_printed_never_asserted(self, tmp_path, capsys):
        write_csv(tmp_path / "out", "A", [])
        spec_path = write_spec(
            tmp_path / "s.json",
            {
                **base_spec(asserted={"A": {"_rows": 0}}),
                "known_defects": {"A.some_rule": "counts 2x upstream"},
            },
        )
        assert run(spec_path, tmp_path / "out") == 0
        assert "counts 2x upstream" in capsys.readouterr().out


class TestRecord:
    def test_record_refused_outside_harness(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")])
        spec_path = write_spec(tmp_path / "s.json", base_spec(snapshot={"A": {"_rows": 0}}))
        with pytest.raises(SystemExit):
            run(spec_path, tmp_path / "out", "--record")

    def _harness_spec(self, spec_obj: dict) -> Path:
        # record() confines writes to the harness directory by construction, so
        # the success-path tests must use a throwaway spec inside it.
        return write_spec(HARNESS_DIR / "expectations" / ".test-record-tmp.json", spec_obj)

    def test_record_writes_snapshot_and_keeps_asserted(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r1", "g")] * 4)
        spec_path = self._harness_spec(
            base_spec(asserted={"A": {"r1": 4}}, snapshot={"A": {"_rows": 0}})
        )
        try:
            assert run(spec_path, tmp_path / "out", "--record") == 0
            written = json.loads(spec_path.read_text(encoding="utf-8"))
            assert written["asserted"]["A"]["r1"] == 4
            # r1 is asserted, so the snapshot must not shadow it; _rows is not.
            assert written["snapshot"]["A"] == {"_rows": 4}
            assert not spec_path.with_suffix(".json.tmp").exists()
        finally:
            spec_path.unlink(missing_ok=True)

    def test_record_never_shadows_asserted(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r1", "g")] * 3)
        spec_path = self._harness_spec(base_spec(asserted={"A": {"r1": 99}}))
        try:
            assert run(spec_path, tmp_path / "out", "--record") == 0
            written = json.loads(spec_path.read_text(encoding="utf-8"))
            assert written["asserted"]["A"]["r1"] == 99
            assert "r1" not in written["snapshot"]["A"]
        finally:
            spec_path.unlink(missing_ok=True)

    def test_record_drops_stale_queries(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r1", "g")])
        spec_path = self._harness_spec(
            base_spec(snapshot={"A": {"_rows": 1}, "Ghost": {"_rows": 9}})
        )
        try:
            assert run(spec_path, tmp_path / "out", "--record") == 0
            written = json.loads(spec_path.read_text(encoding="utf-8"))
            assert "Ghost" not in written["snapshot"]
        finally:
            spec_path.unlink(missing_ok=True)


class TestRealExpectations:
    """The run.sh default wave and the shipped specs must agree on query names.

    run.sh emits one CSV per DEFAULT_QUERIES entry; check_no_stale_csvs exits 2
    on any CSV the spec does not name. A spec that names fewer queries than the
    default wave makes the default invocation un-runnable -- the exact failure
    this test exists to catch.
    """

    @staticmethod
    def _default_queries() -> list[str]:
        run_sh = (REPO_ROOT / "spring-signals" / "harness" / "run.sh").read_text(encoding="utf-8")
        m = re.search(r'^DEFAULT_QUERIES="([^"]+)"', run_sh, re.M)
        assert m, "run.sh no longer defines DEFAULT_QUERIES"
        return m.group(1).split()

    @pytest.mark.parametrize(
        "spec_name", ["ocs-api-service.json", "fixture-repo.json"]
    )
    def test_spec_names_every_default_wave_query(self, spec_name):
        spec_path = REPO_ROOT / "spring-signals" / "harness" / "expectations" / spec_name
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        named = ca.spec_queries(spec)
        missing = [q for q in self._default_queries() if q not in named]
        assert not missing, f"{spec_name} does not name default-wave queries: {missing}"


class TestEndToEnd:
    def test_subprocess_exit_codes(self, tmp_path):
        write_csv(tmp_path / "out", "A", [row("r", "g")] * 2)
        good = write_spec(tmp_path / "good.json", base_spec(asserted={"A": {"_rows": 2}}))
        bad = write_spec(tmp_path / "bad.json", base_spec(asserted={"A": {"_rows": 1}}))

        def invoke(spec_path: Path) -> int:
            return subprocess.run(
                [sys.executable, str(ENGINE_PATH), "--out", str(tmp_path / "out"),
                 "--expectations", str(spec_path)],
                capture_output=True,
                text=True,
            ).returncode

        assert invoke(good) == 0
        assert invoke(bad) == 1
        assert invoke(tmp_path / "absent.json") != 0
