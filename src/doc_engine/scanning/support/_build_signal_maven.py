"""Maven pom.xml build-signal extraction (plugins and dependencies)."""

from __future__ import annotations

import re
from typing import Dict, List

from doc_engine.scanning.support._build_signal_text import capture_line, safe_match

# Maven dependency: <dependency> ... <groupId>g</groupId> <artifactId>a</artifactId> <version>v</version> ... </dependency>
MAVEN_DEPENDENCY_RE = re.compile(
    r"<dependency>\s*"
    r"<groupId>([^<]+)</groupId>\s*"
    r"<artifactId>([^<]+)</artifactId>"
    r"(?:\s*<version>([^<]*)</version>)?"
    r"(?:\s*<scope>([^<]+)</scope>)?"
    r".*?"
    r"</dependency>",
    re.DOTALL,
)

# Maven plugin: <plugin> ... <groupId> ... <artifactId> ... <version> ... </plugin>
MAVEN_PLUGIN_RE = re.compile(
    r"<plugin>\s*"
    r"(?:<groupId>([^<]+)</groupId>\s*)?"
    r"<artifactId>([^<]+)</artifactId>"
    r"(?:\s*<version>([^<]*)</version>)?"
    r".*?"
    r"</plugin>",
    re.DOTALL,
)


def maven_plugin_row(rel: str, text: str, match: re.Match[str]) -> Dict[str, object]:
    line = capture_line(text, match)
    group = match.group(1) or "org.apache.maven.plugins"
    return {
        "file": rel,
        "line": line,
        "match": safe_match(text, line),
        "rule_id": "deployment__build_plugin",
        "plugin_id": f"{group}:{match.group(2)}",
        "plugin_version": match.group(3) or None,
    }


def maven_dependency_row(rel: str, text: str, match: re.Match[str]) -> Dict[str, object]:
    line = capture_line(text, match)
    coordinate = {"group": match.group(1), "name": match.group(2)}
    if match.group(3):
        coordinate["version"] = match.group(3)
    return {
        "file": rel,
        "line": line,
        "match": safe_match(text, line),
        "rule_id": "deployment__build_dependency",
        "configuration": match.group(4) or "compile",
        "coordinate": coordinate,
    }


def extract_maven(rel: str, text: str) -> List[Dict[str, object]]:
    results: List[Dict[str, object]] = [
        maven_plugin_row(rel, text, match)
        for match in MAVEN_PLUGIN_RE.finditer(text)
    ]
    results.extend(
        maven_dependency_row(rel, text, match)
        for match in MAVEN_DEPENDENCY_RE.finditer(text)
    )
    return results
