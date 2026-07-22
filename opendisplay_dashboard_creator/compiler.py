"""MVP compiler that converts validated dashboard models to OpenDisplay JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Dashboard
from .parser import parse_dashboard


def compile_dashboard(dashboard: Dashboard) -> dict[str, Any]:
    """Compile a validated dashboard model into the OpenDisplay JSON payload."""
    return {
        "opendisplay": {
            "schemaVersion": dashboard.version,
            "dashboard": dashboard.to_json(),
        }
    }


def compile_file(path: str | Path) -> dict[str, Any]:
    """Parse and compile a dashboard definition file."""
    return compile_dashboard(parse_dashboard(path))


def export_json(payload: dict[str, Any], output: str | Path | None = None) -> str:
    """Serialize compiled payload to JSON and optionally write it to disk."""
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output is not None:
        Path(output).write_text(text, encoding="utf-8")
    return text
