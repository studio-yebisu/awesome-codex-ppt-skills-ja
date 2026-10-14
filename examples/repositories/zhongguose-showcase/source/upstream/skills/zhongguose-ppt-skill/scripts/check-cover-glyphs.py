#!/usr/bin/env python3
"""Verify that a generated WOFF2 contains every requested Unicode character."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path, help="Path to the generated WOFF2 file")
    parser.add_argument(
        "--text",
        action="append",
        required=True,
        help="Text whose characters must exist; repeat for multiple labels",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    font_path = args.font.resolve()
    if not font_path.is_file():
        raise SystemExit(f"Font not found: {font_path}")

    font = TTFont(font_path)
    codepoints = {
        codepoint
        for table in font["cmap"].tables
        for codepoint in table.cmap
    }

    failures: list[str] = []
    for text in args.text:
        missing = "".join(
            character
            for character in dict.fromkeys(text)
            if not character.isspace() and ord(character) not in codepoints
        )
        if missing:
            failures.append(f"{text}: {missing}")

    if failures:
        print("Cover-font glyph validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Cover-font glyph validation passed: {len(args.text)} text sample(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
