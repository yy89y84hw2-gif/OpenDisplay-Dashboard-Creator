"""Validated dashboard model contracts used by the MVP compiler."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Layout:
    """Position and size of a dashboard widget."""

    x: int = 0
    y: int = 0
    width: int = 1
    height: int = 1

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "Layout":
        if data is None:
            return cls()
        return cls(
            x=int(data.get("x", 0)),
            y=int(data.get("y", 0)),
            width=int(data.get("width", data.get("w", 1))),
            height=int(data.get("height", data.get("h", 1))),
        )

    def to_json(self) -> dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class Widget:
    """Dashboard widget model."""

    id: str
    type: str
    title: str = ""
    source: str | None = None
    layout: Layout = field(default_factory=Layout)
    options: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Widget":
        return cls(
            id=str(data["id"]),
            type=str(data.get("type", "text")),
            title=str(data.get("title", "")),
            source=None if data.get("source") is None else str(data.get("source")),
            layout=Layout.from_mapping(data.get("layout")),
            options=dict(data.get("options", {})),
        )

    def to_json(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "layout": self.layout.to_json(),
            "options": dict(self.options),
        }
        if self.source is not None:
            payload["source"] = self.source
        return payload


@dataclass(frozen=True)
class Dashboard:
    """Dashboard model accepted by the compiler."""

    title: str
    widgets: tuple[Widget, ...] = ()
    version: str = "1"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Dashboard":
        widgets = tuple(Widget.from_mapping(item) for item in data.get("widgets", []))
        return cls(
            title=str(data.get("title", "Untitled dashboard")),
            widgets=widgets,
            version=str(data.get("version", "1")),
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "title": self.title,
            "widgets": [widget.to_json() for widget in self.widgets],
        }
