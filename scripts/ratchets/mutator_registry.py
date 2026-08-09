"""OCP registry for gate mutators — harness stays closed to catalog churn.

Open for extension: append an incident-seeded ``Mutator`` in
``gate_mutators.definitions`` (or register an extra source via
``register_source``). Closed for modification: ``mutate.py`` only calls
``load_registry`` / ``all_mutators`` and never inlines operator lists.

Not a mega-registry. Formatting perturbations (``java_perturbations.py``) and
assertion-engine mutants (``tests/spring_signals/mutation_driver.py``) keep
their own oracles and must not be folded in. See CONTRIBUTING.md
“Mutation-scope taxonomies.”
"""
from __future__ import annotations

from typing import Callable, List, Tuple

from gate_mutators import definitions
from mutator import Mutator

Source = Callable[[], Tuple[Mutator, ...]]

_SOURCES: List[Source] = [definitions]
_CACHE: Tuple[Mutator, ...] | None = None


def register_source(source: Source) -> None:
    """Append an extra definition source (tests / future incident packs)."""
    global _CACHE
    _SOURCES.append(source)
    _CACHE = None


def clear_sources() -> None:
    """Reset to the default catalog source only (test isolation)."""
    global _CACHE
    _SOURCES.clear()
    _SOURCES.append(definitions)
    _CACHE = None


def _validate(mutators: Tuple[Mutator, ...]) -> None:
    names = [m.name for m in mutators]
    if len(names) != len(set(names)):
        dupes = sorted({n for n in names if names.count(n) > 1})
        raise ValueError(f"duplicate gate mutator names: {dupes}")
    for m in mutators:
        if len(m.why.strip()) < 20:
            raise ValueError(f"{m.name}: why must name an incident class")
        if not m.expected_caught_by.strip():
            raise ValueError(f"{m.name}: expected_caught_by is required")


def load_registry() -> Tuple[Mutator, ...]:
    """Load and validate every registered definition source once."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    collected: List[Mutator] = []
    for source in _SOURCES:
        collected.extend(source())
    mutators = tuple(collected)
    _validate(mutators)
    _CACHE = mutators
    return mutators


def all_mutators() -> Tuple[Mutator, ...]:
    """Public catalog snapshot used by the kill harness and tests."""
    return load_registry()


def known_names() -> frozenset[str]:
    """Stable name set for registry-contract tests."""
    return frozenset(m.name for m in load_registry())
