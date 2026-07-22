from opendisplay_dashboard_creator.compiler import compile_dashboard, export_json
from opendisplay_dashboard_creator.models import Dashboard, Layout, Widget
from opendisplay_dashboard_creator.parser import parse_dashboard_text


def test_compile_dashboard_exports_opendisplay_json():
    dashboard = Dashboard(
        title="Ops",
        widgets=(Widget(id="cpu", type="metric", title="CPU", source="prometheus", layout=Layout(width=2)),),
    )

    assert compile_dashboard(dashboard) == {
        "opendisplay": {
            "schemaVersion": "1",
            "dashboard": {
                "version": "1",
                "title": "Ops",
                "widgets": [
                    {
                        "id": "cpu",
                        "type": "metric",
                        "title": "CPU",
                        "source": "prometheus",
                        "layout": {"x": 0, "y": 0, "width": 2, "height": 1},
                        "options": {},
                    }
                ],
            },
        }
    }


def test_parse_dashboard_text_reuses_models():
    dashboard = parse_dashboard_text('{"title":"Ops","widgets":[{"id":"status","type":"text"}]}')

    assert dashboard.title == "Ops"
    assert dashboard.widgets[0].id == "status"


def test_export_json_writes_file(tmp_path):
    output = tmp_path / "dashboard.json"

    text = export_json({"ok": True}, output)

    assert text == '{\n  "ok": true\n}\n'
    assert output.read_text(encoding="utf-8") == text
