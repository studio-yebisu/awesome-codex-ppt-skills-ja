#!/usr/bin/env python3
"""Extract the dominant colours of an image, for mapping a brand palette.

When the brand reference is an image (a slide, a logo, a brand page), reading
hex values by eye is approximate. This samples the actual pixels and reports the
dominant colours with their share, plus rough suggestions for background / text /
accent, so the theme tokens can be set from real values.

    python3 image_colors.py brand.png
    python3 image_colors.py slide.jpg --colors 8

Prints JSON. Needs Pillow; if missing, it is installed into a dedicated venv
(`~/.cache/presentation-forge/venv`, never the system Python) automatically. If
that isn't possible (no network, sandboxed), it says so and you should read the
colours by eye instead.
"""

import argparse
import colorsys
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    try:
        from pf_venv import reexec_in_venv
        reexec_in_venv("pillow")
    except Exception:
        sys.exit(
            "error: Pillow is not installed and a dedicated venv could not be "
            "set up automatically.\n"
            "Either run `pip install pillow` yourself, or read the image's "
            "colours by eye and set the theme tokens manually."
        )


def hex_of(rgb):
    return "#%02x%02x%02x" % rgb


def dominant_colours(path: Path, k: int):
    img = Image.open(path).convert("RGB")
    img.thumbnail((240, 240))  # downscale: speed, and average out JPEG noise
    # Adaptive palette quantisation groups near-identical pixels into k clusters.
    q = img.quantize(colors=k, method=Image.Quantize.FASTOCTREE)
    palette = q.getpalette()
    counts = q.getcolors()  # list of (count, palette_index)
    total = sum(c for c, _ in counts)
    out = []
    for count, idx in sorted(counts, reverse=True):
        r, g, b = palette[idx * 3: idx * 3 + 3]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        out.append({
            "hex": hex_of((r, g, b)),
            "rgb": [r, g, b],
            "share": round(count / total, 4),
            "hsv": [round(h, 3), round(s, 3), round(v, 3)],
        })
    return out


def suggest(colours):
    """Rough role guesses; the caller refines by eye against the reference."""
    if not colours:
        return {}
    # Background: the largest area, usually light or a strong brand fill.
    bg = max(colours, key=lambda c: c["share"])
    # Text: the darkest colour with a meaningful share.
    text = min((c for c in colours if c["share"] >= 0.02), key=lambda c: c["hsv"][2],
               default=min(colours, key=lambda c: c["hsv"][2]))
    # Accent: the most vivid colour (saturation * value) that is not near-grey.
    vivid = [c for c in colours if c["hsv"][1] >= 0.25]
    accent = max(vivid, key=lambda c: c["hsv"][1] * c["hsv"][2], default=None)
    s = {"bg": bg["hex"], "ink": text["hex"]}
    if accent:
        s["accent"] = accent["hex"]
    return s


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("image", help="path to the image")
    ap.add_argument("--colors", type=int, default=6,
                    help="number of dominant colours to report (default 6)")
    args = ap.parse_args()

    path = Path(args.image)
    if not path.is_file():
        raise SystemExit(f"error: image not found: {path}")

    colours = dominant_colours(path, max(2, args.colors))
    report = {
        "image": str(path),
        "colors": colours,
        "suggested_tokens": suggest(colours),
    }
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
