#!/usr/bin/env python3
"""_build_signal_extract.py — deterministic, high-value facts from build scripts.

This module exists because ast-grep has no Groovy grammar, so a .gradle file
cannot be parsed structurally the way .java files are. The compromise is to
extract the small, stable, textually-present facts that docs need most:
plugins, dependency coordinates, Java/Spring Boot toolchain versions, and
multi-module includes. Dynamic Groovy (`project.ext`, custom DSLs, method
closures) is intentionally left out: a wrong coordinate is worse than no
coordinate.

Concept modules: ``_build_signal_text``, ``_build_signal_gradle``,
``_build_signal_maven``, ``_build_signal_catalog``. This façade keeps the
stable ``extract_build_signals`` import path (including climb-poked ``_`` aliases).

Supported files:
  - build.gradle / settings.gradle / *.gradle (Groovy DSL)
  - build.gradle.kts / settings.gradle.kts / *.gradle.kts (Kotlin DSL)
  - pom.xml (Maven)
  - libs.versions.toml (Gradle version catalog)

Usage:
    from doc_engine.scanning.support._build_signal_extract import extract_build_signals
"""

from __future__ import annotations

from typing import Dict, List

from doc_engine.scanning.support._build_signal_catalog import (
    catalog_library_row as _catalog_library_row,
)
from doc_engine.scanning.support._build_signal_catalog import (
    extract_version_catalog as _extract_version_catalog,
)
from doc_engine.scanning.support._build_signal_gradle import (
    extract_gradle as _extract_gradle,
)
from doc_engine.scanning.support._build_signal_maven import (
    extract_maven as _extract_maven,
)
from doc_engine.scanning.support._build_signal_text import (
    line_number as _line_number,
)
from doc_engine.scanning.support._build_signal_text import (
    read_text_compat as _read_text_compat,
)
from doc_engine.scanning.support._build_signal_text import (
    safe_match as _safe_match,
)
from doc_engine.scanning.support._build_signal_text import (
    strip_comments as _strip_comments,
)

_GRADLE_SUFFIXES = (".gradle", ".gradle.kts")


def extract_build_signals(rel: str, text: str) -> List[Dict[str, object]]:
    """Extract structured evidence from a build script or catalog file.

    Returns a list of evidence dicts in the same shape as the Java ast-grep
    pipeline: {file, line, match, rule_id, ...}. The caller decides which
    bucket to append to (deployment).
    """
    if not text:
        return []
    name = rel.rsplit("/", 1)[-1].lower()
    if name == "pom.xml":
        return _extract_maven(rel, text)
    if name == "libs.versions.toml":
        return _extract_version_catalog(rel, text)
    if name.endswith(_GRADLE_SUFFIXES):
        comment_free = _strip_comments(text)
        return _extract_gradle(rel, text, comment_free)
    return []


__all__ = [
    "extract_build_signals",
    "_catalog_library_row",
    "_extract_gradle",
    "_extract_maven",
    "_extract_version_catalog",
    "_line_number",
    "_read_text_compat",
    "_safe_match",
    "_strip_comments",
]
