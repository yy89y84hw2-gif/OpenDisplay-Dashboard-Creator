"""YAML parser for dashboard definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class DashboardParseError(ValueError):
    """Raised when a dashboard YAML document cannot be parsed."""


def parse_dashboard_yaml(source: str | Path) -> dict[str, Any]:
    """Parse a dashboard YAML file and return its mapping.

    The MVP input format is YAML. This function intentionally keeps YAML as the
    only accepted source format and rejects empty documents or non-mapping roots.
    """

    path = Path(source)
    try:
        with path.open("r", encoding="utf-8") as yaml_file:
            document = yaml.safe_load(yaml_file)
    except yaml.YAMLError as exc:
        raise DashboardParseError(f"Invalid YAML in {path}: {exc}") from exc
    except OSError as exc:
        raise DashboardParseError(f"Unable to read {path}: {exc}") from exc

    if document is None:
        raise DashboardParseError(f"Dashboard YAML is empty: {path}")
    if not isinstance(document, dict):
        raise DashboardParseError("Dashboard YAML root must be a mapping")

    return document
