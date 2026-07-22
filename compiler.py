"""MVP compiler for OpenDisplay dashboard YAML definitions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CompileError(ValueError):
    """Raised when a dashboard definition cannot be compiled."""


def load_dashboard(source: str | Path) -> dict[str, Any]:
    """Load a dashboard definition from a YAML file."""
    path = Path(source)
    return parse_dashboard_yaml(path.read_text(encoding="utf-8"))


def compile_dashboard(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    """Compile a dashboard YAML path or dashboard mapping into JSON-ready data."""
    dashboard = load_dashboard(source) if isinstance(source, (str, Path)) else source
    if not isinstance(dashboard, dict):
        raise CompileError("Dashboard definition must be a mapping.")
    if not dashboard:
        raise CompileError("Dashboard definition must not be empty.")

    compiled = dict(dashboard)
    compiled.setdefault("type", "dashboard")
    compiled.setdefault("version", 1)
    return compiled


def compile_dashboard_json(source: str | Path | dict[str, Any]) -> str:
    """Compile a dashboard definition and return a stable JSON string."""
    return json.dumps(compile_dashboard(source), ensure_ascii=False, indent=2, sort_keys=True)


def parse_dashboard_yaml(content: str) -> dict[str, Any]:
    """Parse the supported dashboard YAML subset without changing the data model."""
    lines = _meaningful_lines(content)
    if not lines:
        raise CompileError("Dashboard YAML is empty.")

    document, next_index = _parse_block(lines, 0, lines[0][0])
    if next_index != len(lines):
        raise CompileError("Unexpected YAML content after the dashboard definition.")
    if not isinstance(document, dict):
        raise CompileError("Dashboard YAML root must be a mapping.")
    return document


def _meaningful_lines(content: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for raw in content.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2 != 0:
            raise CompileError("YAML indentation must use multiples of two spaces.")
        result.append((indent, stripped))
    return result


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index][0] < indent:
        return {}, index
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _parse_mapping(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise CompileError(f"Unexpected indentation near '{text}'.")
        if text.startswith("- "):
            break
        key, value = _split_key_value(text)
        if value == "":
            value, index = _parse_block(lines, index + 1, indent + 2)
        else:
            value = _parse_scalar(value)
            index += 1
        mapping[key] = value
    return mapping, index


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    values: list[Any] = []
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent != indent or not text.startswith("- "):
            break
        item_text = text[2:].strip()
        if item_text == "":
            value, index = _parse_block(lines, index + 1, indent + 2)
        elif ":" in item_text and not item_text.startswith(('"', "'")):
            key, scalar = _split_key_value(item_text)
            value = {key: _parse_scalar(scalar)} if scalar else {key: None}
            index += 1
            while index < len(lines) and lines[index][0] == indent + 2 and not lines[index][1].startswith("- "):
                child_key, child_value = _split_key_value(lines[index][1])
                if child_value == "":
                    nested, index = _parse_block(lines, index + 1, indent + 4)
                    value[child_key] = nested
                else:
                    value[child_key] = _parse_scalar(child_value)
                    index += 1
        else:
            value = _parse_scalar(item_text)
            index += 1
        values.append(value)
    return values, index


def _split_key_value(text: str) -> tuple[str, str]:
    if ":" not in text:
        raise CompileError(f"Expected key/value pair near '{text}'.")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise CompileError("YAML mapping keys cannot be empty.")
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
