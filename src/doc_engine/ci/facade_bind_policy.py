"""Climb/monkeypatch façade binds (E-REPO / E-FAC).

Lazy ``_facade()`` helpers in BC modules must return the *same module object*
tests ``monkeypatch.setattr`` / ``patch.object``. Binding a sibling shim
(e.g. ``semantic_eval_helpers`` while tests poke ``semantic_eval``) is a silent
false green: B7-style climbs pass attributes exist, but setattr never bites.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any

# (producer_module, facade_callable_name, expected_facade_module)
FACADE_BINDS: tuple[tuple[str, str, str], ...] = (
    (
        "doc_engine.semantic_eval.scan",
        "_facade",
        "doc_engine.tools.semantic_eval",
    ),
)


def resolve_facade(producer: str, attr: str) -> Any:
    mod = importlib.import_module(producer)
    fn = getattr(mod, attr, None)
    if not callable(fn):
        raise TypeError(f"{producer}.{attr} missing or not callable")
    return fn()


def facade_bind_errors(
    binds: tuple[tuple[str, str, str], ...] = FACADE_BINDS,
    *,
    resolver: Callable[[str, str], Any] = resolve_facade,
) -> list[str]:
    """Return human-readable mismatches (empty = green)."""
    errors: list[str] = []
    for producer, attr, expected_name in binds:
        expected = importlib.import_module(expected_name)
        try:
            got = resolver(producer, attr)
        except Exception as exc:  # noqa: BLE001 — surface any bind failure
            errors.append(f"{producer}.{attr}(): resolve failed: {exc}")
            continue
        if got is not expected:
            got_name = getattr(got, "__name__", type(got).__name__)
            errors.append(
                f"{producer}.{attr}() is {got_name!r}, want {expected_name!r} "
                "(monkeypatch on the expected façade would not reach join_under)"
            )
    return errors
