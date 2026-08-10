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


def normalize_plant(raw: Optional[str]) -> str:
    value = (raw or PLANT_FIXTURE).strip().lower() or PLANT_FIXTURE
    if value not in _VALID:
        raise ValueError(
            f"unknown plant {raw!r}; expected {sorted(_VALID)}"
        )
    return value


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
    env_paths: list[Optional[Path]] = []
    for key in (OCS_REPO_ENV, REAL_REPO_ENV):
        raw = os.environ.get(key, "").strip()
        env_paths.append(Path(raw) if raw else None)
    pointer = repo_root / REAL_REPO_PATH_FILE
    file_path: Optional[Path] = None
    if pointer.is_file():
        for line in pointer.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                file_path = Path(stripped)
                break
    return _first_existing([*env_paths, file_path])


def artifactory_present() -> bool:
    user = os.environ.get(ARTIFACTORY_USER_ENV, "").strip()
    password = os.environ.get(ARTIFACTORY_PASSWORD_ENV, "").strip()
    return bool(user and password)


def preflight(repo_root: Path, plant: Optional[str] = None) -> PlantPreflight:
    """Return readiness; ``ok`` is False when the plant cannot run honestly."""
    chosen = normalize_plant(
        plant if plant is not None else os.environ.get(PLANT_ENV)
    )
    if chosen == PLANT_FIXTURE:
        return PlantPreflight(
            plant=chosen,
            ok=True,
            reason="fixture plant — credential-free CI SoR",
            expectations_rel="harness/expectations/fixture-repo.json",
        )
    checkout = resolve_ocs_checkout(repo_root)
    has_arti = artifactory_present()
    if checkout is None:
        return PlantPreflight(
            plant=chosen,
            ok=False,
            reason=(
                "ocs plant needs a checkout: set DOC_ENGINE_REAL_REPO or "
                "SPRING_SIGNALS_OCS_REPO, or local-runs/real-repo.path"
            ),
            has_artifactory=has_arti,
            expectations_rel="harness/expectations/ocs-api-service.json",
        )
    if not has_arti:
        return PlantPreflight(
            plant=chosen,
            ok=False,
            reason=(
                "ocs CodeQL DB create needs artifactory_user + "
                "artifactory_password (work VPN). Checkout is present — "
                "use scripts/ci/remeasure_ocs_floors.py for offline floors."
            ),
            checkout=checkout,
            has_artifactory=False,
            expectations_rel="harness/expectations/ocs-api-service.json",
        )
    return PlantPreflight(
        plant=chosen,
        ok=True,
        reason="ocs plant ready (checkout + Artifactory)",
        checkout=checkout,
        has_artifactory=True,
        expectations_rel="harness/expectations/ocs-api-service.json",
    )


def main(argv: Optional[list[str]] = None) -> int:
    import argparse
    import json
    import sys

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
    if args.json:
        print(
            json.dumps(
                {
                    "plant": result.plant,
                    "ok": result.ok,
                    "reason": result.reason,
                    "checkout": str(result.checkout) if result.checkout else None,
                    "has_artifactory": result.has_artifactory,
                    "expectations_rel": result.expectations_rel,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        status = "ok" if result.ok else "blocked"
        print(f"plant={result.plant} status={status}")
        print(f"reason: {result.reason}")
        if result.checkout is not None:
            print(f"checkout: {result.checkout}")
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
