"""Renderer for OpenDisplay-compatible dashboard payloads."""

from __future__ import annotations

from typing import Any

from .dashboard import Dashboard
from .validator import validate_dashboard

JsonObject = dict[str, Any]


def render_dashboard(dashboard: Dashboard) -> JsonObject:
    """Render a dashboard model to a serializable OpenDisplay payload."""

    validate_dashboard(dashboard)
    return {
        "version": dashboard.version,
        "title": dashboard.title,
        "pages": [
            {
                "id": page.id,
                "title": page.title,
                "widgets": [
                    {
                        "id": widget.id,
                        "type": widget.type,
                        "title": widget.title,
                        "layout": {
                            "x": widget.x,
                            "y": widget.y,
                            "width": widget.width,
                            "height": widget.height,
                        },
                        "config": widget.config,
                    }
                    for widget in page.widgets
                ],
            }
            for page in dashboard.pages
        ],
    }
