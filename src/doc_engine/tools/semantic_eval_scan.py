#!/usr/bin/env python3
"""Shim — scan/CLI live in ``doc_engine.semantic_eval.scan``."""

from __future__ import annotations

from doc_engine.semantic_eval.scan import *  # noqa: F403
from doc_engine.semantic_eval.scan import (  # noqa: F401
    confirmed_findings_for_doc,
    is_safe_markdown_basename,
    load_interview_answers,
    main,
    markdown_names,
    resolve_architecture_path,
    run,
    scan_confirmed_docs,
    scan_mermaid,
)

if __name__ == "__main__":
    main()
