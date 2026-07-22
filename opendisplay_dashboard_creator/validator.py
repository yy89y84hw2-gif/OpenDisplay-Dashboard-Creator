"""Validation helpers for dashboard definitions."""

from __future__ import annotations

from collections.abc import Iterable

from .dashboard import Dashboard


class DashboardValidationError(ValueError):
    """Raised when a dashboard object is internally inconsistent."""


def validate_dashboard(dashboard: Dashboard) -> None:
    """Validate cross-object invariants for a parsed dashboard."""

    if dashboard.version < 1:
        raise DashboardValidationError(
            "dashboard.version must be greater than or equal to 1"
        )
    if not dashboard.title.strip():
        raise DashboardValidationError("dashboard.title must not be empty")

    page_ids = [page.id for page in dashboard.pages]
    _ensure_unique(page_ids, "page id")

    for page in dashboard.pages:
        if not page.id.strip():
            raise DashboardValidationError("page.id must not be empty")
        if not page.title.strip():
            raise DashboardValidationError(f"page {page.id!r} title must not be empty")
        widget_ids = [widget.id for widget in page.widgets]
        _ensure_unique(widget_ids, f"widget id on page {page.id!r}")
        for widget in page.widgets:
            if not widget.id.strip():
                raise DashboardValidationError(
                    f"page {page.id!r} contains an empty widget id"
                )
            if not widget.type.strip():
                raise DashboardValidationError(
                    f"widget {widget.id!r} type must not be empty"
                )
            if widget.width < 1 or widget.height < 1:
                raise DashboardValidationError(
                    f"widget {widget.id!r} width and height must be positive"
                )
            if widget.x < 0 or widget.y < 0:
                raise DashboardValidationError(
                    f"widget {widget.id!r} x and y coordinates must be positive or zero"
                )


def _ensure_unique(values: Iterable[str], label: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise DashboardValidationError(f"duplicate {label}: {value!r}")
        seen.add(value)
