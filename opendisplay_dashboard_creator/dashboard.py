"""Dashboard domain model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .page import Page


@dataclass(frozen=True, slots=True)
class Dashboard:
    """Top-level dashboard definition."""

    title: str
    pages: tuple[Page, ...] = field(default_factory=tuple)
    version: int = 1
