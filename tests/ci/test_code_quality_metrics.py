"""Cohesive suite from tests/ci/test_check_code_quality.py: ComplexityTest, NestingDepthTest, QualnameTest, AnnotationCoverageTest."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from tests.conftest import REPO_ROOT, SCRIPTS_DIR, FIXTURE_DIR, FIXTURE_SNAPSHOT_PATH
SCRIPT_DIR = SCRIPTS_DIR
import check_code_quality as checker
from tests.support.code_quality.measure import measure_one

class ComplexityTest(unittest.TestCase):
    def test_straight_line_function_has_complexity_one(self):
        functions, _, _ = measure_one("def f():\n    return 1\n")
        self.assertEqual(functions["mod.py::f"]["complexity"], 1)

    def test_each_if_adds_one_branch(self):
        source = "def f(a):\n    if a:\n        return 1\n    if a > 2:\n        return 2\n    return 3\n"
        functions, _, _ = measure_one(source)
        self.assertEqual(functions["mod.py::f"]["complexity"], 3)

    def test_and_chain_counts_each_extra_operand(self):
        """`a and b and c` is two decisions, not one -- a reader evaluates
        both. This is where this metric deliberately exceeds textbook
        McCabe, so it is pinned rather than left implicit."""
        functions, _, _ = measure_one("def f(a, b, c):\n    return a and b and c\n")
        self.assertEqual(functions["mod.py::f"]["complexity"], 3)

    def test_comprehension_filter_counts_beyond_the_comprehension_itself(self):
        functions, _, _ = measure_one("def f(xs):\n    return [x for x in xs if x if x > 1]\n")
        self.assertEqual(functions["mod.py::f"]["complexity"], 4)


class NestingDepthTest(unittest.TestCase):
    def test_flat_function_has_depth_zero(self):
        functions, _, _ = measure_one("def f():\n    return 1\n")
        self.assertEqual(functions["mod.py::f"]["depth"], 0)

    def test_nested_blocks_accumulate_depth(self):
        source = (
            "def f(xs):\n"
            "    for x in xs:\n"
            "        if x:\n"
            "            with open(x) as h:\n"
            "                return h\n"
        )
        functions, _, _ = measure_one(source)
        self.assertEqual(functions["mod.py::f"]["depth"], 3)

    def test_sequential_blocks_do_not_accumulate_depth(self):
        """Two `if`s in a row are depth 1, not 2 -- the metric measures
        containment, which is what a reader has to hold on the stack, not
        the number of blocks."""
        source = "def f(a):\n    if a:\n        pass\n    if a:\n        pass\n"
        functions, _, _ = measure_one(source)
        self.assertEqual(functions["mod.py::f"]["depth"], 1)

    def test_nested_function_depth_belongs_to_itself_not_its_parent(self):
        source = (
            "def outer(xs):\n"
            "    def inner(ys):\n"
            "        for y in ys:\n"
            "            if y:\n"
            "                return y\n"
            "    return inner\n"
        )
        functions, _, _ = measure_one(source)
        self.assertEqual(functions["mod.py::outer"]["depth"], 0)
        self.assertEqual(functions["mod.py::outer.inner"]["depth"], 2)


class QualnameTest(unittest.TestCase):
    def test_method_is_keyed_by_class_and_name(self):
        functions, _, _ = measure_one("class C:\n    def m(self):\n        return 1\n")
        self.assertIn("mod.py::C.m", functions)

    def test_function_defined_inside_an_if_is_still_found(self):
        functions, _, _ = measure_one("import os\nif os.name:\n    def f():\n        return 1\n")
        self.assertIn("mod.py::f", functions)

    def test_duplicate_qualname_keeps_the_worse_measurement(self):
        """A conditional def gives one key two measurements. Keeping the
        worse one is the safe direction: the ratchet must not be loosened by
        a definition the interpreter may never execute."""
        source = (
            "import os\n"
            "if os.name:\n"
            "    def f(a):\n"
            "        return 1\n"
            "else:\n"
            "    def f(a):\n"
            "        if a:\n"
            "            if a > 1:\n"
            "                return 2\n"
            "        return 3\n"
        )
        functions, _, _ = measure_one(source)
        self.assertEqual(functions["mod.py::f"]["complexity"], 3)
        self.assertEqual(functions["mod.py::f"]["depth"], 2)


class AnnotationCoverageTest(unittest.TestCase):
    def test_return_annotation_alone_counts_as_annotated(self):
        _, total, annotated = measure_one("def f(a) -> int:\n    return a\n")
        self.assertEqual((total, annotated), (1, 1))

    def test_one_annotated_parameter_counts_as_annotated(self):
        _, total, annotated = measure_one("def f(a: int, b):\n    return a\n")
        self.assertEqual((total, annotated), (1, 1))

    def test_bare_function_does_not_count(self):
        _, total, annotated = measure_one("def f(a, b):\n    return a\n")
        self.assertEqual((total, annotated), (1, 0))

    def test_self_alone_does_not_make_a_method_annotated(self):
        """Nobody annotates `self`; counting it would let a method claim
        coverage it does not have."""
        _, total, annotated = measure_one("class C:\n    def m(self):\n        return 1\n")
        self.assertEqual((total, annotated), (1, 0))
