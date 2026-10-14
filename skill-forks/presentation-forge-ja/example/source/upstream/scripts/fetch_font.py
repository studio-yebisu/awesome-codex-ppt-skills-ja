#!/usr/bin/env python3
"""Download a web font from Google Fonts and emit @font-face CSS for a theme.

Capturing a brand means using its real fonts, not a system fallback. When the
brand font is on Google Fonts (free), this fetches the actual .woff2 files into a
theme's fonts/ folder and prints ready-to-paste @font-face rules pointing at the
local files, so the built deck looks identical offline.

    python3 fetch_font.py "Montserrat" --weights 400,700 --out themes/acme/fonts
    python3 fetch_font.py "IBM Plex Serif" --out /tmp/f --css-only

If the family is not on Google Fonts (a commercial or custom face), it says so;
ask the user for the .woff2 files instead, or pick the closest free alternative.

Needs network access (fine in Claude Code; may be restricted in the app sandbox).
Standard library only.
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# A modern desktop UA so the CSS API serves woff2 (it varies output by UA).
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
CSS2 = "https://fonts.googleapis.com/css2"
# Subsets worth keeping for slide decks (latin-ext covers French accents).
DEFAULT_SUBSETS = ("latin", "latin-ext")
FACE_RE = re.compile(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", re.DOTALL)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fetch_css(family: str, weights: list[str]) -> str:
    spec = urllib.parse.quote(family) + ":wght@" + ";".join(weights)
    url = f"{CSS2}?family={spec}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise SystemExit(
                f"'{family}' (weights {','.join(weights)}) was not found on "
                "Google Fonts. Check the exact family name and weights, or ask "
                "the user for the .woff2 files (commercial/custom font)."
            )
        raise SystemExit(f"error: Google Fonts request failed: {e}")
    except urllib.error.URLError as e:
        raise SystemExit(f"error: no network access to Google Fonts: {e.reason}")


def parse_faces(css: str, subsets):
    faces = []
    for subset, block in FACE_RE.findall(css):
        if subsets and subset not in subsets:
            continue
        weight = re.search(r"font-weight:\s*(\d+)", block)
        style = re.search(r"font-style:\s*(\w+)", block)
        url = re.search(r"url\(([^)]+)\)\s*format\(['\"]woff2['\"]\)", block)
        urange = re.search(r"unicode-range:\s*([^;]+);", block)
        if not url:
            continue
        faces.append({
            "subset": subset,
            "weight": weight.group(1) if weight else "400",
            "style": style.group(1) if style else "normal",
            "url": url.group(1).strip("'\""),
            "unicode_range": urange.group(1).strip() if urange else None,
        })
    return faces


def merge_variable(faces):
    """Fold the weights of a variable font into one face per subset.

    For a variable font, Google Fonts answers every requested weight with the
    very same file. Downloading it once per weight would embed identical
    copies in every deck; instead keep one file per subset and declare the
    weight range (font-weight: 400 700), which the browser maps onto the
    font's weight axis."""
    merged = {}
    for f in faces:
        key = (f["style"], f["subset"], f["url"])
        if key in merged:
            merged[key]["weights"].append(f["weight"])
        else:
            merged[key] = dict(f, weights=[f["weight"]])
    for f in merged.values():
        f["weights"] = sorted(set(f["weights"]), key=int)
    return list(merged.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("family", help='font family, e.g. "Montserrat"')
    ap.add_argument("--weights", default="400,700",
                    help="comma-separated weights (default 400,700)")
    ap.add_argument("--out", default=".",
                    help="directory to write .woff2 into (theme fonts/ folder)")
    ap.add_argument("--subsets", default=",".join(DEFAULT_SUBSETS),
                    help="comma-separated subsets to keep (default latin,latin-ext)")
    ap.add_argument("--css-only", action="store_true",
                    help="print @font-face CSS without downloading the files")
    args = ap.parse_args()

    weights = [w.strip() for w in args.weights.split(",") if w.strip()]
    subsets = tuple(s.strip() for s in args.subsets.split(",") if s.strip())
    css = fetch_css(args.family, weights)
    faces = parse_faces(css, subsets)
    if not faces:
        raise SystemExit(f"error: no matching woff2 faces for '{args.family}'.")

    out = Path(args.out)
    rules = []
    files = 0
    for f in merge_variable(faces):
        weights = f["weights"]
        span = weights[0] if len(weights) == 1 else f"{weights[0]}-{weights[-1]}"
        fname = f"{slug(args.family)}-{span}-{f['style']}-{f['subset']}.woff2"
        if not args.css_only:
            out.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(f["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                (out / fname).write_bytes(r.read())
        # One @font-face per subset, each with its unicode-range, so the browser
        # loads the right file per glyph (latin-ext carries the accents).
        urange = (f"  unicode-range: {f['unicode_range']};\n"
                  if f["unicode_range"] else "")
        rules.append(
            f"@font-face {{\n"
            f"  font-family: \"{args.family}\";\n"
            f"  font-style: {f['style']};\n"
            f"  font-weight: {span.replace('-', ' ')};\n"
            f"  font-display: swap;\n"
            f"  src: url(\"fonts/{fname}\") format(\"woff2\");\n"
            f"{urange}"
            f"}}"
        )
        files += 1

    if not args.css_only:
        print(f"Downloaded {files} file(s) to {out}/", file=sys.stderr)
    print("\n".join(rules))
    print(f"\n/* In tokens.css, set the family name, e.g. "
          f"--font-sans: \"{args.family}\", system-ui, sans-serif; */",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
