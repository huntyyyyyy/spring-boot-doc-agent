"""Coverage climb B9: build_command win/empty; context until; uncertainty; code_dep.

Q2 adequacy witness: mutmut_slice on build_command, local_runner context,
uncertainty FULL_SUPPORT, and code_dep non-map/list/failure edges.
"""

from __future__ import annotations

import re
from types import SimpleNamespace

import pytest

from doc_engine.pipeline.local_runner_phases import context as ctx_mod
from doc_engine.scanning import build_command as bc
from doc_engine.scanning.gap_probe import code_dep as cd
from doc_engine.scanning.gap_probe import uncertainty as unc

pytestmark = pytest.mark.domain_climb_sensor

def test_canonicalize_tokens_win32(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bc.sys, "platform", "win32")
    monkeypatch.setattr(
        bc.subprocess, "list2cmdline", lambda tokens: "WIN:" + "|".join(tokens)
    )
    assert bc._canonicalize_tokens(["mvn", "clean"]) == "WIN:mvn|clean"

def test_validate_build_command_empty_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bc.shlex, "split", lambda *_a, **_k: [])
    with pytest.raises(bc.BuildCommandError, match="empty"):
        bc.validate_build_command("mvn")

def test_context_until_stage_log(monkeypatch: pytest.MonkeyPatch) -> None:
    logs: list[str] = []

    monkeypatch.setattr(ctx_mod, "_build_mock_executor", lambda log: None)
    monkeypatch.setattr(ctx_mod, "find_existing_readme", lambda *_a, **_k: None)
    monkeypatch.setattr(ctx_mod, "_partition_specs_by_kind", lambda specs: ([], []))
    monkeypatch.setattr(ctx_mod, "_record_reused_signal_scan", lambda state: None)
    monkeypatch.setattr(
        ctx_mod,
        "PipelineContext",
        lambda **k: SimpleNamespace(**k),
    )

    state = SimpleNamespace(
        repo_path="/r",
        out_dir="/o",
        manifest="/m",
        docs_dir="/d",
        py="python",
        today="2026-01-01",
        until_stage="signal_scan",
        skip_signal_scan=False,
        args=SimpleNamespace(respect_gitignore=False, max_tokens=1),
        log=lambda msg="": logs.append(msg),
    )
    monkeypatch.setattr(ctx_mod, "_select_specs_for_state", lambda state: 7)
    assert ctx_mod.phase_build_context(state) == 7
    monkeypatch.setattr(ctx_mod, "_select_specs_for_state", lambda state: [])
    assert ctx_mod.phase_build_context(state) is None
    assert any("until stage" in str(x) for x in logs)

def test_uncertainty_full_support() -> None:
    assert (
        unc._supported_claim(unscored_s3=False, imputed_axes=[])
        == unc.UncertaintyClaim.FULL_SUPPORT
    )

def test_code_dep_non_map_list_and_failure() -> None:
    assert cd._row_matches_pattern("nope", re.compile("x"), ("match",)) is False
    assert cd._bucket_keyword_hits("nope", re.compile("x")) == 0
    # deployment row that counts a family but no code keywords → failure append
    signals = {
        "evidence": {
            "deployment": [{"match": "spring-boot-starter-data-redis"}],
            "messaging": [],
            "outbound_clients": [],
            "observability": [],
            "security": [],
        }
    }
    out = cd.measure_r_code_dep(signals)
    assert out["failures"]
    assert any(f.get("stratum") == "redis" for f in out["failures"])
