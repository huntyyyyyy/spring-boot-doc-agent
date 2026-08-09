"""Gradle build-signal regex patterns."""

from __future__ import annotations

import re

# Gradle plugin declarations:
#   id 'org.springframework.boot' version '3.2.0'
#   id("org.springframework.boot") version "3.2.0"
#   apply plugin: 'org.springframework.boot'
#   plugins { id 'java' }
GRADLE_PLUGIN_RE = re.compile(
    r"(?:^|\s|\()id\s*(?:\(?\s*)['\"]([a-zA-Z0-9._\-]+)['\"]\s*\)?"
    r"(?:\s+version\s+['\"]([^'\"]+)['\"])?",
    re.MULTILINE,
)

# Same as the versioned branch above, but anchored on the trailing
# version clause so the optional version in GRADLE_PLUGIN_RE doesn't
# miss it when the id(...) form isn't used.
GRADLE_PLUGIN_VERSIONED_RE = re.compile(
    r"\bid\s*(?:\(?\s*)['\"]([a-zA-Z0-9._\-]+)['\"]\s*\)?\s+version\s+['\"]([^'\"]+)['\"]",
    re.MULTILINE,
)

# Gradle dependency declaration: configuration 'group:name:version' or configuration "group:name:version"
# Also captures "group:name" (version omitted) and "group:name:" (empty version).
# Configurations: implementation, api, compileOnly, runtimeOnly, testImplementation, etc.
GRADLE_DEPENDENCY_RE = re.compile(
    r"\b(implementation|api|compileOnly|runtimeOnly|testImplementation|"
    r"testCompileOnly|testRuntimeOnly|compile|runtime|provided|compileClasspath|"
    r"runtimeClasspath|testCompileClasspath|testRuntimeClasspath|annotationProcessor|"
    r"developmentOnly)\s*\(?\s*['\"]([a-zA-Z0-9._\-]+)(?:\:([a-zA-Z0-9._\-]*)(?:\:([a-zA-Z0-9._\-]+))?)?['\"]\s*\)?",
    re.MULTILINE,
)

# Gradle settings include: include 'module' or include(":module")
GRADLE_INCLUDE_RE = re.compile(
    r"\binclude\s*\(?\s*['\"]([a-zA-Z0-9._\-:]+)['\"]\s*\)?",
    re.MULTILINE,
)

# Gradle toolchain / Java version:
#   sourceCompatibility = '17'
#   sourceCompatibility = JavaVersion.VERSION_17
#   java.toolchain.languageVersion = JavaLanguageVersion.of(17)
#   org.gradle.java.home=/path (gradle.properties)
GRADLE_TOOLCHAIN_RE = re.compile(
    r"\b(sourceCompatibility|targetCompatibility)\s*=\s*(?:JavaVersion\.VERSION_)?(?:JavaLanguageVersion\.of\()?\s*['\"]?([0-9._]+)['\"]?\)?",
    re.MULTILINE,
)

GRADLE_BOOT_PLUGIN_RE = re.compile(
    r"id\s*\(?\s*['\"]org\.springframework\.boot['\"]\s*\)?\s+version\s+['\"]([^'\"]+)['\"]",
    re.MULTILINE,
)

# apply plugin: 'org.springframework.boot' does not follow the id(...) shape above.
GRADLE_APPLY_PLUGIN_RE = re.compile(
    r"apply\s+plugin\s*:\s*['\"]([a-zA-Z0-9._\-]+)['\"]",
    re.MULTILINE,
)
