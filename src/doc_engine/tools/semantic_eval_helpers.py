#!/usr/bin/env python3
"""Compatibility shim for the semantic-eval mechanical pre-pass.

Prefer ``doc_engine.tools.semantic_eval``. Public ``__all__`` only (COH4).

Run::

    python -m doc_engine.tools.semantic_eval_helpers <artifacts_dir>
"""

from __future__ import annotations

from doc_engine.tools.semantic_eval import *  # noqa: F403
from doc_engine.tools.semantic_eval import __all__ as __all__
from doc_engine.tools.semantic_eval import main

if __name__ == "__main__":
    main()
