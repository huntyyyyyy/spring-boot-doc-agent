"""Kitchen-sink Ch05 convergence + Ch07 lost-update."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from unittest import mock

import pytest
from doc_engine.tools import run_manifest

from tests.support.kitchen_sink.constants import (
    EMPTY_JAVA,
    EMPTY_SHA256,
    HUGE_JAVA,
    MAX_TOKENS,
    NUL_JAVA,
    PY,
    SMALL_FILE_BYTES,
)
from tests.support.kitchen_sink.harness import _evidence_files, _grouped, _run
from tests.support.kitchen_sink.testcase import KitchenBoundTestCase

pytestmark = pytest.mark.domain_integration


class Ch05ConvergenceTest(KitchenBoundTestCase):
    """signals.file_signatures, groups.json's file union, manifest
    .file_signatures and cross_group_edges' node set are four derived copies
    of one fact — the repo's file set — produced by three different walk
    implementations. Where they must converge, assert it; where they provably
    diverge, pin the divergence so it is a known trade-off rather than a
    surprise."""

    def test_manifest_signatures_are_the_scan_signatures(self):
        self.assertEqual(
            self.kitchen.manifest["file_signatures"],
            self.kitchen.signals["file_signatures"],
        )

    def test_empty_file_hashes_to_the_known_empty_digest(self):
        self.assertEqual(
            self.kitchen.signals["file_signatures"][EMPTY_JAVA], EMPTY_SHA256
        )

    def test_edge_nodes_are_a_subset_of_grouped_files(self):
        grouped = _grouped(self.kitchen.groups)
        referenced = set()
        for _gid, block in self.kitchen.edges["groups"].items():
            for arc in block.get("outbound", []) + block.get("inbound", []):
                for key in ("from", "to", "from_file", "to_file", "file"):
                    if isinstance(arc, dict) and isinstance(arc.get(key), str):
                        referenced.add(arc[key])
        self.assertEqual(referenced - grouped, set())

    def test_preflight_reuses_the_partition_rather_than_re_deriving_it(self):
        self.assertEqual(
            self.kitchen.preflight["num_groups"], self.kitchen.groups["num_groups"]
        )

    def test_nul_file_diverges_between_the_two_walkers(self):
        """Deterministic disagreement: partition skips it as binary, the scan
        still hashes it."""
        self.assertNotIn(NUL_JAVA, _grouped(self.kitchen.groups))
        self.assertIn(NUL_JAVA, self.kitchen.signals["file_signatures"])

    def test_a_file_can_be_cited_as_evidence_yet_belong_to_no_group(self):
        """The sharpest divergence, and the first CLI-level exercise of
        --max-file-bytes. partition_repo.py enforces a size ceiling;
        spring_signal_scan.py has none. So above the ceiling a file is
        citable evidence in the final documentation that no Stage-1 subagent
        will ever summarize, and nothing in the pipeline reconciles that."""
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "groups.json")
            proc = _run(
                [
                    PY,
                    "-m",
                    "doc_engine.tools.partition_repo",
                    self.kitchen.repo,
                    "--max-tokens",
                    MAX_TOKENS,
                    "--max-file-bytes",
                    SMALL_FILE_BYTES,
                    "--out",
                    out,
                ]
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            with open(out, encoding="utf-8") as f:
                small = json.load(f)
        skipped = {s["file"]: s["reason"] for s in small["skipped"]}
        self.assertIn(HUGE_JAVA, skipped)
        self.assertRegex(skipped[HUGE_JAVA], r"^too-large \(\d+ bytes\)$")
        self.assertNotIn(HUGE_JAVA, _grouped(small))
        self.assertIn(HUGE_JAVA, set(_evidence_files(self.kitchen.signals)))


class Ch07LostUpdateTest(KitchenBoundTestCase):

    def test_concurrent_read_modify_write_loses_an_update(self):
        """SKILL.md's concurrency contract — start-stage/end-stage exactly once
        per stage, orchestrating thread only — is load-bearing because this
        module has no locking, as its own docstring states. Demonstrated by
        replaying the forbidden interleaving deterministically rather than
        with threads: a racing test is a flaky test, and the interleaving is
        the point, not the race."""
        scratch = tempfile.mkdtemp(prefix="ks_lost_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "run_manifest.json")
        run_manifest._write_json_atomic(
            path, run_manifest.build_init_manifest(self.kitchen.repo)
        )

        a = run_manifest._read_json(path)
        b = run_manifest._read_json(path)
        run_manifest.start_stage(a, "architect")
        run_manifest._write_json_atomic(path, a)
        run_manifest.start_stage(b, "doc_writer")
        run_manifest._write_json_atomic(path, b)

        names = [s["name"] for s in run_manifest._read_json(path)["stages"]]
        self.assertEqual(names, ["doc_writer"])
        self.assertNotIn(
            "architect",
            names,
            "if this now passes, run_manifest.py grew locking and "
            "SKILL.md's concurrency contract can be relaxed",
        )

    def test_a_failed_write_leaves_the_previous_manifest_intact(self):
        """Temp file plus os.replace, so a crash mid-write cannot leave a
        half-written manifest for the next stage's json.load(). Deterministic:
        the failure is injected, not waited for."""
        scratch = tempfile.mkdtemp(prefix="ks_atomic_")
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        path = os.path.join(scratch, "run_manifest.json")
        run_manifest._write_json_atomic(
            path, run_manifest.build_init_manifest(self.kitchen.repo)
        )
        before = open(path, "rb").read()

        with mock.patch.object(
            run_manifest.json, "dump", side_effect=RuntimeError("disk full")
        ):
            with self.assertRaises(RuntimeError):
                run_manifest._write_json_atomic(path, {"stages": [{"name": "x"}]})

        self.assertEqual(open(path, "rb").read(), before)
        json.loads(before.decode("utf-8"))
        leftovers = [n for n in os.listdir(scratch) if n != "run_manifest.json"]
        self.assertEqual(leftovers, [], f"temp file left behind: {leftovers}")

    def test_the_real_run_honored_the_once_per_stage_contract(self):
        names = [s["name"] for s in self.kitchen.manifest["stages"]]
        self.assertEqual(
            sorted(names),
            sorted(
                [
                    "architect",
                    "doc_writer",
                    "file_summarize",
                    "gap_analysis_interview",
                    "partition",
                    "signal_scan",
                ]
            ),
        )
        self.assertEqual(len(names), len(set(names)))
        for stage in self.kitchen.manifest["stages"]:
            with self.subTest(stage=stage["name"]):
                self.assertEqual(stage["status"], "complete")

    def test_manifest_is_never_observed_half_written(self):
        snapshots = self.kitchen.snapshots
        self.assertGreater(len(snapshots), 10)
        for name, data in snapshots:
            self.assertIn("stages", data, f"manifest malformed after {name}")
