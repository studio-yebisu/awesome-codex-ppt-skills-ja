"""SlideFly -> PPTX: Tabler icons as native PowerPoint shapes (SVG outline -> DrawingML custGeom).

Tabler icons are 24x24 stroked outlines (path, circle, rect, line, polyline, polygon, ellipse).
Each becomes one sub-path of a custom geometry, stroked in the icon colour, no fill: it recolours and
scales like any shape and needs no picture fallback. Arcs are converted to cubic Béziers.
"""
import math
import re

S = 1000   # path units per SVG unit (24x24 -> 24000)


def _arc(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """SVG endpoint arc -> list of cubic segments (each 3 points)."""
    if rx == 0 or ry == 0:
        return [[(x2, y2), (x2, y2), (x2, y2)]]
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = c * dx + s * dy, -s * dx + c * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    co = math.sqrt(max(0, num / (rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2))) * (-1 if fa == fs else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cy = c * cxp - s * cyp + (x1 + x2) / 2, s * cxp + c * cyp + (y1 + y2) / 2
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)  # noqa: E731
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(1, math.ceil(abs(dt) / (math.pi / 2)))
    d, out = dt / n, []
    k = 4 / 3 * math.tan(d / 4)
    pt = lambda t: (cx + rx * math.cos(t) * c - ry * math.sin(t) * s, cy + rx * math.cos(t) * s + ry * math.sin(t) * c)  # noqa: E731
    der = lambda t: (-rx * math.sin(t) * c - ry * math.cos(t) * s, -rx * math.sin(t) * s + ry * math.cos(t) * c)  # noqa: E731
    for i in range(n):
        a, b = t1 + i * d, t1 + (i + 1) * d
        p0, p3, d0, d3 = pt(a), pt(b), der(a), der(b)
        out.append([(p0[0] + k * d0[0], p0[1] + k * d0[1]), (p3[0] - k * d3[0], p3[1] - k * d3[1]), p3])
    return out


def path_cmds(d):
    """SVG path data -> list of ('M'|'L'|'C'|'Z', points)."""
    toks = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?', d)
    out, i, cur, start, cmd, prev_c = [], 0, (0.0, 0.0), (0.0, 0.0), None, None
    while i < len(toks):
        if re.match(r'[A-Za-z]', toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in 'Zz':
                out.append(('Z', []))
                cur = start
                continue
        rel = cmd.islower()
        C = cmd.upper()
        take = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'A': 7}[C]
        v = [float(t) for t in toks[i:i + take]]
        i += take
        ox, oy = cur if rel else (0, 0)
        if C in 'ML':
            p = (v[0] + ox, v[1] + oy)
            out.append((('M' if C == 'M' else 'L'), [p]))
            if C == 'M':
                start, cmd = p, ('l' if rel else 'L')
            cur = p
        elif C in 'HV':
            cur = (v[0] + ox, cur[1]) if C == 'H' else (cur[0], v[0] + oy)
            out.append(('L', [cur]))
        elif C in 'CS':
            if C == 'S':
                c1 = (2 * cur[0] - prev_c[0], 2 * cur[1] - prev_c[1]) if prev_c else cur
                v = [c1[0] - ox, c1[1] - oy] + v
            pts = [(v[j] + ox, v[j + 1] + oy) for j in (0, 2, 4)]
            out.append(('C', pts))
            prev_c, cur = pts[1], pts[2]
            continue
        elif C in 'QT':
            q = (v[0] + ox, v[1] + oy) if C == 'Q' else cur
            e = (v[-2] + ox, v[-1] + oy)
            out.append(('C', [(cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1])),
                              (e[0] + 2 / 3 * (q[0] - e[0]), e[1] + 2 / 3 * (q[1] - e[1])), e]))
            cur = e
        elif C == 'A':
            e = (v[5] + ox, v[6] + oy)
            out += [('C', seg) for seg in _arc(cur[0], cur[1], v[0], v[1], v[2], int(v[3]), int(v[4]), e[0], e[1])]
            cur = e
        prev_c = None
    return out


