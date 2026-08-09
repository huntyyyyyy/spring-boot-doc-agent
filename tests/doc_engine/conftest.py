"""Kitchen-sink fixtures for doc_engine chapter suites (E-KH1).

Fixtures live in ``tests.support.kitchen_sink.fixtures`` and are re-exported
here so pytest discovers them under ``tests/doc_engine/`` without nested
``pytest_plugins`` (unsupported; affects the whole suite).
"""

from __future__ import annotations

from tests.support.kitchen_sink.fixtures import (
    kitchen,
    kitchen_docs_scratch,
    kitchen_repo_copy,
)

__all__ = ["kitchen", "kitchen_docs_scratch", "kitchen_repo_copy"]
