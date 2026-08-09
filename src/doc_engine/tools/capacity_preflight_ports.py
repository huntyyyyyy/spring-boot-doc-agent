"""Hexagonal ports for capacity preflight estimate vs report write."""

from __future__ import annotations

from typing import Any, Protocol


class CapacityEstimatePort(Protocol):
    """Port: estimate Stage-0 / Stage-4 capacity from repo + optional artifacts."""

    def compute_preflight(self, *args: Any, **kwargs: Any) -> dict:
        ...


class CapacityReportWriter(Protocol):
    """Port: persist a capacity preflight / calibration report to disk."""

    def write_report(self, path: str, report: dict) -> None:
        ...


def write_capacity_report(path: str, report: dict) -> None:
    """Default filesystem adapter for CapacityReportWriter."""
    from doc_engine.tools.capacity_preflight_cli import _maybe_write_report

    _maybe_write_report(path, report)
