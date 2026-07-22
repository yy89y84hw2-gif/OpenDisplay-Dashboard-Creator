"""Core domain objects for OpenDisplay Dashboard Creator."""

from .model import Alignment, Dashboard, Layout, Page, Style, Widget, WidgetType
from .parser import load_dashboard
from .validator import validate_dashboard

__all__ = [
    "Alignment",
    "Dashboard",
    "Layout",
    "Page",
    "Style",
    "Widget",
    "WidgetType",
    "load_dashboard",
    "validate_dashboard",
]
