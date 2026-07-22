import json
import subprocess
import sys

from opendisplay_dashboard_creator.compiler import compile_dashboard
from opendisplay_dashboard_creator.exporter import export_dashboard_json
from opendisplay_dashboard_creator.parser import parse_dashboard


def test_parser_compiler_and_exporter_reuse_supported_dashboard(tmp_path):
    source = tmp_path / "dashboard.yaml"
    source.write_text(
        """
title: Operations
widgets:
  - type: metric
    title: Requests
    x: 1
    y: 2
    width: 3
    height: 4
    options:
      query: requests_total
""".strip(),
        encoding="utf-8",
    )

    dashboard = parse_dashboard(source)
    payload = compile_dashboard(dashboard)
    rendered = export_dashboard_json(payload)

    assert json.loads(rendered) == {
        "title": "Operations",
        "widgets": [
            {
                "type": "metric",
                "title": "Requests",
                "layout": {"x": 1, "y": 2, "width": 3, "height": 4},
                "options": {"query": "requests_total"},
            }
        ],
    }


def test_package_module_cli_outputs_json(tmp_path):
    source = tmp_path / "dashboard.yaml"
    source.write_text("title: Empty\nwidgets: []\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "opendisplay_dashboard_creator", str(source)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(result.stdout) == {"title": "Empty", "widgets": []}
