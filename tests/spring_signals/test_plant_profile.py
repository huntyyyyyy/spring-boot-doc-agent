"""OCS plant preflight — fixture SoR; checkout fail-closed with clear reasons."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_HARNESS = Path(__file__).resolve().parents[2] / "spring-signals" / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))

from plant_profile import (  # noqa: E402
    PLANT_FIXTURE,
    PLANT_OCS,
    preflight,
    resolve_ocs_checkout,
)

pytestmark = pytest.mark.domain_stage0


def test_fixture_plant_always_ok(tmp_path: Path) -> None:
    result = preflight(tmp_path, PLANT_FIXTURE)
    assert result.ok
    assert result.plant == PLANT_FIXTURE


def test_ocs_without_pointer_explains_how_to_configure(tmp_path: Path) -> None:
    result = preflight(tmp_path, PLANT_OCS)
    assert not result.ok
    assert "local-runs/real-repo.path" in result.reason
    assert resolve_ocs_checkout(tmp_path) is None


def test_ocs_pointer_missing_dir_is_explicit(tmp_path: Path) -> None:
    pointer = tmp_path / "local-runs" / "real-repo.path"
    pointer.parent.mkdir(parents=True)
    missing = tmp_path / "not-a-checkout"
    pointer.write_text(str(missing) + "\n", encoding="utf-8")
    result = preflight(tmp_path, PLANT_OCS)
    assert not result.ok
    assert "configured but not a directory" in result.reason
    assert str(missing) in result.reason


def test_ocs_checkout_present_without_artifactory_blocks_db(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("artifactory_user", raising=False)
    monkeypatch.delenv("artifactory_password", raising=False)
    checkout = tmp_path / "client-tree"
    checkout.mkdir()
    pointer = tmp_path / "local-runs" / "real-repo.path"
    pointer.parent.mkdir(parents=True)
    pointer.write_text(str(checkout) + "\n", encoding="utf-8")
    result = preflight(tmp_path, PLANT_OCS)
    assert not result.ok
    assert result.remeasure_ok
    assert result.checkout == checkout.resolve()
    assert "artifactory" in result.reason.lower()
    assert "remeasure_ocs_floors" in result.reason
    from plant_profile import exit_code_for, main

    assert exit_code_for(result) == 3
    assert main(["--root", str(tmp_path), "--plant", "ocs"]) == 3
