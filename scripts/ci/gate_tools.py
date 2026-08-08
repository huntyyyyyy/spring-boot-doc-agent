#!/usr/bin/env python3
"""Deprecated shim — prefer ``from doc_engine.ci.gate_tools import …``."""

from __future__ import annotations

import sys

from doc_engine.ci import gate_tools as _impl

sys.modules[__name__] = _impl
