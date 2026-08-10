"""Resolve spring-signals plant (fixture | ocs) and fail-closed preflight.

Fixture is the CI/merge CodeQL SoR. OCS is campaign/opt-in and needs a local
checkout; Artifactory credentials are required only for traced DB create.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from plant_checkout import missing_checkout_reason, resolve_ocs_checkout

PLANT_ENV = "SPRING_SIGNALS_PLANT"
ARTIFACTORY_USER_ENV = "artifactory_user"
ARTIFACTORY_PASSWORD_ENV = "artifactory_password"

PLANT_FIXTURE = "fixture"
PLANT_OCS = "ocs"
_VALID = frozenset({PLANT_FIXTURE, PLANT_OCS})

# Re-export for callers that imported resolve from this module.
__all__ = (
    "PLANT_ENV",
    "PLANT_FIXTURE",
    "PLANT_OCS",
    "PlantPreflight",
    "artifactory_present",
    "exit_code_for",
    "main",
    "normalize_plant",
    "preflight",
    "resolve_ocs_checkout",
)


@dataclass(frozen=True)
class PlantPreflight:
    """Readiness for one plant invocation."""

    plant: str
    ok: bool
    reason: str
    checkout: Optional[Path] = None
    has_artifactory: bool = False
    expectations_rel: str = ""
    # True when checkout resolves — enough for ast-grep floor remeasure (OCS6).
    remeasure_ok: bool = False


def normalize_plant(raw: Optional[str]) -> str:
    value = (raw or PLANT_FIXTURE).strip().lower() or PLANT_FIXTURE
    if value not in _VALID:
        raise ValueError(
            f"unknown plant {raw!r}; expected {sorted(_VALID)}"
        )
    return value


def artifactory_present() -> bool:
    user = os.environ.get(ARTIFACTORY_USER_ENV, "").strip()
    password = os.environ.get(ARTIFACTORY_PASSWORD_ENV, "").strip()
    return bool(user and password)


def preflight(repo_root: Path, plant: Optional[str] = None) -> PlantPreflight:
    """Return readiness; ``ok`` is False when the *full* plant cannot run honestly.

    Missing Artifactory with a resolvable checkout sets ``remeasure_ok=True`` and
    is exit code 3 from ``main`` — offline floors may proceed; create-db must not.
    """
    chosen = normalize_plant(
        plant if plant is not None else os.environ.get(PLANT_ENV)
    )
    if chosen == PLANT_FIXTURE:
        return PlantPreflight(
            plant=chosen,
            ok=True,
            reason="fixture plant — credential-free CI SoR",
            expectations_rel="harness/expectations/fixture-repo.json",
            remeasure_ok=False,
        )
    checkout = resolve_ocs_checkout(repo_root)
    has_arti = artifactory_present()
    if checkout is None:
        return PlantPreflight(
            plant=chosen,
            ok=False,
            reason=missing_checkout_reason(repo_root),
            has_artifactory=has_arti,
            expectations_rel="harness/expectations/ocs-api-service.json",
            remeasure_ok=False,
        )
    if not has_arti:
        return PlantPreflight(
            plant=chosen,
            ok=False,
            reason=(
                "run-plant/create-db need artifactory_user + "
                "artifactory_password (VPN). Checkout OK for offline "
                "floors — next: python scripts/ci/remeasure_ocs_floors.py "
                "(this script exits 3)."
            ),
            checkout=checkout,
            has_artifactory=False,
            expectations_rel="harness/expectations/ocs-api-service.json",
            remeasure_ok=True,
        )
    return PlantPreflight(
        plant=chosen,
        ok=True,
        reason="ocs plant ready (checkout + Artifactory)",
        checkout=checkout,
        has_artifactory=True,
        expectations_rel="harness/expectations/ocs-api-service.json",
        remeasure_ok=True,
    )


def exit_code_for(result: PlantPreflight) -> int:
    """0 = full plant ok; 2 = no checkout; 3 = checkout ok, Artifactory missing."""
    if result.ok:
        return 0
    if result.remeasure_ok:
        return 3
    return 2


def _status_label(result: PlantPreflight) -> str:
    if result.ok:
        return "ok"
    if result.remeasure_ok:
        return "offline_floors_ok"
    return "blocked"


def _emit_json(result: PlantPreflight) -> None:
    import json

    print(
        json.dumps(
            {
                "plant": result.plant,
                "ok": result.ok,
                "remeasure_ok": result.remeasure_ok,
                "reason": result.reason,
                "checkout": str(result.checkout) if result.checkout else None,
                "has_artifactory": result.has_artifactory,
                "expectations_rel": result.expectations_rel,
                "exit_code": exit_code_for(result),
            },
            indent=2,
            sort_keys=True,
        )
    )


def _emit_text(result: PlantPreflight) -> None:
    print(f"plant={result.plant} status={_status_label(result)}")
    print(f"reason: {result.reason}")
    if result.checkout is not None:
        print(f"checkout: {result.checkout}")
    if result.remeasure_ok and not result.ok:
        print("next: python scripts/ci/remeasure_ocs_floors.py")


def _emit_result(result: PlantPreflight, *, as_json: bool) -> None:
    if as_json:
        _emit_json(result)
    else:
        _emit_text(result)


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plant", default=None)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = preflight(args.root.resolve(), args.plant)
    _emit_result(result, as_json=args.json)
    return exit_code_for(result)


if __name__ == "__main__":
    raise SystemExit(main())
