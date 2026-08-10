"""Resolve spring-signals plant (fixture | ocs) and fail-closed preflight.

Fixture is the CI/merge CodeQL SoR. OCS is campaign/opt-in and needs a local
checkout; Artifactory credentials are required only for traced DB create.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

PLANT_ENV = "SPRING_SIGNALS_PLANT"
OCS_REPO_ENV = "SPRING_SIGNALS_OCS_REPO"
# Same pointer as Stage-0 real-repo lane (never commit the path).
REAL_REPO_ENV = "DOC_ENGINE_REAL_REPO"
REAL_REPO_PATH_FILE = Path("local-runs") / "real-repo.path"

ARTIFACTORY_USER_ENV = "artifactory_user"
ARTIFACTORY_PASSWORD_ENV = "artifactory_password"

PLANT_FIXTURE = "fixture"
PLANT_OCS = "ocs"
_VALID = frozenset({PLANT_FIXTURE, PLANT_OCS})


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


def _env_checkout_paths() -> list[Path]:
    out: list[Path] = []
    for key in (OCS_REPO_ENV, REAL_REPO_ENV):
        raw = os.environ.get(key, "").strip()
        if raw:
            out.append(Path(raw))
    return out


def _pointer_checkout_path(repo_root: Path) -> Optional[Path]:
    pointer = repo_root / REAL_REPO_PATH_FILE
    if not pointer.is_file():
        return None
    for line in pointer.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return Path(stripped)
    return None


def _candidate_paths(repo_root: Path) -> list[Path]:
    """Configured OCS checkout paths (env first, then gitignored pointer)."""
    out = _env_checkout_paths()
    pointed = _pointer_checkout_path(repo_root)
    if pointed is not None:
        out.append(pointed)
    return out


def _first_existing(candidates: list[Optional[Path]]) -> Optional[Path]:
    for path in candidates:
        if path is None:
            continue
        resolved = path.expanduser()
        if resolved.is_dir():
            return resolved.resolve()
    return None


def resolve_ocs_checkout(repo_root: Path) -> Optional[Path]:
    """Env wins, then gitignored pointer file (same doctrine as real_fixture)."""
    return _first_existing(list(_candidate_paths(repo_root)))


def _missing_checkout_reason(repo_root: Path) -> str:
    configured = _candidate_paths(repo_root)
    if not configured:
        return (
            "ocs plant needs a checkout: set DOC_ENGINE_REAL_REPO or "
            "SPRING_SIGNALS_OCS_REPO, or local-runs/real-repo.path"
        )
    shown = ", ".join(repr(str(path)) for path in configured)
    return (
        "ocs plant checkout configured but not a directory on this machine: "
        f"{shown} — fix the path, or sync the tree onto this host"
    )


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
            reason=_missing_checkout_reason(repo_root),
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
