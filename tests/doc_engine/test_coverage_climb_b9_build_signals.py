"""Coverage climb B9: build_signal_extract helper / empty / catalog None.

Q2 adequacy witness: mutmut_slice on scanning.support._build_signal_extract —
asserts bite newline normalize, line_number, safe_match OOB, catalog None, empty.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from doc_engine.scanning.support import _build_signal_extract as bse

pytestmark = pytest.mark.domain_climb_sensor

def test_read_text_compat_and_line_number() -> None:
    assert bse._read_text_compat("hi") == "hi\n"
    assert bse._read_text_compat("hi\n") == "hi\n"
    assert bse._line_number("a\nb\nc", 3) == 2

def test_safe_match_out_of_range() -> None:
    assert bse._safe_match("one\ntwo", 99) == ""

def test_catalog_library_row_none_and_empty_extract() -> None:
    match = SimpleNamespace(
        group=lambda i: None,
        start=lambda: 0,
    )
    assert bse._catalog_library_row("libs.versions.toml", "x", match) is None
    assert bse.extract_build_signals("x.unknown", "") == []
    assert bse.extract_build_signals("readme.md", "hello") == []
