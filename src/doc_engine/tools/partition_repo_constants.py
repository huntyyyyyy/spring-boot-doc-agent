"""Token / exclude constants for adaptive DFS partition grouping."""

from __future__ import annotations

DEFAULT_EXCLUDED_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp",
    ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar", ".jar", ".war", ".class",
    ".so", ".dll", ".dylib", ".exe", ".bin", ".woff", ".woff2", ".ttf",
    ".eot", ".mp3", ".mp4", ".mov", ".avi", ".lock",
}

DEFAULT_EXCLUDED_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Gemfile.lock",
    "poetry.lock", "Cargo.lock", "composer.lock",
}

# Chars-per-token divisors, calibrated against a real BPE tokenizer
# (tiktoken's cl100k_base — used only offline to pick these constants, not
# a runtime dependency of this script) run against real and synthetic Java,
# Python, YAML, JSON, and .properties files.
CHARS_PER_TOKEN_DEFAULT = 4
CHARS_PER_TOKEN_DENSE = 3
DENSE_EXTS = {".yml", ".yaml", ".json", ".properties", ".xml", ".toml"}
