"""Command line entry point for the OpenDisplay dashboard compiler MVP."""

from __future__ import annotations

import argparse

from exporter import export_dashboard_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile an OpenDisplay dashboard YAML file to JSON.")
    parser.add_argument("source", help="Path to the dashboard YAML file.")
    parser.add_argument("destination", help="Path where the compiled JSON file will be written.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    export_dashboard_json(args.source, args.destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
