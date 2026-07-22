"""Page domain model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .widget import Widget


@dataclass(frozen=True, slots=True)
class Page:
    """A dashboard page containing widgets."""

    id: str
    title: str
    widgets: tuple[Widget, ...] = field(default_factory=tuple)
