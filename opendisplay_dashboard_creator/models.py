"""Dashboard data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Widget:
    """A widget displayed on an OpenDisplay dashboard."""

    type: str
    title: str
    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1
    options: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Dashboard:
    """Dashboard definition supported by the package."""

    title: str
    widgets: tuple[Widget, ...] = ()
