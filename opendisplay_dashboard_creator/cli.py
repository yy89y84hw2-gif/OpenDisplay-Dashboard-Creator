"""Command line interface for dashboard compilation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .compiler import compile_dashboard
from .exporter import export_dashboard_json


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Compile an OpenDisplay dashboard YAML file to JSON.")
    parser.add_argument("source", help="Path to the dashboard YAML file to compile.")
    parser.add_argument("-o", "--output", help="Optional path where the JSON output should be written.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the dashboard compiler CLI."""

    args = build_parser().parse_args(argv)
    payload = compile_dashboard(args.source)
    rendered = export_dashboard_json(payload, Path(args.output) if args.output else None)
    if not args.output:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
