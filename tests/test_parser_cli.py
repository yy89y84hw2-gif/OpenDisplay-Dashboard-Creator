import json

import pytest

from opendisplay_dashboard_creator.cli import main
from opendisplay_dashboard_creator.parser import DashboardParseError, parse_dashboard_yaml


def test_parse_dashboard_yaml_reads_yaml_mapping(tmp_path):
    source = tmp_path / "dashboard.yaml"
    source.write_text(
        """
title: Operations
widgets:
  - id: cpu
    type: metric
""".strip(),
        encoding="utf-8",
    )

    assert parse_dashboard_yaml(source) == {
        "title": "Operations",
        "widgets": [{"id": "cpu", "type": "metric"}],
    }


def test_parse_dashboard_yaml_rejects_non_mapping_root(tmp_path):
    source = tmp_path / "dashboard.yaml"
    source.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    with pytest.raises(DashboardParseError, match="root must be a mapping"):
        parse_dashboard_yaml(source)


def test_cli_compiles_yaml_to_json_file(tmp_path):
    source = tmp_path / "dashboard.yaml"
    output = tmp_path / "dashboard.json"
    source.write_text(
        """
title: Operations
widgets:
  - id: cpu
    type: metric
""".strip(),
        encoding="utf-8",
    )

    assert main([str(source), "--output", str(output)]) == 0

    assert json.loads(output.read_text(encoding="utf-8")) == {
        "schema": "opendisplay.dashboard.v1",
        "title": "Operations",
        "widgets": [{"id": "cpu", "type": "metric"}],
    }
