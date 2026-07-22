"""Compile dashboard models to OpenDisplay JSON-compatible structures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import Dashboard
from .parser import parse_dashboard


def compile_dashboard(source: str | Path | Dashboard) -> dict[str, Any]:
    """Compile a supported dashboard into an OpenDisplay JSON payload."""

    dashboard = parse_dashboard(source) if isinstance(source, (str, Path)) else source
    return {
        "title": dashboard.title,
        "widgets": [
            {
                "type": widget.type,
                "title": widget.title,
                "layout": {
                    "x": widget.x,
                    "y": widget.y,
                    "width": widget.width,
                    "height": widget.height,
                },
                "options": dict(widget.options),
            }
            for widget in dashboard.widgets
        ],
    }
