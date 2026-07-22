"""Dashboard domain model.

This module contains the plain Python object model used by ODDC. It does not
contain OpenDisplay-specific or Home Assistant-specific behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class WidgetType(str, Enum):
    """Supported kinds of widgets that can appear on a dashboard page."""

    TEXT = "TEXT"
    VALUE = "VALUE"
    ICON = "ICON"
    SEPARATOR = "SEPARATOR"
    SPACER = "SPACER"
    CONTAINER = "CONTAINER"


class Alignment(str, Enum):
    """Horizontal alignment options for styled content."""

    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


@dataclass(slots=True)
class Style:
    """Visual styling applied to a widget."""

    font: str | None = None
    size: int | None = None
    color: str | None = None
    bold: bool = False
    alignment: Alignment = Alignment.LEFT

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the style."""
        return (
            "Style("
            f"font={self.font!r}, "
            f"size={self.size!r}, "
            f"color={self.color!r}, "
            f"bold={self.bold!r}, "
            f"alignment={self.alignment!r}"
            ")"
        )


@dataclass(slots=True)
class Layout:
    """Grid layout settings for a dashboard page."""

    rows: int = 1
    columns: int = 1
    margin: int = 0
    spacing: int = 0

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the layout."""
        return (
            "Layout("
            f"rows={self.rows!r}, "
            f"columns={self.columns!r}, "
            f"margin={self.margin!r}, "
            f"spacing={self.spacing!r}"
            ")"
        )


@dataclass(slots=True)
class Widget:
    """A display element placed on a dashboard page."""

    id: str
    type: WidgetType
    label: str
    entity: str | None = None
    style: Style = field(default_factory=Style)

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the widget."""
        return (
            "Widget("
            f"id={self.id!r}, "
            f"type={self.type!r}, "
            f"label={self.label!r}, "
            f"entity={self.entity!r}, "
            f"style={self.style!r}"
            ")"
        )


@dataclass(slots=True)
class Page:
    """A dashboard page containing widgets arranged with a layout."""

    id: str
    title: str
    layout: Layout = field(default_factory=Layout)
    widgets: list[Widget] = field(default_factory=list)

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the page."""
        return (
            "Page("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"layout={self.layout!r}, "
            f"widgets={self.widgets!r}"
            ")"
        )


@dataclass(slots=True)
class Dashboard:
    """Root object describing an entire dashboard."""

    title: str
    pages: list[Page] = field(default_factory=list)

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the dashboard."""
        return f"Dashboard(title={self.title!r}, pages={self.pages!r})"
