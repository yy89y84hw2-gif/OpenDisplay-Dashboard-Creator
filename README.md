# OpenDisplay-Dashboard-Creator

MVP compiler for creating OpenDisplay dashboard JSON from a YAML dashboard definition.

## YAML input

```yaml
title: Operations
widgets:
  - id: cpu
    type: metric
    label: CPU usage
    position:
      x: 0
      y: 0
      w: 4
      h: 2
```

## CLI

Compile YAML to stdout:

```bash
opendisplay-dashboard-compiler dashboard.yaml
```

Compile YAML to a JSON file:

```bash
opendisplay-dashboard-compiler dashboard.yaml --output dashboard.json
```

The MVP validates the dashboard title, widget list, required widget `id` and `type`, and optional widget positions before exporting JSON.
