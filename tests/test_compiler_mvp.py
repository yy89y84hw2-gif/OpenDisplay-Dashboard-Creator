import json
import tempfile
import unittest
from pathlib import Path

from compiler import CompileError, compile_dashboard, compile_dashboard_json
from exporter import export_dashboard_json


DASHBOARD_YAML = """
name: Demo dashboard
widgets:
  - id: title
    type: text
    label: Welcome
  - id: metric
    type: number
    value: 42
"""


class CompilerMvpTest(unittest.TestCase):
    def test_compiles_supported_dashboard_yaml_to_json_ready_mapping(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "dashboard.yaml"
            source.write_text(DASHBOARD_YAML, encoding="utf-8")

            compiled = compile_dashboard(source)

        self.assertEqual(compiled["name"], "Demo dashboard")
        self.assertEqual(compiled["type"], "dashboard")
        self.assertEqual(compiled["version"], 1)
        self.assertEqual(compiled["widgets"][1]["value"], 42)

    def test_compiled_json_is_stable_and_parseable(self):
        compiled = compile_dashboard_json({"name": "Demo", "widgets": []})

        self.assertEqual(json.loads(compiled), {"name": "Demo", "type": "dashboard", "version": 1, "widgets": []})

    def test_exporter_writes_compiled_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "dashboard.yaml"
            destination = Path(tmpdir) / "dashboard.json"
            source.write_text(DASHBOARD_YAML, encoding="utf-8")

            returned = export_dashboard_json(source, destination)

            self.assertEqual(returned, destination)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["widgets"][0]["id"], "title")

    def test_rejects_empty_yaml(self):
        with self.assertRaises(CompileError):
            compile_dashboard_json({})


if __name__ == "__main__":
    unittest.main()
