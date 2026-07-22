"""Validation helpers for the dashboard domain model."""

from __future__ import annotations

from .model import Dashboard


def validate_dashboard(dashboard: Dashboard) -> None:
    """Validate that a dashboard contains the required core fields.

    Args:
        dashboard: Dashboard instance to validate.

    Raises:
        ValueError: If the dashboard, one of its pages, or one of its widgets is
            missing a required value.
    """
    if not dashboard.pages:
        raise ValueError("Dashboard must contain at least one page.")

    for page in dashboard.pages:
        if not page.title:
            raise ValueError(f"Page {page.id!r} must define a title.")

        for widget in page.widgets:
            if widget.type is None:
                raise ValueError(f"Widget {widget.id!r} must define a type.")
            if not widget.label:
                raise ValueError(f"Widget {widget.id!r} must define a label.")
