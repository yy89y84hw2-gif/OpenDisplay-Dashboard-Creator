"""YAML parser for supported dashboard definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml

from .models import Dashboard, Widget


def parse_dashboard(path: str | Path) -> Dashboard:
    """Parse a dashboard YAML file into package models."""

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise ValueError("Dashboard file must contain a YAML mapping.")
    return dashboard_from_mapping(raw)


def dashboard_from_mapping(raw: Mapping[str, Any]) -> Dashboard:
    """Build a dashboard model from already-loaded YAML data."""

    title = raw.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError("Dashboard requires a non-empty string title.")

    widgets = raw.get("widgets", [])
    if not isinstance(widgets, list):
        raise ValueError("Dashboard widgets must be a list.")

    return Dashboard(title=title, widgets=tuple(_widget_from_mapping(widget) for widget in widgets))


def _widget_from_mapping(raw: Any) -> Widget:
    if not isinstance(raw, Mapping):
        raise ValueError("Each widget must be a mapping.")

    widget_type = raw.get("type")
    title = raw.get("title")
    if not isinstance(widget_type, str) or not widget_type:
        raise ValueError("Each widget requires a non-empty string type.")
    if not isinstance(title, str) or not title:
        raise ValueError("Each widget requires a non-empty string title.")

    return Widget(
        type=widget_type,
        title=title,
        x=_int_value(raw, "x", 0),
        y=_int_value(raw, "y", 0),
        width=_int_value(raw, "width", 1),
        height=_int_value(raw, "height", 1),
        options=_mapping_value(raw, "options"),
    )


def _int_value(raw: Mapping[str, Any], key: str, default: int) -> int:
    value = raw.get(key, default)
    if not isinstance(value, int):
        raise ValueError(f"Widget {key} must be an integer.")
    return value


def _mapping_value(raw: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = raw.get(key, {})
    if not isinstance(value, Mapping):
        raise ValueError(f"Widget {key} must be a mapping.")
    return dict(value)
