"""Widget domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class Widget:
    """A renderable widget inside a page."""

    id: str
    type: str
    title: str | None = None
    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1
    config: JsonObject = field(default_factory=dict)
