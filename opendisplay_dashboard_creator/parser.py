"""Parser for dashboard definitions used by the MVP compiler."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import Dashboard


def parse_dashboard_text(text: str) -> Dashboard:
    """Parse a dashboard definition from JSON text."""
    data = json.loads(text)
    if not isinstance(data, Mapping):
        raise ValueError("dashboard definition must be a JSON object")
    return Dashboard.from_mapping(data)


def parse_dashboard(path: str | Path) -> Dashboard:
    """Parse a dashboard definition file."""
    return parse_dashboard_text(Path(path).read_text(encoding="utf-8"))
