"""YAML parser for dashboard definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .model import Alignment, Dashboard, Layout, Page, Style, Widget, WidgetType
from .validator import validate_dashboard


def load_dashboard(path: str | Path) -> Dashboard:
    """Load a dashboard YAML file and return a Dashboard object.

    Args:
        path: Filesystem path to a YAML dashboard definition.

    Returns:
        A parsed and validated Dashboard instance.
    """
    with Path(path).open("r", encoding="utf-8") as dashboard_file:
        data = yaml.safe_load(dashboard_file) or {}

    dashboard = _parse_dashboard(data)
    validate_dashboard(dashboard)
    return dashboard


def _parse_dashboard(data: dict[str, Any]) -> Dashboard:
    pages = [_parse_page(page_data) for page_data in data.get("pages", [])]
    return Dashboard(title=str(data.get("title", "")), pages=pages)


def _parse_page(data: dict[str, Any]) -> Page:
    widgets = [_parse_widget(widget_data) for widget_data in data.get("widgets", [])]
    return Page(
        id=str(data.get("id", "")),
        title=str(data.get("title", "")),
        layout=_parse_layout(data.get("layout", {})),
        widgets=widgets,
    )


def _parse_widget(data: dict[str, Any]) -> Widget:
    return Widget(
        id=str(data.get("id", "")),
        type=WidgetType(data["type"]) if data.get("type") is not None else None,  # type: ignore[arg-type]
        label=str(data.get("label", "")),
        entity=data.get("entity"),
        style=_parse_style(data.get("style", {})),
    )


def _parse_style(data: dict[str, Any]) -> Style:
    alignment = data.get("alignment", Alignment.LEFT.value)
    return Style(
        font=data.get("font"),
        size=data.get("size"),
        color=data.get("color"),
        bold=bool(data.get("bold", False)),
        alignment=Alignment(alignment),
    )


def _parse_layout(data: dict[str, Any]) -> Layout:
    return Layout(
        rows=int(data.get("rows", 1)),
        columns=int(data.get("columns", 1)),
        margin=int(data.get("margin", 0)),
        spacing=int(data.get("spacing", 0)),
    )
