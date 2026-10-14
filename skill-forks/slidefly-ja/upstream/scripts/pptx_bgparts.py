"""SlideFly -> PPTX: pieces of the CSS background compiler (pptx_bgsvg): colours, gradient stops, angles,
inline SVG data URIs."""
import base64
import math
import re
from urllib.parse import unquote

from pptx_css import color, px, resolve


def _col(v, tok):
    c = color(resolve(v, [tok])) if v else None
    return c or ('000000', 0)


def _stops(args, tok, length):
    """'color [pos [pos]]' list -> [(offset 0..1, hex, alpha)] with CSS defaults for missing positions."""
    raw = []
    for a in args:
        m = re.match(r'(.+?)((?:\s+-?[\d.]+(?:px|%)?){0,2})\s*$', a.strip())
        c, pos = (m.group(1), m.group(2).split()) if m else (a, [])
        hexa = _col(c.strip(), tok)
        ps = [(px(p) / 100 * length if p.endswith('%') else px(p)) for p in pos] or [None]
        raw += [(p, hexa) for p in ps]
    if raw[0][0] is None:
        raw[0] = (0, raw[0][1])
    if raw[-1][0] is None:
        raw[-1] = (length, raw[-1][1])
    out, last = [], 0
    for i, (p, c) in enumerate(raw):   # missing positions: spread evenly between known neighbours
        if p is None:
            j = next(k for k in range(i, len(raw)) if raw[k][0] is not None)
            p = last + (raw[j][0] - last) / (j - i + 1)
        p = max(p, last)
        out.append((p, c))
        last = p
    return [(p / length if length else 0, c[0], c[1]) for p, c in out]


def _grad_xml(gid, kind, stops, attrs):
    st = ''.join(f'<stop offset="{max(0, min(1, o)):.4f}" stop-color="#{h}" stop-opacity="{a:.3f}"/>' for o, h, a in stops)
    return f'<{kind} id="{gid}" gradientUnits="userSpaceOnUse" {attrs}>{st}</{kind}>'


def _angle(first):
    sides = {'to top': 0, 'to right': 90, 'to bottom': 180, 'to left': 270, 'to top right': 45, 'to right top': 45,
             'to bottom right': 135, 'to right bottom': 135, 'to bottom left': 225, 'to left bottom': 225, 'to top left': 315, 'to left top': 315}
    f = first.strip()
    if f in sides:
        return sides[f], True
    m = re.fullmatch(r'(-?[\d.]+)(deg|turn|rad)', f)
    if m:
        v = float(m.group(1))
        return (v * 360 if m.group(2) == 'turn' else math.degrees(v) if m.group(2) == 'rad' else v), True
    return 180, False


def _conic(args, rep, tw, th, tok):
    """(repeating-)conic-gradient -> wedges of solid colour (hard stops, as the styles use it for sunbursts)."""
    head = args[0] if re.match(r'\s*(from|at)\b', args[0]) else ''
    args = args[1:] if head else args
    frm = re.search(r'from\s+(-?[\d.]+)deg', head)
    at = re.search(r'at\s+(\S+)\s+(\S+)', head)
    one = lambda v, full: px(v) / 100 * full if v.endswith('%') else px(v)  # noqa: E731
    cx, cy = (one(at.group(1), tw), one(at.group(2), th)) if at else (tw / 2, th / 2)
    start, segs, last = float(frm.group(1)) if frm else 0, [], 0
    for a in args:   # 'color a1 [a2]' in degrees
        m = re.match(r'(.+?)\s+(-?[\d.]+)deg(?:\s+(-?[\d.]+)deg)?\s*$', a.strip())
        if not m:
            continue
        a1, a2 = float(m.group(2)), float(m.group(3)) if m.group(3) else None
        segs.append((last if a2 is None else a1, a1 if a2 is None else a2, _col(m.group(1), tok)))
        last = a1 if a2 is None else a2
    period = last if rep and last > 0 else 360
    r, out = math.hypot(tw, th) * 2, ''
    for k in range(int(360 / period) + 1 if rep else 1):
        for a1, a2, (hexv, al) in segs:
            if al <= 0.01:
                continue
            p = [(cx + r * math.sin(math.radians(start + k * period + t)), cy - r * math.cos(math.radians(start + k * period + t))) for t in (a1, a2)]
            out += f'<polygon points="{cx:.1f},{cy:.1f} {p[0][0]:.1f},{p[0][1]:.1f} {p[1][0]:.1f},{p[1][1]:.1f}" fill="#{hexv}" fill-opacity="{al:.3f}"/>'
    return out


def _svg_doc(url):
    """data:image/svg+xml URL -> (viewBox, preserveAspectRatio, inner markup) or None."""
    m = re.match(r"""url\(\s*['"]?data:image/svg\+xml(;base64)?,(.*?)['"]?\s*\)$""", url.strip(), re.S)
    if not m:
        return None
    text = base64.b64decode(m.group(2)).decode('utf-8', 'ignore') if m.group(1) else unquote(m.group(2))
    root = re.search(r'<svg\b([^>]*)>(.*)</svg>', text, re.S)
    if not root:
        return None
    vb = re.search(r'viewBox=["\']([^"\']+)', root.group(1))
    par = re.search(r'preserveAspectRatio=["\']([^"\']+)', root.group(1))
    if not vb:
        w, h = (re.search(rf'{k}=["\']([\d.]+)', root.group(1)) for k in ('width', 'height'))
        vb = f'0 0 {w.group(1) if w else 100} {h.group(1) if h else 100}'
    return (vb if isinstance(vb, str) else vb.group(1)), (par.group(1) if par else 'xMidYMid meet'), root.group(2)
