"""Export compiled OpenDisplay dashboard data."""

from __future__ import annotations

from pathlib import Path

from compiler import compile_dashboard_json


def export_dashboard_json(source: str | Path, destination: str | Path) -> Path:
    """Compile a dashboard YAML file and write the resulting JSON file."""
    output_path = Path(destination)
    output_path.write_text(compile_dashboard_json(source) + "\n", encoding="utf-8")
    return output_path
