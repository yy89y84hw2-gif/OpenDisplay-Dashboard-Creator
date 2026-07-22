import pytest

from oddc.model import Dashboard, Layout, Page, Style, Widget, WidgetType
from oddc.validator import validate_dashboard


def test_validate_dashboard_accepts_minimal_valid_dashboard() -> None:
    dashboard = Dashboard(
        title="Valid",
        pages=[
            Page(
                id="home",
                title="Home",
                layout=Layout(),
                widgets=[
                    Widget(
                        id="welcome",
                        type=WidgetType.TEXT,
                        label="Welcome",
                        style=Style(),
                    )
                ],
            )
        ],
    )

    validate_dashboard(dashboard)


def test_validate_dashboard_requires_at_least_one_page() -> None:
    with pytest.raises(ValueError, match="at least one page"):
        validate_dashboard(Dashboard(title="Empty"))


def test_validate_dashboard_requires_page_title() -> None:
    dashboard = Dashboard(title="Invalid", pages=[Page(id="home", title="")])

    with pytest.raises(ValueError, match="Page 'home' must define a title"):
        validate_dashboard(dashboard)


def test_validate_dashboard_requires_widget_type() -> None:
    dashboard = Dashboard(
        title="Invalid",
        pages=[
            Page(
                id="home",
                title="Home",
                widgets=[Widget(id="missing-type", type=None, label="Missing type")],  # type: ignore[arg-type]
            )
        ],
    )

    with pytest.raises(ValueError, match="Widget 'missing-type' must define a type"):
        validate_dashboard(dashboard)


def test_validate_dashboard_requires_widget_label() -> None:
    dashboard = Dashboard(
        title="Invalid",
        pages=[
            Page(
                id="home",
                title="Home",
                widgets=[Widget(id="missing-label", type=WidgetType.TEXT, label="")],
            )
        ],
    )

    with pytest.raises(ValueError, match="Widget 'missing-label' must define a label"):
        validate_dashboard(dashboard)
