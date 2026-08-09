"""Ports for E-MOD3 tools wave 2 (run_manifest / citation_coverage).

Filename prefix ``test_pipeline_`` keeps this module classifier-aligned with
``domain_pipeline`` (see ``test_domain_rules.FilenamePrefixRule``).
"""

from __future__ import annotations

import pytest

from doc_engine.tools.citation_coverage_ports import CitationCoveragePort
from doc_engine.tools.citation_coverage_report import check_docs, total_findings
from doc_engine.tools.run_manifest_finalize import finalize_manifest
from doc_engine.tools.run_manifest_ports import (
    RunManifestLifecycle,
    RunManifestStore,
    default_manifest_store,
)
from doc_engine.tools.run_manifest_stages import (
    build_init_manifest,
    end_stage,
    start_stage,
)

pytestmark = [
    pytest.mark.domain_pipeline,
]


def test_run_manifest_store_port_roundtrip(tmp_path) -> None:
    store: RunManifestStore = default_manifest_store()
    path = str(tmp_path / "m.json")
    data = {"run_id": "x", "status": "running", "stages": []}
    store.write(path, data)
    loaded = store.load(path)
    assert loaded["run_id"] == "x"


def test_run_manifest_lifecycle_protocol_surface() -> None:
    class _Adapter:
        build_init_manifest = staticmethod(build_init_manifest)
        start_stage = staticmethod(start_stage)
        end_stage = staticmethod(end_stage)
        finalize_manifest = staticmethod(finalize_manifest)

    lifecycle: RunManifestLifecycle = _Adapter()
    m = lifecycle.build_init_manifest(".", now_ms=1)
    lifecycle.start_stage(m, "scan", now_ms=2)
    lifecycle.end_stage(m, "scan", "complete", now_ms=3)
    finalized, _ = lifecycle.finalize_manifest(m, now_ms=4)
    assert finalized["status"] == "complete"


def test_citation_coverage_port_surface(tmp_path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "readme.md").write_text("Hello.\n", encoding="utf-8")

    class _Adapter:
        check_docs = staticmethod(check_docs)
        total_findings = staticmethod(total_findings)

    port: CitationCoveragePort = _Adapter()
    report = port.check_docs(str(docs), None)
    assert port.total_findings(report) == 0
