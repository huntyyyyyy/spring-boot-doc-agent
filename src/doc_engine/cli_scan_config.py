"""Scan CLI → Config override mapping for ``doc-engine scan``."""

from __future__ import annotations

import argparse
from typing import Any, Dict

from doc_engine.config import (
    Config,
    load_repo_config,
    merge_config,
    sanitize_repo_settings,
    trust_from_flag,
)


def split_scanner_names(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def apply_optional_scan_flags(
    args: argparse.Namespace, overrides: Dict[str, Any]
) -> None:
    if args.respect_gitignore:
        overrides["respect_gitignore"] = True
    if args.build_command:
        overrides["build_command"] = args.build_command
    if args.db_path:
        overrides["db_path"] = args.db_path


def scan_cli_overrides(args: argparse.Namespace) -> Dict[str, Any]:
    """Map scan CLI flags onto Config override keys."""
    overrides: Dict[str, Any] = {}
    if args.scanners:
        overrides["scanners"] = split_scanner_names(args.scanners)
    if args.sql_dialect != "ansi":
        overrides["sql_dialect"] = args.sql_dialect
    apply_optional_scan_flags(args, overrides)
    return overrides


def scan_config(repo: str, args: argparse.Namespace) -> Config:
    trust = trust_from_flag(bool(getattr(args, "trust_repo_config", False)))
    base = sanitize_repo_settings(load_repo_config(repo) or Config(), trust) or Config()
    return merge_config(base, scan_cli_overrides(args))
