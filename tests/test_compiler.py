import json

import pytest

from opendisplay_dashboard_creator.compiler import DashboardValidationError, compile_dashboard


def test_compile_dashboard_preserves_validated_widgets():
    dashboard = {
        "title": "Operations",
        "widgets": [
            {
                "id": "cpu",
                "type": "metric",
                "label": "CPU",
                "position": {"x": 0, "y": 0, "w": 4, "h": 2},
            }
        ],
    }

    compiled = compile_dashboard(dashboard)

    assert compiled == {
        "schema": "opendisplay.dashboard.v1",
        "title": "Operations",
        "widgets": [
            {
                "id": "cpu",
                "type": "metric",
                "label": "CPU",
                "position": {"x": 0, "y": 0, "w": 4, "h": 2},
            }
        ],
    }
    json.dumps(compiled)


@pytest.mark.parametrize(
    "dashboard, message",
    [
        ({"widgets": []}, "title"),
        ({"title": "Ops"}, "widgets"),
        ({"title": "Ops", "widgets": [{"id": "cpu"}]}, "type"),
        (
            {"title": "Ops", "widgets": [{"id": "cpu", "type": "metric", "position": {"x": -1}}]},
            "position 'x'",
        ),
    ],
)
def test_compile_dashboard_rejects_invalid_dashboard(dashboard, message):
    with pytest.raises(DashboardValidationError, match=message):
        compile_dashboard(dashboard)
