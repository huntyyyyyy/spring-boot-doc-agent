"""Assert certified local_runner mock end-to-end outputs for kitchen-sink."""

from __future__ import annotations

import json
import os

from doc_engine.scanning.covering import verify_covering_proof


def assert_local_runner_exit_and_banner(test_case, proc) -> None:
    test_case.assertEqual(
        proc.returncode, 0, proc.stdout[-4000:] + proc.stderr[-2000:]
    )
    test_case.assertIn("RESULT: every gate passed", proc.stdout)


def assert_mock_certification(test_case, run_dir: str) -> dict:
    cert_path = os.path.join(run_dir, "certification.json")
    test_case.assertTrue(os.path.isfile(cert_path))
    with open(cert_path, encoding="utf-8") as handle:
        cert = json.load(handle)
    test_case.assertTrue(
        cert.get("certified"),
        f"expected certified under --allow-mock; failures={cert.get('failures')}",
    )
    test_case.assertEqual(cert.get("generative_executor"), "mock")
    return cert


def assert_covering_proof_matches_signals(test_case, run_dir: str) -> None:
    covering = os.path.join(run_dir, "covering_proof.json")
    signals_path = os.path.join(run_dir, "spring_signals.json")
    test_case.assertTrue(
        os.path.isfile(covering), "local_runner missing covering_proof.json"
    )
    with open(signals_path, encoding="utf-8") as handle:
        signals = json.load(handle)
    with open(covering, encoding="utf-8") as handle:
        proof = json.load(handle)
    test_case.assertNotIn("_covering_proof", signals)
    ok, why = verify_covering_proof(
        proof,
        file_signatures=signals["file_signatures"],
        scanner_version=signals["scanner_version"],
    )
    test_case.assertTrue(ok, why)
