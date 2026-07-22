# OpenDisplay-Dashboard-Creator

Utilities to create OpenDisplay dashboard payloads from strict YAML definitions.

## YAML format

```yaml
version: 1
title: Factory floor
pages:
  - id: overview
    title: Overview
    widgets:
      - id: temperature
        type: gauge
        title: Temperature
        x: 0
        y: 0
        width: 2
        height: 1
        config:
          unit: C
```

The parser is intentionally strict: unknown keys, invalid YAML, missing required
fields, duplicate IDs, and type mismatches raise `DashboardParserError` with a
message that identifies the failing field when possible.

## Development

The project targets Python 3.11 and keeps tooling aligned through
`pyproject.toml` (`requires-python`, Ruff `target-version`, and mypy
`python_version`).

Run the checks with:

```bash
python -m pytest -q
ruff check .
mypy opendisplay_dashboard_creator tests
```
