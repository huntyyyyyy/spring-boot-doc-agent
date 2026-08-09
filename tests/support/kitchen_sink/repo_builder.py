"""Assemble the kitchen-sink enterprise fixture repo."""

from __future__ import annotations

import os

from tests.support.kitchen_sink.repo_plants_billing import plant_root_and_billing
from tests.support.kitchen_sink.repo_plants_config_noise import (
    plant_config_twins,
    plant_ledger_legacy_noise,
)


def build_enterprise_repo(root):
    """Write a deterministic, hostile, multi-module Spring repo.

    Deterministic in the strict sense: fixed content, no randomness, no clock,
    no network — which is what lets the invariant assertions mean anything.
    The hostile bytes are declared inline rather than copied from a checked-in
    tree, because git and editors silently normalize exactly the things under
    test here (BOM, CRLF, lone high bytes).
    """
    os.makedirs(root, exist_ok=True)
    plant_root_and_billing(root)
    plant_config_twins(root)
    plant_ledger_legacy_noise(root)
