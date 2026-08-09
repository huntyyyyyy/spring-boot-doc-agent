"""unittest.TestCase binding for session ``kitchen`` fixture (E-KH1)."""

from __future__ import annotations

import unittest

import pytest

from tests.support.kitchen_sink.artifacts import KitchenArtifacts


class KitchenBoundTestCase(unittest.TestCase):
    """Autouse-binds read-only ``kitchen`` onto ``self.kitchen``."""

    kitchen: KitchenArtifacts

    @pytest.fixture(autouse=True)
    def _bind_kitchen(self, kitchen: KitchenArtifacts) -> None:
        self.kitchen = kitchen
