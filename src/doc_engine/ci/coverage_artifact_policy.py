"""Coverage artifact policy — oracle SoR vs climb sensor filenames (16-A).

Owns the boolean-safe naming contract: only ``coverage.xml`` is Cover% SoR;
climb writes ``coverage.climb.xml`` and must never feed gap inventory.
"""

from __future__ import annotations

from pathlib import Path

DEFAULT_FLOOR = 98.7
ORACLE_XML_NAME = "coverage.xml"
CLIMB_XML_NAME = "coverage.climb.xml"
CLIMB_BANNER = "mode=climb (not CI oracle)"


def is_climb_xml_path(path_name: str) -> bool:
    """True when *path_name* is the climb artifact basename."""
    return path_name.replace("\\", "/").rsplit("/", 1)[-1] == CLIMB_XML_NAME


def refuse_climb_as_gap_inventory(coverage_xml: Path) -> str | None:
    """Gap inventory binds oracle SoR only — refuse climb artifact."""
    if is_climb_xml_path(str(coverage_xml)):
        return (
            f"refusing climb artifact {CLIMB_XML_NAME} as gap inventory; "
            f"use cohesive {ORACLE_XML_NAME} (oracle SoR)"
        )
    return None
