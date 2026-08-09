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
stable ``extract_build_signals`` import path.

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
    VERSION_CATALOG_LIBRARY_RE,
    VERSION_CATALOG_VERSION_RE,
    catalog_library_row as _catalog_library_row,
    catalog_version_row as _catalog_version_row,
    extract_version_catalog as _extract_version_catalog,
)
from doc_engine.scanning.support._build_signal_gradle import (
    GRADLE_APPLY_PLUGIN_RE,
    GRADLE_BOOT_PLUGIN_RE,
    GRADLE_DEPENDENCY_RE,
    GRADLE_INCLUDE_RE,
    GRADLE_PLUGIN_RE,
    GRADLE_PLUGIN_VERSIONED_RE,
    GRADLE_TOOLCHAIN_RE,
    append_bare_gradle_plugins as _append_bare_gradle_plugins,
    append_gradle_apply_plugins as _append_gradle_apply_plugins,
    append_gradle_dependencies as _append_gradle_dependencies,
    append_gradle_modules_and_toolchains as _append_gradle_modules_and_toolchains,
    extract_gradle as _extract_gradle,
    gradle_dependency_coordinate as _gradle_dependency_coordinate,
    gradle_row as _gradle_row,
    gradle_versioned_plugins as _gradle_versioned_plugins,
)
from doc_engine.scanning.support._build_signal_maven import (
    MAVEN_DEPENDENCY_RE,
    MAVEN_PLUGIN_RE,
    extract_maven as _extract_maven,
    maven_dependency_row as _maven_dependency_row,
    maven_plugin_row as _maven_plugin_row,
)
from doc_engine.scanning.support._build_signal_text import (
    capture_line as _capture_line,
    line_number as _line_number,
    read_text_compat as _read_text_compat,
    safe_match as _safe_match,
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
