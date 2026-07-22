"""Minimal command line interface for the MVP compiler."""

from __future__ import annotations

import argparse
import sys

from .compiler import compile_file, export_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile an OpenDisplay dashboard definition to JSON.")
    parser.add_argument("input", help="Path to the dashboard definition JSON file.")
    parser.add_argument("-o", "--output", help="Path where the compiled JSON should be written.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    compiled = compile_file(args.input)
    text = export_json(compiled, args.output)
    if args.output is None:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
