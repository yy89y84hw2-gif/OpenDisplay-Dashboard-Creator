from pathlib import Path

from oddc import Alignment, Dashboard, WidgetType, load_dashboard


def test_load_dashboard_returns_dashboard_from_yaml() -> None:
    dashboard = load_dashboard(Path("examples/minimal.yaml"))

    assert isinstance(dashboard, Dashboard)
    assert dashboard.title == "Minimal Dashboard"
    assert len(dashboard.pages) == 1

    page = dashboard.pages[0]
    assert page.id == "home"
    assert page.title == "Home"
    assert page.layout.rows == 1
    assert page.layout.columns == 1
    assert len(page.widgets) == 1

    widget = page.widgets[0]
    assert widget.id == "welcome"
    assert widget.type is WidgetType.TEXT
    assert widget.label == "Welcome"
    assert widget.style.alignment is Alignment.CENTER
    assert widget.style.bold is True


def test_load_dashboard_applies_defaults(tmp_path: Path) -> None:
    dashboard_file = tmp_path / "dashboard.yaml"
    dashboard_file.write_text(
        """
title: Defaults
pages:
  - id: main
    title: Main
    widgets:
      - id: headline
        type: TEXT
        label: Headline
""".strip(),
        encoding="utf-8",
    )

    dashboard = load_dashboard(dashboard_file)

    assert dashboard.pages[0].layout.rows == 1
    assert dashboard.pages[0].layout.columns == 1
    assert dashboard.pages[0].widgets[0].style.alignment is Alignment.LEFT
