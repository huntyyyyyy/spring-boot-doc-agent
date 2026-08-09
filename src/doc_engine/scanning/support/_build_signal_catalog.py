"""Gradle libs.versions.toml catalog build-signal extraction."""

from __future__ import annotations

import re
from typing import Dict, List

from doc_engine.scanning.support._build_signal_text import capture_line, safe_match

# libs.versions.toml: [versions] spring-boot = "3.2.0"
# [libraries] spring-boot-starter = { module = "org.springframework.boot:spring-boot-starter", version.ref = "spring-boot" }
VERSION_CATALOG_VERSION_RE = re.compile(
    r"^\s*([a-zA-Z0-9.\-_]+)\s*=\s*['\"]([^'\"]+)['\"]\s*$",
    re.MULTILINE,
)
VERSION_CATALOG_LIBRARY_RE = re.compile(
    r"^\s*([a-zA-Z0-9.\-_]+)\s*=\s*\{\s*"
    r"(?:module\s*=\s*['\"]([a-zA-Z0-9._\-]+):([a-zA-Z0-9._\-]+)['\"]|"
    r"group\s*=\s*['\"]([a-zA-Z0-9._\-]+)['\"].*?name\s*=\s*['\"]([a-zA-Z0-9._\-]+)['\"])"
    r".*?\}\s*$",
    re.MULTILINE | re.DOTALL,
)


def catalog_version_row(rel: str, text: str, match: re.Match[str]) -> Dict[str, object]:
    line = capture_line(text, match)
    return {
        "file": rel,
        "line": line,
        "match": safe_match(text, line),
        "rule_id": "deployment__version_catalog",
        "catalog_kind": "version",
        "catalog_key": match.group(1),
        "catalog_value": match.group(2),
    }


def catalog_library_row(
    rel: str, text: str, match: re.Match[str],
) -> Dict[str, object] | None:
    group = match.group(2) or match.group(4)
    name = match.group(3) or match.group(5)
    if not (group and name):
        return None
    line = capture_line(text, match)
    return {
        "file": rel,
        "line": line,
        "match": safe_match(text, line),
        "rule_id": "deployment__version_catalog",
        "catalog_kind": "library",
        "catalog_key": match.group(1),
        "coordinate": {"group": group, "name": name},
    }


def extract_version_catalog(rel: str, text: str) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = [
        catalog_version_row(rel, text, match)
        for match in VERSION_CATALOG_VERSION_RE.finditer(text)
    ]
    for match in VERSION_CATALOG_LIBRARY_RE.finditer(text):
        row = catalog_library_row(rel, text, match)
        if row is not None:
            results.append(row)
    return results
