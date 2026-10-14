#!/usr/bin/env python3
"""Build a deck-specific WOFF2 cover font and a reproducibility manifest."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = SKILL_DIR / "assets" / "font-sources" / "qijic-original.ttf.gz"
DEFAULT_LICENSE = SKILL_DIR / "assets" / "font-sources" / "OFL-1.1.txt"
DEFAULT_NOTICE = SKILL_DIR / "assets" / "font-sources" / "FONT-NOTICE.txt"
DEFAULT_OUTPUT_RELATIVE = Path("assets/fonts/zhongguose-cover.woff2")
MANIFEST_NAME = "zhongguose-cover.manifest.json"
ORIGINAL_TTF_SHA256 = "ea2a8e8e750c420e9698df54d63a1eef24ac76eca53b1d17a4714935965f818b"
SOURCE_ARCHIVE_SHA256 = "1e2dfe3e99eae69c90a0ea16fa24def2d254cd6914ef5f428677bcc43e6ce023"
PRIMARY_NAME_IDS = {1, 3, 4, 6, 16, 17, 21, 22}
SKIP_TAGS = {"script", "style", "noscript", "template"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
COVER_FONT_TEXT_ATTRIBUTE = "data-cover-font-text"


def is_han_codepoint(codepoint: int) -> bool:
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x20000 <= codepoint <= 0x2FA1F
        or 0x30000 <= codepoint <= 0x323AF
    )


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[tuple[str, bool, bool]] = []
        self._skip_depth = 0
        self._cover_depth = 0
        self.visible_parts: list[str] = []
        self.cover_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_name = tag.lower()
        starts_skip = tag_name in SKIP_TAGS
        attribute_map = {key.lower(): value or "" for key, value in attrs}
        classes = attribute_map.get("class", "")
        starts_cover = "cover-title" in classes.split()
        cover_font_text = attribute_map.get(COVER_FONT_TEXT_ATTRIBUTE, "").strip()
        if cover_font_text:
            self.visible_parts.append(cover_font_text)
            self.cover_parts.append(cover_font_text)
        if tag_name in VOID_TAGS:
            return
        self._stack.append((tag_name, starts_skip, starts_cover))
        if starts_skip:
            self._skip_depth += 1
        if starts_cover:
            self._cover_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if not self._stack:
            return
        _, starts_skip, starts_cover = self._stack.pop()
        if starts_skip:
            self._skip_depth = max(0, self._skip_depth - 1)
        if starts_cover:
            self._cover_depth = max(0, self._cover_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._skip_depth or not data:
            return
        self.visible_parts.append(data)
        if self._cover_depth:
            self.cover_parts.append(data)


def parse_html_text(path: Path) -> tuple[str, str]:
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8-sig"))
    parser.close()
    return "".join(parser.visible_parts), "".join(parser.cover_parts)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_license_files(output_dir: Path) -> None:
    for source in (DEFAULT_LICENSE, DEFAULT_NOTICE):
        if not source.is_file():
            raise FileNotFoundError(f"Required font license file is missing: {source}")
        shutil.copyfile(source, output_dir / source.name)


def rename_modified_font(font: object) -> None:
    name_table = font["name"]
    replaced_ids = {0, 1, 2, 3, 4, 5, 6, 13, 14, 16, 17, 21, 22}
    name_table.names = [record for record in name_table.names if record.nameID not in replaced_ids]

    values = {
        0: "Copyright (c) 2020, Lingdong Huang. Modified and redistributed under SIL OFL 1.1.",
        1: "Zhongguose Cover",
        2: "Regular",
        3: "ZhongguoseCover-Regular;1.000",
        4: "Zhongguose Cover Regular",
        5: "Version 1.000",
        6: "ZhongguoseCover-Regular",
        13: (
            "Licensed under the SIL Open Font License, Version 1.1. "
            "This is a Modified Version and does not use the Reserved Font Name QIJI as its primary font name."
        ),
        14: "https://openfontlicense.org",
        16: "Zhongguose Cover",
        17: "Regular",
        21: "Zhongguose Cover",
        22: "Regular",
    }
    for name_id, value in values.items():
        name_table.setName(value, name_id, 3, 1, 0x0409)
        name_table.setName(value, name_id, 1, 0, 0)


def load_fonttools() -> tuple[object, object] | tuple[None, None]:
    try:
        import brotli  # noqa: F401
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except (ImportError, ModuleNotFoundError):
        return None, None
    return subset, TTFont


def build_subset(source: Path, output: Path, text: str, cover_text: str) -> tuple[set[int], int]:
    subset_module, ttfont_class = load_fonttools()
    if subset_module is None or ttfont_class is None:
        raise RuntimeError(
            "FontTools with Brotli support is required. Install it with: "
            'python -m pip install "fonttools[woff]"'
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    unpacked_source: Path | None = None
    try:
        actual_source = source
        if source.name.lower().endswith(".ttf.gz"):
            if source.resolve() == DEFAULT_SOURCE.resolve() and sha256_bytes(source.read_bytes()) != SOURCE_ARCHIVE_SHA256:
                raise RuntimeError("Bundled source archive SHA-256 does not match the pinned value.")
            handle, unpacked_name = tempfile.mkstemp(
                prefix=".zhongguose-cover-source-", suffix=".ttf", dir=output.parent
            )
            os.close(handle)
            unpacked_source = Path(unpacked_name)
            with gzip.open(source, "rb") as compressed, unpacked_source.open("wb") as target:
                shutil.copyfileobj(compressed, target)
            if source.resolve() == DEFAULT_SOURCE.resolve() and sha256_bytes(unpacked_source.read_bytes()) != ORIGINAL_TTF_SHA256:
                raise RuntimeError("Unpacked source TTF SHA-256 does not match the pinned original.")
            actual_source = unpacked_source

        font = ttfont_class(str(actual_source), recalcTimestamp=False, lazy=False)
        source_cmap = font.getBestCmap() or {}
        requested = {ord(char) for char in text if not char.isspace()}
        missing = requested.difference(source_cmap)
        missing_cover = {ord(char) for char in cover_text if not char.isspace()}.difference(source_cmap)
        missing_cover_han = {codepoint for codepoint in missing_cover if is_han_codepoint(codepoint)}
        if missing_cover_han:
            preview = "".join(chr(codepoint) for codepoint in sorted(missing_cover_han)[:24])
            raise RuntimeError(f"The source font is missing cover-title Han characters: {preview}")

        options = subset_module.Options()
        options.flavor = "woff2"
        options.with_zopfli = False
        options.retain_gids = False
        options.notdef_glyph = True
        options.notdef_outline = True
        options.recommended_glyphs = True
        options.layout_features = ["*"]
        options.name_legacy = True
        options.recalc_timestamp = False
        if "FFTM" not in options.drop_tables:
            options.drop_tables.append("FFTM")

        subsetter = subset_module.Subsetter(options=options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        rename_modified_font(font)
        font.flavor = "woff2"

        output.parent.mkdir(parents=True, exist_ok=True)
        handle, temp_name = tempfile.mkstemp(prefix=f".{output.stem}-", suffix=".woff2", dir=output.parent)
        os.close(handle)
        temp_path = Path(temp_name)
        try:
            font.save(str(temp_path), reorderTables=True)
            if temp_path.read_bytes()[:4] != b"wOF2":
                raise RuntimeError("Generated font does not have a valid WOFF2 signature.")
            check_font = ttfont_class(str(temp_path), recalcTimestamp=False, lazy=False)
            primary_names = [
                record.toUnicode()
                for record in check_font["name"].names
                if record.nameID in PRIMARY_NAME_IDS
            ]
            if any("QIJI" in value.upper() for value in primary_names):
                raise RuntimeError("Generated font still uses the upstream Reserved Font Name in a primary name field.")
            present_name_ids = {record.nameID for record in check_font["name"].names}
            if 13 not in present_name_ids or 14 not in present_name_ids:
                raise RuntimeError("Generated font is missing OFL license metadata.")
            check_font.close()
            temp_path.replace(output)
        finally:
            font.close()
            temp_path.unlink(missing_ok=True)

        return missing, len(source_cmap)
    finally:
        if unpacked_source is not None:
            unpacked_source.unlink(missing_ok=True)


def write_manifest(html_path: Path, font_path: Path, mode: str, visible_text: str) -> Path:
    import brotli
    import fontTools

    html_bytes = html_path.read_bytes()
    font_bytes = font_path.read_bytes()
    unique_characters = sorted({char for char in visible_text if not char.isspace()})
    manifest = {
        "schema": 1,
        "mode": mode,
        "html_sha256": sha256_bytes(html_bytes),
        "font_file": font_path.name,
        "font_sha256": sha256_bytes(font_bytes),
        "font_bytes": len(font_bytes),
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_ttf_sha256": ORIGINAL_TTF_SHA256,
        "fonttools_version": fontTools.__version__,
        "brotli_version": getattr(brotli, "__version__", "unknown"),
        "visible_character_count": len(unique_characters),
        "visible_characters_sha256": sha256_bytes("".join(unique_characters).encode("utf-8")),
    }
    manifest_path = font_path.parent / MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a deck-specific Zhongguose Cover WOFF2 font from visible HTML text."
    )
    parser.add_argument("html", type=Path, help="Path to the deck index.html")
    parser.add_argument("--include-html", action="append", default=[], type=Path, help="Additional HTML text to include")
    parser.add_argument("--extra-text", action="append", default=[], help="Additional literal characters to include")
    parser.add_argument("--extra-text-file", action="append", default=[], type=Path, help="UTF-8 text file to include")
    parser.add_argument(
        "--source-font",
        type=Path,
        default=DEFAULT_SOURCE,
        help="TTF, OTF, WOFF2, or gzip-compressed TTF source font",
    )
    parser.add_argument("--output", type=Path, help="Output WOFF2 path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    html_path = args.html.resolve()
    if not html_path.is_file():
        raise FileNotFoundError(f"Deck HTML not found: {html_path}")

    source = args.source_font.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Full source font not found: {source}")

    output = args.output.resolve() if args.output else html_path.parent / DEFAULT_OUTPUT_RELATIVE
    visible_text, cover_text = parse_html_text(html_path)
    all_text = [visible_text, " "]
    for extra_html in args.include_html:
        extra_visible, _ = parse_html_text(extra_html.resolve())
        all_text.append(extra_visible)
    all_text.extend(args.extra_text)
    for extra_file in args.extra_text_file:
        all_text.append(extra_file.resolve().read_text(encoding="utf-8-sig"))
    combined_text = "".join(all_text)

    missing, source_codepoints = build_subset(source, output, combined_text, cover_text)
    mode = "subset"

    copy_license_files(output.parent)
    manifest_path = write_manifest(html_path, output, mode, combined_text)

    print(f"Cover font ready: {output}")
    print(f"Mode: {mode}")
    print(f"WOFF2 bytes: {output.stat().st_size}")
    print(f"Visible unique characters: {len({char for char in combined_text if not char.isspace()})}")
    if source_codepoints:
        print(f"Source Unicode code points: {source_codepoints}")
    if missing:
        preview = "".join(chr(codepoint) for codepoint in sorted(missing)[:24])
        print(f"Warning: {len(missing)} visible character(s) are absent from the source font: {preview}")
    print(f"Manifest: {manifest_path}")
    print("License files copied beside the font.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, UnicodeError) as error:
        print(f"Font preparation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
