"""Export compiled dashboards."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TextIO


def export_dashboard_json(payload: dict[str, Any], output: str | Path | TextIO | None = None) -> str:
    """Serialize a compiled dashboard payload as formatted JSON."""

    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        return rendered
    if hasattr(output, "write"):
        output.write(rendered)
        return rendered
    Path(output).write_text(rendered, encoding="utf-8")
    return rendered
