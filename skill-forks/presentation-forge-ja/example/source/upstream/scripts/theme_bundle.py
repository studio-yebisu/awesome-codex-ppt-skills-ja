#!/usr/bin/env python3
"""Pack a Presentation Forge theme into one portable style file, or unpack it.

A theme folder IS the complete style: colours and type scale (`tokens.css`), the
layout and per-variant styling (`slides.css`), the web fonts (`fonts.css` +
`fonts/*.woff2`), the logo (`logos/`) and any backgrounds (`images/`). This packs
all of it, byte for byte, into a single self-contained `<name>.pfstyle.json`:
CSS stays as readable text, binary assets are base64, and a short human-readable
summary is included so you can see the palette and fonts at a glance. Nothing is
lost.

Hand that one file to someone (or to a future conversation) and `unpack` rebuilds
the exact same theme folder, with no need for the original images or PowerPoint.

    python3 theme_bundle.py pack   <deck>/themes/acme  -o acme.pfstyle.json
    python3 theme_bundle.py unpack acme.pfstyle.json   <deck>/themes  [--name acme]

Standard library only.
"""

import argparse
import base64
import datetime
import json
import re
import sys
from pathlib import Path

FORMAT = "presentation-forge-theme"
VERSION = 1
TEXT_EXT = {".css"}                      # stored as readable text; rest is base64
SKIP = {".DS_Store"}                     # OS junk, never part of the style


def _summary(files: dict) -> dict:
    """A readable preview derived from tokens.css and the asset list. Not the
    source of truth (that is `files`); just so a human can eyeball the style."""
    s = {"colors": {}, "fonts": {}, "logos": [], "backgrounds": []}
    tokens = files.get("tokens.css", {}).get("text", "")
    for name in ("--bg", "--ink", "--accent", "--accent-deep"):
        m = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", tokens)
        if m:
            s["colors"][name] = m.group(1).strip()
    for name in ("--font-sans", "--font-serif", "--font-mono"):
        m = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", tokens)
        if m:
            s["fonts"][name] = m.group(1).strip()
    for path in files:
        if path.startswith("logos/") and not path.endswith(".gitkeep"):
            s["logos"].append(path)
        elif path.startswith("images/") and not path.endswith(".gitkeep"):
            s["backgrounds"].append(path)
    return s


def pack(theme_dir: Path, out: Path | None) -> Path:
    if not theme_dir.is_dir():
        raise SystemExit(f"error: not a theme folder: {theme_dir}")
    files = {}
    for p in sorted(theme_dir.rglob("*")):
        if not p.is_file() or p.name in SKIP:
            continue
        rel = p.relative_to(theme_dir).as_posix()
        if p.suffix.lower() in TEXT_EXT:
            files[rel] = {"encoding": "utf-8", "text": p.read_text(encoding="utf-8")}
        else:
            files[rel] = {"encoding": "base64",
                          "data": base64.b64encode(p.read_bytes()).decode("ascii")}
    if not files:
        raise SystemExit(f"error: theme folder is empty: {theme_dir}")

    bundle = {
        "format": FORMAT,
        "version": VERSION,
        "name": theme_dir.name,
        "created": datetime.date.today().isoformat(),
        "summary": _summary(files),
        "files": files,
    }
    out = out or Path(f"{theme_dir.name}.pfstyle.json")
    out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    n_assets = sum(1 for f in files.values() if f["encoding"] == "base64")
    print(f"Packed theme '{theme_dir.name}' -> {out} "
          f"({len(files)} files, {n_assets} binary asset(s), "
          f"{out.stat().st_size // 1024} KB)")
    return out


def _safe_name(name: str) -> str:
    """A theme folder name must be a single, plain path component.

    The name can come from an untrusted style file, so reject anything that
    could escape the destination (separators, ``..``, absolute paths)."""
    if name in ("", ".", "..") or "/" in name or "\\" in name or Path(name).is_absolute():
        raise SystemExit(f"error: unsafe theme name in style file, refusing: {name!r}")
    return name


def _safe_member(base: Path, rel: str) -> Path:
    """Resolve ``rel`` under ``base``, refusing anything that escapes it.

    A ``.pfstyle.json`` is shared between people and across conversations, so its
    file keys are untrusted input. Reject absolute paths and ``..`` traversal so
    an unpack can never write outside the theme folder (zip-slip)."""
    dest = (base / rel).resolve()
    if dest != base and base not in dest.parents:
        raise SystemExit(f"error: unsafe path in style file, refusing: {rel!r}")
    return dest


def unpack(bundle_path: Path, dest_themes: Path, name: str | None) -> Path:
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"error: cannot read style file: {e}")
    if bundle.get("format") != FORMAT:
        raise SystemExit(f"error: not a {FORMAT} style file: {bundle_path}")

    theme_name = _safe_name(name or bundle.get("name") or "imported-theme")
    target = (dest_themes / theme_name).resolve()
    target.mkdir(parents=True, exist_ok=True)
    for rel, entry in bundle.get("files", {}).items():
        dest = _safe_member(target, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if entry.get("encoding") == "utf-8":
            dest.write_text(entry.get("text", ""), encoding="utf-8", newline="\n")
        else:
            dest.write_bytes(base64.b64decode(entry.get("data", "")))

    print(f"Unpacked style into {target}/")
    summ = bundle.get("summary", {})
    if summ:
        print("Summary:", json.dumps(summ, ensure_ascii=False))
    print(f'Next: set "theme": "{theme_name}" in deck.config.json, then build.')
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pack", help="pack a theme folder into a .pfstyle.json")
    p.add_argument("theme_dir", help="path to themes/<name>/")
    p.add_argument("-o", "--output", help="output .pfstyle.json path")

    u = sub.add_parser("unpack", help="rebuild a theme folder from a .pfstyle.json")
    u.add_argument("bundle", help="path to the .pfstyle.json")
    u.add_argument("dest_themes", help="the deck's themes/ directory")
    u.add_argument("--name", help="override the theme folder name")

    args = ap.parse_args()
    if args.cmd == "pack":
        pack(Path(args.theme_dir), Path(args.output) if args.output else None)
    else:
        unpack(Path(args.bundle), Path(args.dest_themes), args.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
