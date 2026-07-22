"""OpenDisplay dashboard creator MVP compiler."""

from .compiler import compile_dashboard
from .parser import parse_dashboard_yaml

__all__ = ["compile_dashboard", "parse_dashboard_yaml"]
