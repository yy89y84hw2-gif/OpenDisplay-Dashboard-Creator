"""Minimal CLI for compiling dashboard YAML to JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .compiler import DashboardValidationError, compile_dashboard
from .parser import DashboardParseError, parse_dashboard_yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="opendisplay-dashboard-compiler",
        description="Compile an OpenDisplay dashboard YAML file to JSON.",
    )
    parser.add_argument("input", type=Path, help="Path to the dashboard YAML file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to write JSON output. Defaults to stdout.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        dashboard = parse_dashboard_yaml(args.input)
        compiled = compile_dashboard(dashboard)
    except (DashboardParseError, DashboardValidationError) as exc:
        parser.exit(1, f"error: {exc}\n")

    output = json.dumps(compiled, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
