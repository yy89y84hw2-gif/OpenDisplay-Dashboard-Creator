"""Strict YAML parser for dashboard definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml

from .dashboard import Dashboard
from .page import Page
from .validator import DashboardValidationError, validate_dashboard
from .widget import Widget

RawMap = dict[str, Any]


class DashboardParserError(ValueError):
    """Raised when YAML cannot be parsed into a dashboard."""


def parse_dashboard_file(path: str | Path) -> Dashboard:
    """Parse a dashboard definition from a YAML file."""

    source = Path(path)
    try:
        content = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise DashboardParserError(f"Unable to read YAML file {source}: {exc}") from exc
    return parse_dashboard(content, source_name=str(source))


def parse_dashboard(yaml_content: str, *, source_name: str = "<string>") -> Dashboard:
    """Parse a strict, typed dashboard YAML document."""

    try:
        raw = yaml.safe_load(yaml_content)
    except yaml.YAMLError as exc:
        detail = _format_yaml_error(exc)
        raise DashboardParserError(f"Invalid YAML in {source_name}: {detail}") from exc

    if raw is None:
        raise DashboardParserError(
            f"Invalid dashboard in {source_name}: document is empty"
        )
    root = _require_map(raw, "dashboard")
    allowed_root = {"version", "title", "pages"}
    _reject_unknown_keys(root, allowed_root, "dashboard")

    dashboard = Dashboard(
        version=_optional_int(root, "version", 1, "dashboard.version"),
        title=_required_str(root, "title", "dashboard.title"),
        pages=tuple(_parse_pages(_required_list(root, "pages", "dashboard.pages"))),
    )
    try:
        validate_dashboard(dashboard)
    except DashboardValidationError as exc:
        raise DashboardParserError(
            f"Invalid dashboard in {source_name}: {exc}"
        ) from exc
    return dashboard


def _parse_pages(raw_pages: list[Any]) -> list[Page]:
    pages: list[Page] = []
    for index, raw_page in enumerate(raw_pages):
        location = f"dashboard.pages[{index}]"
        page = _require_map(raw_page, location)
        _reject_unknown_keys(page, {"id", "title", "widgets"}, location)
        pages.append(
            Page(
                id=_required_str(page, "id", f"{location}.id"),
                title=_required_str(page, "title", f"{location}.title"),
                widgets=tuple(
                    _parse_widgets(
                        _optional_list(page, "widgets", [], f"{location}.widgets"),
                        location,
                    )
                ),
            )
        )
    return pages


def _parse_widgets(raw_widgets: list[Any], page_location: str) -> list[Widget]:
    widgets: list[Widget] = []
    for index, raw_widget in enumerate(raw_widgets):
        location = f"{page_location}.widgets[{index}]"
        widget = _require_map(raw_widget, location)
        _reject_unknown_keys(
            widget,
            {"id", "type", "title", "x", "y", "width", "height", "config"},
            location,
        )
        widgets.append(
            Widget(
                id=_required_str(widget, "id", f"{location}.id"),
                type=_required_str(widget, "type", f"{location}.type"),
                title=_optional_str(widget, "title", None, f"{location}.title"),
                x=_optional_int(widget, "x", 0, f"{location}.x"),
                y=_optional_int(widget, "y", 0, f"{location}.y"),
                width=_optional_int(widget, "width", 1, f"{location}.width"),
                height=_optional_int(widget, "height", 1, f"{location}.height"),
                config=_optional_map(widget, "config", {}, f"{location}.config"),
            )
        )
    return widgets


def _format_yaml_error(exc: yaml.YAMLError) -> str:
    if hasattr(exc, "problem_mark") and exc.problem_mark is not None:
        mark = exc.problem_mark
        return f"line {mark.line + 1}, column {mark.column + 1}: {exc}"
    return str(exc)


def _reject_unknown_keys(raw: RawMap, allowed: set[str], location: str) -> None:
    unknown = sorted(set(raw) - allowed)
    if unknown:
        raise DashboardParserError(
            f"{location} contains unknown key(s): {', '.join(unknown)}"
        )


def _required_str(raw: RawMap, key: str, location: str) -> str:
    if key not in raw:
        raise DashboardParserError(f"{location} is required")
    return _as_str(raw[key], location)


def _optional_str(
    raw: RawMap, key: str, default: str | None, location: str
) -> str | None:
    if key not in raw or raw[key] is None:
        return default
    return _as_str(raw[key], location)


def _optional_int(raw: RawMap, key: str, default: int, location: str) -> int:
    if key not in raw:
        return default
    value = raw[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise DashboardParserError(f"{location} must be an integer")
    return cast(int, value)


def _required_list(raw: RawMap, key: str, location: str) -> list[Any]:
    if key not in raw:
        raise DashboardParserError(f"{location} is required")
    value = raw[key]
    if not isinstance(value, list):
        raise DashboardParserError(f"{location} must be a list")
    return value


def _optional_list(
    raw: RawMap, key: str, default: list[Any], location: str
) -> list[Any]:
    if key not in raw:
        return default
    value = raw[key]
    if not isinstance(value, list):
        raise DashboardParserError(f"{location} must be a list")
    return value


def _optional_map(raw: RawMap, key: str, default: RawMap, location: str) -> RawMap:
    if key not in raw:
        return default.copy()
    return _require_map(raw[key], location)


def _require_map(value: Any, location: str) -> RawMap:
    if not isinstance(value, dict):
        raise DashboardParserError(f"{location} must be a mapping")
    if not all(isinstance(key, str) for key in value):
        raise DashboardParserError(f"{location} keys must be strings")
    return value


def _as_str(value: Any, location: str) -> str:
    if not isinstance(value, str):
        raise DashboardParserError(f"{location} must be a string")
    return value
