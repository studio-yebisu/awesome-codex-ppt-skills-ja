#!/usr/bin/env python3
"""Extract the *design language* of a PowerPoint (.pptx) for re-use as a
Presentation Forge theme.

A .pptx is just a zip of XML. This reads the parts that define the look - the
theme colour scheme, the major/minor fonts, the slide size - and lists the
embedded media (logos, backgrounds). It prints a JSON report and, with
``--dump-media``, copies the media files out so you can pick a logo / background.

It does NOT write the theme itself: mapping the palette onto theme tokens and
choosing which image is the logo is a judgement call left to the caller (the
skill's theme-import workflow). The point of this script is the deterministic,
boring extraction.

    python3 pptx_theme.py <file.pptx>                     # print JSON report
    python3 pptx_theme.py <file.pptx> --dump-media <dir>  # also extract media

Standard library only - no python-pptx, no Pillow, no pip install.
"""

import argparse
import json
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
EMU_PER_PX = 9525  # 914400 EMU/inch / 96 px/inch

# clrScheme child -> friendly name. dk1/lt1 are usually text/background.
COLOR_SLOTS = [
    "dk1", "lt1", "dk2", "lt2",
    "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
    "hlink", "folHlink",
]


def _color_from(el):
    """Read a hex colour from a clrScheme slot element (srgbClr or sysClr)."""
    if el is None:
        return None
    srgb = el.find(f"{A}srgbClr")
    if srgb is not None and srgb.get("val"):
        return "#" + srgb.get("val").lower()
    sysclr = el.find(f"{A}sysClr")
    if sysclr is not None and sysclr.get("lastClr"):
        return "#" + sysclr.get("lastClr").lower()
    return None


def _read_xml(zf, name):
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def extract_theme(zf):
    """Return {'palette': {...}, 'fonts': {...}} from the first theme part."""
    theme_names = sorted(n for n in zf.namelist()
                         if n.startswith("ppt/theme/") and n.endswith(".xml"))
    palette, fonts = {}, {}
    if not theme_names:
        return {"palette": palette, "fonts": fonts, "theme_part": None}
    root = _read_xml(zf, theme_names[0])
    if root is None:
        return {"palette": palette, "fonts": fonts, "theme_part": theme_names[0]}

    scheme = root.find(f".//{A}clrScheme")
    if scheme is not None:
        for slot in COLOR_SLOTS:
            hexv = _color_from(scheme.find(f"{A}{slot}"))
            if hexv:
                palette[slot] = hexv

    font_scheme = root.find(f".//{A}fontScheme")
    if font_scheme is not None:
        for kind in ("major", "minor"):
            latin = font_scheme.find(f"{A}{kind}Font/{A}latin")
            if latin is not None and latin.get("typeface"):
                fonts[kind] = latin.get("typeface")
    return {"palette": palette, "fonts": fonts, "theme_part": theme_names[0]}


def slide_size_px(zf):
    root = _read_xml(zf, "ppt/presentation.xml")
    if root is None:
        return None
    sz = root.find(f"{P}sldSz")
    if sz is None:
        return None
    try:
        w = round(int(sz.get("cx")) / EMU_PER_PX)
        h = round(int(sz.get("cy")) / EMU_PER_PX)
        return {"width": w, "height": h}
    except (TypeError, ValueError):
        return None


