"""Gradle DSL build-signal extraction (plugins, deps, modules, toolchains)."""

from __future__ import annotations

from typing import Dict, List

from doc_engine.scanning.support._build_signal_gradle_patterns import (
    GRADLE_APPLY_PLUGIN_RE,
    GRADLE_BOOT_PLUGIN_RE,
    GRADLE_DEPENDENCY_RE,
    GRADLE_INCLUDE_RE,
    GRADLE_PLUGIN_RE,
    GRADLE_PLUGIN_VERSIONED_RE,
    GRADLE_TOOLCHAIN_RE,
)
from doc_engine.scanning.support._build_signal_text import capture_line, safe_match


def gradle_row(
    rel: str,
    text: str,
    match: re.Match[str],
    *,
    rule_id: str,
    **extra: object,
) -> Dict[str, object]:
    line = capture_line(text, match)
    row: Dict[str, object] = {
        "file": rel,
        "line": line,
        "match": safe_match(text, line),
        "rule_id": rule_id,
    }
    row.update(extra)
    return row


def gradle_versioned_plugins(
    rel: str, text: str, comment_free: str,
) -> Dict[int, Dict[str, object]]:
    versioned_by_start: Dict[int, Dict[str, object]] = {}
    for match in GRADLE_PLUGIN_VERSIONED_RE.finditer(comment_free):
        versioned_by_start[match.start(1)] = gradle_row(
            rel,
            text,
            match,
            rule_id="deployment__build_plugin",
            plugin_id=match.group(1),
            plugin_version=match.group(2),
        )
    return versioned_by_start


def gradle_dependency_coordinate(match: re.Match[str]) -> Dict[str, str]:
    coordinate = {"group": match.group(2)}
    if match.group(3):
        coordinate["name"] = match.group(3)
    if match.group(4):
        coordinate["version"] = match.group(4)
    return coordinate


def append_bare_gradle_plugins(
    results: List[Dict[str, object]],
    *,
    rel: str,
    text: str,
    comment_free: str,
    versioned_by_start: Dict[int, Dict[str, object]],
) -> None:
    for match in GRADLE_PLUGIN_RE.finditer(comment_free):
        if match.start(1) in versioned_by_start:
            continue
        results.append(
            gradle_row(
                rel,
                text,
                match,
                rule_id="deployment__build_plugin",
                plugin_id=match.group(1),
                plugin_version=match.group(2) or None,
            )
        )


def append_gradle_apply_plugins(
    results: List[Dict[str, object]],
    *,
    rel: str,
    text: str,
    comment_free: str,
) -> None:
    for match in GRADLE_APPLY_PLUGIN_RE.finditer(comment_free):
        results.append(
            gradle_row(
                rel,
                text,
                match,
                rule_id="deployment__build_plugin",
                plugin_id=match.group(1),
                plugin_version=None,
            )
        )


def append_gradle_dependencies(
    results: List[Dict[str, object]],
    *,
    rel: str,
    text: str,
    comment_free: str,
) -> None:
    for match in GRADLE_DEPENDENCY_RE.finditer(comment_free):
        results.append(
            gradle_row(
                rel,
                text,
                match,
                rule_id="deployment__build_dependency",
                configuration=match.group(1),
                coordinate=gradle_dependency_coordinate(match),
            )
        )


def append_gradle_modules_and_toolchains(
    results: List[Dict[str, object]],
    *,
    rel: str,
    text: str,
    comment_free: str,
) -> None:
    for match in GRADLE_INCLUDE_RE.finditer(comment_free):
        results.append(
            gradle_row(
                rel,
                text,
                match,
                rule_id="deployment__build_module",
                module=match.group(1).lstrip(":"),
            )
        )
    for match in GRADLE_TOOLCHAIN_RE.finditer(comment_free):
        results.append(
            gradle_row(
                rel,
                text,
                match,
                rule_id="deployment__build_toolchain",
                toolchain_kind=match.group(1),
                toolchain_value=match.group(2),
            )
        )


def extract_gradle(rel: str, text: str, comment_free: str) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = []
    # Collect all versioned plugin ids first, then skip the bare id
    # matches that would otherwise duplicate them. We key by the position of
    # the id keyword, which is the same start position both regexes use, so
    # the bare id match for a versioned plugin is detected and suppressed.
    versioned_by_start = gradle_versioned_plugins(rel, text, comment_free)
    results.extend(versioned_by_start.values())
    append_bare_gradle_plugins(
        results,
        rel=rel,
        text=text,
        comment_free=comment_free,
        versioned_by_start=versioned_by_start,
    )
    append_gradle_apply_plugins(
        results, rel=rel, text=text, comment_free=comment_free,
    )
    append_gradle_dependencies(
        results, rel=rel, text=text, comment_free=comment_free,
    )
    append_gradle_modules_and_toolchains(
        results, rel=rel, text=text, comment_free=comment_free,
    )
    return results
