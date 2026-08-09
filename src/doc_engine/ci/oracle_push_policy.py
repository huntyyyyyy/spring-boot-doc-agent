"""When local pre_pr must remesure the oracle Cover% floor (E-HOOK2).

Remote CI 3.11 writes ``coverage.xml`` with ``fail_under=98.7``. Local push
must evaluate the same predicate when package/test trees change — not domain
select alone.
"""

from __future__ import annotations

import os
from typing import Iterable

ORACLE_PATH_PREFIXES: tuple[str, ...] = (
    "src/doc_engine/",
    "src/stf/",
    "tests/",
)


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes")


def path_triggers_oracle(path: str) -> bool:
    """Return True when *path* can change whole-repo Cover%."""
    norm = path.replace("\\", "/").lstrip("./")
    return any(
        norm == prefix.rstrip("/") or norm.startswith(prefix)
        for prefix in ORACLE_PATH_PREFIXES
    )


def should_remesure_oracle(mode: str, changed_paths: Iterable[str]) -> bool:
    """Decide whether pre_pr must run oracle coverage-measure."""
    if _env_flag("PRE_PR_SKIP_ORACLE"):
        return False
    if _env_flag("PRE_PR_FORCE_ORACLE"):
        return True
    if mode in ("full", "actions_outage"):
        return True
    if mode == "fast":
        return False
    return any(path_triggers_oracle(path) for path in changed_paths)
