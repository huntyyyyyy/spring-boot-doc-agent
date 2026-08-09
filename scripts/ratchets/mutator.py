"""Gate-mutator type and locate/apply (artifact-aware; not PIT operators).

This module owns the *shape* of a gate mutator and how it finds/rewrites an
anchor. Catalog entries live in ``gate_mutators.py``; the OCP registry that
loads them is ``mutator_registry.py``; the sandboxed kill harness is
``mutate.py``.

Not to be conflated with:
  - formatting perturbations (``java_perturbations.py``) — Type-1 drift FP
  - assertion-engine mutants (``tests/spring_signals/mutation_driver.py``)
  - PIT-class Java SUT mutation (ROR/bytecode) — out of scope here
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import NamedTuple, Optional


class Mutator(NamedTuple):
    """One deliberate defect the gate harness should kill.

    Data this file interprets, never behaviour a document supplies — the same
    boundary ``check_repo_claims.py`` draws around its predicates.

    ``lang`` decides HOW the defect is located. Set it to an ast-grep language
    and the anchor is a structural pattern rewritten with ``ast-grep --rewrite``,
    so reindenting or reflowing the target cannot quietly detach the mutator
    from the code it is supposed to break. Leave it empty and the anchor is a
    literal string.

    The literal cases are not laziness, and each one in the catalog says why:
      - markdown, where ast-grep's grammar matches broad block nodes. Measured
        on this repo's README: a pattern for ``ast-grep`` reported 35 lines of
        which 27 contained no such string. A rewrite driven by that would edit
        the wrong text.
      - the ast-grep rule file itself, where the text to match *contains*
        ``$$$ARGS``. That is ast-grep's own metavariable syntax, so a structural
        search for it does not mean what it reads as.

    Both are covered instead by ``test_mutate.RegistryAnchorsTest``, which fails
    the build when a literal anchor drifts out of the file it names.
    """

    name: str
    path: str
    lang: str
    find: str
    replace: str
    expected_caught_by: str
    why: str

    def apply(self, root: Path) -> Optional[str]:
        """Locate the anchor under ``root`` and introduce the defect.

        Returns an error string if the mutation could not be applied. An
        unapplied mutator is never scored: a defect that was never introduced
        tells you nothing about whether a test would have caught it.
        """
        target = root / self.path
        if not target.is_file():
            return f"{self.path} is not in the tracked tree"
        if self.lang:
            return _apply_structural(target, self)
        return _apply_literal(target, self)


def _apply_structural(path: Path, mutator: Mutator) -> Optional[str]:
    """Rewrite via ast-grep, so the anchor survives reformatting.

    The exit code cannot carry this decision. Measured against ast-grep
    0.44.1: ``--update-all`` exits 1 both when the pattern matches nothing and
    when the invocation genuinely fails, so the two are indistinguishable
    from the status alone. What is unambiguous is whether the file moved, so
    that is what is checked — and it stays correct if the exit-code
    behaviour changes in a later release.
    """
    before = path.read_text(encoding="utf-8")
    result = subprocess.run(
        ["ast-grep", "run", "-l", mutator.lang, "-p", mutator.find,
         "-r", mutator.replace, "--update-all", str(path)],
        capture_output=True, text=True)
    if path.read_text(encoding="utf-8") != before:
        return None
    detail = result.stderr.strip()[:160]
    return (f"structural pattern matched nothing in {mutator.path}; the mutator "
            f"has drifted from the code and is testing nothing"
            + (f" (ast-grep said: {detail})" if detail else ""))


def _apply_literal(path: Path, mutator: Mutator) -> Optional[str]:
    text = path.read_text(encoding="utf-8")
    if mutator.find not in text:
        return (f"anchor not found in {mutator.path}; the mutator has drifted "
                f"from the file and is testing nothing")
    path.write_text(text.replace(mutator.find, mutator.replace, 1), encoding="utf-8")
    return None