def _png_size(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return None


def _jpeg_size(data):
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    n = len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF markers carry the frame dimensions.
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg
    return None


def _img_size(data):
    try:
        return _png_size(data) or _jpeg_size(data)
    except Exception:
        return None


def media_list(zf):
    out = []
    for name in sorted(n for n in zf.namelist() if n.startswith("ppt/media/")):
        try:
            data = zf.read(name)
        except KeyError:
            continue
        dims = _img_size(data)
        out.append({
            "name": Path(name).name,
            "ext": Path(name).suffix.lower().lstrip("."),
            "bytes": len(data),
            "width": dims[0] if dims else None,
            "height": dims[1] if dims else None,
        })
    return out


def suggested_tokens(palette):
    """A rough mapping from the PPT palette to Presentation Forge token names.
    These are *suggestions*; refine by eye when writing tokens.css."""
    g = palette.get
    s = {}
    if g("lt1"):
        s["--bg"] = g("lt1")
    if g("lt2"):
        s["--bg-soft"] = g("lt2")
    if g("dk1"):
        s["--ink"] = g("dk1")
        s["--accent-deep"] = g("dk2", g("dk1"))
    if g("accent1"):
        s["--accent"] = g("accent1")
    if g("dk2"):
        s["--muted"] = g("dk2")
    return s


def _emu_px(v):
    try:
        return round(int(v) / EMU_PER_PX)
    except (TypeError, ValueError):
        return None


def _xfrm_box(sp):
    """Position/size (px) of a shape from its <a:xfrm>, or None."""
    xfrm = sp.find(f"{P}spPr/{A}xfrm")
    if xfrm is None:
        return None
    off, ext = xfrm.find(f"{A}off"), xfrm.find(f"{A}ext")
    if off is None or ext is None:
        return None
    return {"x": _emu_px(off.get("x")), "y": _emu_px(off.get("y")),
            "w": _emu_px(ext.get("cx")), "h": _emu_px(ext.get("cy"))}


def _rels_targets(zf, part_name):
    """Map relationship id -> media filename for a part's .rels."""
    base = part_name.rsplit("/", 1)
    rels = f"{base[0]}/_rels/{base[1]}.rels"
    out = {}
    root = _read_xml(zf, rels)
    if root is None:
        return out
    for rel in root:
        out[rel.get("Id")] = (rel.get("Target") or "").split("/")[-1]
    return out


def master_info(zf):
    """Best-effort layout signal from the slide master: background fill, the
    title/body placeholder boxes (px), and the default title/body font sizes
    (pt). Wrapped so a quirky deck never breaks the rest of the extraction."""
    names = sorted(n for n in zf.namelist()
                   if n.startswith("ppt/slideMasters/") and n.endswith(".xml"))
    if not names:
        return None
    try:
        name = names[0]
        root = _read_xml(zf, name)
        if root is None:
            return None
        info = {}

        bg = root.find(f"{P}cSld/{P}bg")
        if bg is not None:
            srgb = bg.find(f".//{A}solidFill/{A}srgbClr")
            if srgb is not None and srgb.get("val"):
                info["background"] = "#" + srgb.get("val").lower()
            else:
                blip = bg.find(f".//{A}blipFill/{A}blip")
                if blip is not None:
                    rid = blip.get(f"{REL}embed")
                    info["background_image"] = _rels_targets(zf, name).get(rid, True)

        sptree = root.find(f"{P}cSld/{P}spTree")
        if sptree is not None:
            for sp in sptree.findall(f"{P}sp"):
                ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
                ptype = ph.get("type") if ph is not None else "body"
                box = _xfrm_box(sp)
                if not box:
                    continue
                if ptype in ("title", "ctrTitle") and "title_box" not in info:
                    info["title_box"] = box
                elif ptype in ("body", "subTitle") and "body_box" not in info:
                    info["body_box"] = box

        def _sz(style):
            el = root.find(f"{P}txStyles/{P}{style}/{A}lvl1pPr/{A}defRPr")
            if el is not None and el.get("sz"):
                try:
                    return round(int(el.get("sz")) / 100)  # sz is in 1/100 pt
                except ValueError:
                    return None
            return None

        if _sz("titleStyle"):
            info["title_pt"] = _sz("titleStyle")
        if _sz("bodyStyle"):
            info["body_pt"] = _sz("bodyStyle")
        return info or None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pptx", help="path to the .pptx file")
    ap.add_argument("--dump-media", metavar="DIR",
                    help="extract ppt/media/* into DIR for inspection")
    args = ap.parse_args()

    path = Path(args.pptx)
    if not path.is_file():
        raise SystemExit(f"error: file not found: {path}")
    if not zipfile.is_zipfile(path):
        raise SystemExit(f"error: not a .pptx (zip) file: {path}")

    with zipfile.ZipFile(path) as zf:
        theme = extract_theme(zf)
        report = {
            "file": str(path),
            "slide_size_px": slide_size_px(zf),
            "palette": theme["palette"],
            "fonts": theme["fonts"],
            "suggested_tokens": suggested_tokens(theme["palette"]),
            "master": master_info(zf),
            "media": media_list(zf),
        }
        if args.dump_media:
            out = Path(args.dump_media)
            out.mkdir(parents=True, exist_ok=True)
            for name in zf.namelist():
                if name.startswith("ppt/media/"):
                    (out / Path(name).name).write_bytes(zf.read(name))
            report["media_dir"] = str(out)

    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
