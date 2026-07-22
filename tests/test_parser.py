from __future__ import annotations

import pytest

from opendisplay_dashboard_creator.parser import DashboardParserError, parse_dashboard
from opendisplay_dashboard_creator.renderer import render_dashboard


def test_parse_dashboard_and_render_payload() -> None:
    dashboard = parse_dashboard(
        """
        version: 1
        title: Factory floor
        pages:
          - id: overview
            title: Overview
            widgets:
              - id: temperature
                type: gauge
                title: Temperature
                x: 1
                y: 2
                width: 3
                height: 4
                config:
                  unit: C
        """
    )

    assert dashboard.title == "Factory floor"
    assert dashboard.pages[0].widgets[0].config == {"unit": "C"}
    assert render_dashboard(dashboard)["pages"][0]["widgets"][0]["layout"] == {
        "x": 1,
        "y": 2,
        "width": 3,
        "height": 4,
    }


@pytest.mark.parametrize(
    ("yaml_content", "message"),
    [
        ("", "document is empty"),
        ("title: Demo\npages: []\nextra: nope", "unknown key"),
        ("title: Demo\npages: nope", "dashboard.pages must be a list"),
        ("title: Demo\npages:\n - id: 1\n   title: Page", "id must be a string"),
        (
            "\n".join(
                [
                    "title: Demo",
                    "pages:",
                    " - id: page",
                    "   title: Page",
                    "   widgets:",
                    "    - id: w",
                    "      type: chart",
                    "      width: false",
                ]
            ),
            "width must be an integer",
        ),
    ],
)
def test_parser_is_strict(yaml_content: str, message: str) -> None:
    with pytest.raises(DashboardParserError, match=message):
        parse_dashboard(yaml_content)


def test_yaml_errors_include_location() -> None:
    with pytest.raises(DashboardParserError, match="Invalid YAML.*line"):
        parse_dashboard("title: [broken")
