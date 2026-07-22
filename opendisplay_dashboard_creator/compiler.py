"""Compiler from validated dashboard YAML mappings to OpenDisplay JSON."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class DashboardValidationError(ValueError):
    """Raised when a dashboard definition is not valid for the MVP compiler."""


_REQUIRED_WIDGET_FIELDS = ("id", "type")


def compile_dashboard(dashboard: dict[str, Any]) -> dict[str, Any]:
    """Validate and compile a dashboard mapping into an exportable JSON object."""

    if not isinstance(dashboard, dict):
        raise DashboardValidationError("Dashboard must be a mapping")

    title = _require_string(dashboard, "title")
    widgets = _require_list(dashboard, "widgets")

    compiled_widgets = [_compile_widget(widget, index) for index, widget in enumerate(widgets)]
    return {
        "schema": "opendisplay.dashboard.v1",
        "title": title,
        "widgets": compiled_widgets,
    }


def _compile_widget(widget: Any, index: int) -> dict[str, Any]:
    if not isinstance(widget, dict):
        raise DashboardValidationError(f"Widget at index {index} must be a mapping")

    compiled = deepcopy(widget)
    for field in _REQUIRED_WIDGET_FIELDS:
        value = compiled.get(field)
        if not isinstance(value, str) or not value.strip():
            raise DashboardValidationError(
                f"Widget at index {index} must define a non-empty string '{field}'"
            )

    position = compiled.get("position")
    if position is not None:
        _validate_position(position, index)

    return compiled


def _require_string(document: dict[str, Any], field: str) -> str:
    value = document.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DashboardValidationError(f"Dashboard must define a non-empty string '{field}'")
    return value


def _require_list(document: dict[str, Any], field: str) -> list[Any]:
    value = document.get(field)
    if not isinstance(value, list):
        raise DashboardValidationError(f"Dashboard must define a list '{field}'")
    return value


def _validate_position(position: Any, index: int) -> None:
    if not isinstance(position, dict):
        raise DashboardValidationError(f"Widget at index {index} position must be a mapping")

    for field in ("x", "y", "w", "h"):
        value = position.get(field)
        if not isinstance(value, int) or value < 0:
            raise DashboardValidationError(
                f"Widget at index {index} position '{field}' must be a non-negative integer"
            )