def ellipse(cx, cy, rx, ry):
    return [('M', [(cx + rx, cy)])] + [('C', s) for s in _arc(cx + rx, cy, rx, ry, 0, 0, 1, cx - rx, cy)] + \
           [('C', s) for s in _arc(cx - rx, cy, rx, ry, 0, 0, 1, cx + rx, cy)] + [('Z', [])]


def shapes(svg):
    """All drawable elements of an icon SVG -> list of command lists (skips the invisible bounding path)."""
    out = []
    for tag, attrs in re.findall(r'<(path|circle|rect|line|polyline|polygon|ellipse)\b([^>]*)/?>', svg):
        a = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
        if a.get('stroke') == 'none' and a.get('fill', 'none') == 'none':
            continue
        f = lambda k: float(a.get(k, 0))  # noqa: E731
        if tag == 'path':
            out.append(path_cmds(a.get('d', '')))
        elif tag in ('circle', 'ellipse'):
            out.append(ellipse(f('cx'), f('cy'), f('r') or f('rx'), f('r') or f('ry')))
        elif tag == 'rect':
            x, y, w, h = f('x'), f('y'), f('width'), f('height')
            out.append(path_cmds(f'M{x} {y}h{w}v{h}h{-w}z'))
        elif tag == 'line':
            out.append([('M', [(f('x1'), f('y1'))]), ('L', [(f('x2'), f('y2'))])])
        else:
            pts = [float(p) for p in re.split(r'[\s,]+', a.get('points', '').strip()) if p]
            cmds = [('M', [(pts[0], pts[1])])] + [('L', [(pts[j], pts[j + 1])]) for j in range(2, len(pts) - 1, 2)]
            out.append(cmds + ([('Z', [])] if tag == 'polygon' else []))
    return out


def geom(svg):
    """custGeom XML (24x24 viewBox) for an icon, stroked only."""
    paths = ''
    for cmds in shapes(svg):
        body = ''
        for c, pts in cmds:
            p = ''.join(f'<a:pt x="{int(x * S)}" y="{int(y * S)}"/>' for x, y in pts)
            body += {'M': f'<a:moveTo>{p}</a:moveTo>', 'L': f'<a:lnTo>{p}</a:lnTo>', 'C': f'<a:cubicBezTo>{p}</a:cubicBezTo>', 'Z': '<a:close/>'}[c]
        paths += f'<a:path w="{24 * S}" h="{24 * S}" fill="none">{body}</a:path>'
    return ('<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>'
            f'<a:pathLst>{paths}</a:pathLst></a:custGeom>')


def rebuild(node):
    """Serialize a DOM subtree back to markup (enough for an inline icon SVG)."""
    attrs = ''.join(f' {k}="{v}"' for k, v in node.attrs.items() if v is not None)
    inner = ''.join(k if isinstance(k, str) else rebuild(k) for k in node.kids)
    return f'<{node.tag}{attrs}>{inner}</{node.tag}>'


def place(ctx, node, x, y, size, role='accent'):
    """A Tabler <i class="ico" data-icon> as a stroked custom shape (inline SVG, else the icons.py cache/CDN)."""
    if not node or not node.attrs.get('data-icon'):
        return
    inner = node.find(lambda n: n.tag == 'svg')
    if inner is None:
        try:
            import icons
            svg = icons.fetch_svg(node.attrs['data-icon'], node.attrs.get('data-style', 'outline'))
        except Exception:   # offline or unknown name: leave the icon out
            return
    else:
        svg = rebuild(inner)
    col = ctx.t[role] if isinstance(role, str) else role
    ctx.items.append({'name': 'Icon ' + node.attrs['data-icon'], 'x': x, 'y': y, 'w': size, 'h': size, 'fill': None, 'round': True,
                      'geom': ('raw', geom(svg)), 'line': (col, max(1.5, size / 24 * 1.75)), 'anim': True,
                      'src': node})   # appears with the element that holds it (pptx_anim)
