"""SlideFly -> PPTX: free-placed elements (data-layout="free" and inline-positioned blocks).

A block keeps its spot and takes its look from the deck CSS (rules made of its own classes) plus its inline style:
background, border, padding, colour, size, weight, alignment, display/mono face. Inline <svg> drawings become real
SVG pictures (PowerPoint 365 draws them as vectors; a 1x1 PNG is the fallback older versions show).
"""
import re
import struct
import zlib
from xml.sax.saxutils import escape, quoteattr

from pptx_css import color, px, resolve
from pptx_text import para, runs

SVG_PROPS = ('fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'stroke-dasharray', 'opacity', 'font-size',
             'font-family', 'font-weight', 'fill-opacity', 'stroke-opacity')


def class_decl(sheet, cls):
    """Rules whose last part is only classes the element has (`.box`, `.abs.box`), in cascade order."""
    have, out = set(cls), {}
    for sel, spec, order, dd in sorted(sheet.rules, key=lambda r: (r[1], r[2])):
        last = sel.split()[-1] if sel.split() else ''
        names = re.findall(r'\.([\w-]+)', last)
        if names and re.fullmatch(r'(\.[\w-]+)+', last) and set(names) <= have:
            out.update(dd)
    return out


def decl(ctx, node):
    """Deck CSS for the node's classes, then its inline style (inline wins)."""
    d = class_decl(ctx.sheet, node.cls) if getattr(ctx, 'sheet', None) else {}
    for k, v in re.findall(r'([\w-]+)\s*:\s*([^;]+)', node.attrs.get('style', '')):
        d[k.strip()] = v.strip()
    return d


def _col(ctx, v):
    if not v:
        return None
    if 'on-accent' in v:
        return ctx.t['on_accent']
    c = color(resolve(v, [getattr(ctx, 'tok', {})]))
    return c if c and c[1] > 0.02 else None


def free_box(ctx, k, spot):
    x, y, w, h = spot
    d = decl(ctx, k)
    font_sh = d.get('font', '')
    fs = px(d.get('font-size') or (re.search(r'(\d+(?:\.\d+)?)px', font_sh) or [None, '26'])[1], 26)
    fam = d.get('font-family', '') + ' ' + font_sh
    face = 'display' if 'font-display' in fam else 'mono' if 'font-mono' in fam else 'body'
    wt = d.get('font-weight') or (re.match(r'\s*(\d{3})\b', font_sh) or [None, '400'])[1]
    bold = px(wt, 400) >= 600
    col = _col(ctx, d.get('color')) or ctx.t['fg']
    bg = _col(ctx, d.get('background') or d.get('background-color'))
    bd = re.search(r'(\d+(?:\.\d+)?)px\s+\w+\s+(.+)', d.get('border', ''))
    line = ((_col(ctx, bd.group(2)) or ctx.t['fg']), float(bd.group(1))) if bd else None
    pad = [px(p) for p in resolve(d.get('padding', '0'), [getattr(ctx, 'tok', {})]).split()] or [0]
    al = {'center': 'ctr', 'right': 'r'}.get(d.get('text-align', '').strip(), 'l')
    rs = runs(ctx, k, fs, col, face, bold)
    bd_rule = {}   # `.box b { font-family: var(--font-display); font-size: 1.3em }`: headings inside a block
    for sel, _, _, dd in getattr(getattr(ctx, 'sheet', None), 'rules', []):
        parts = sel.split()
        if len(parts) >= 2 and parts[-1] in ('b', 'strong') and set(re.findall(r'\.([\w-]+)', parts[-2])) <= set(k.cls) and '.' in parts[-2]:
            bd_rule.update(dd)
    if bd_rule and not bold:
        em = re.search(r'([\d.]+)em', bd_rule.get('font-size', ''))
        for r in (r for r in rs if r['bold']):
            r['size'] = fs * float(em.group(1)) if em else r['size']
            if 'font-display' in bd_rule.get('font-family', ''):
                r.update(font=ctx.t['font_display'], bold=ctx.t.get('display_bold', True))
    ps, cur = [], []
    for r in rs:   # a <br> starts a new paragraph so headings stay on their own line
        if r['text'] == '\n':
            ps.append(para(cur, al)) if cur else None
            cur = []
        else:
            cur.append(r)
    if cur:
        ps.append(para(cur, al))
    ctx.box('Text', x, y, w, max(h, 40) if h < 1000 else 120, ps or [para([])], 'ctr' if 'cell-k' in k.cls else 't',
            fill=bg, line=line, inset=pad[1] if len(pad) > 1 else pad[0])
    ctx.items[-1]['src'] = k


def css_box(ctx, k):
    """A block the deck CSS places absolutely (`.src-note { position: absolute; left; right; bottom }`) -> its box."""
    d = decl(ctx, k)
    if d.get('position') != 'absolute' or not any(s in d for s in ('left', 'right', 'top', 'bottom')):
        return None
    g = {s: px(d[s]) for s in ('left', 'right', 'top', 'bottom', 'width', 'height') if s in d and d[s].endswith('px')}
    x = g.get('left', 120)
    w = g.get('width', 1920 - x - g.get('right', 120))
    fs = px(d.get('font-size', '26'), 26)
    h = g.get('height', sum(max(1, -(-len(ln) * fs * 0.5 // w)) for ln in k.text().split('\n')) * fs * 1.4 + 6)
    y = g['top'] if 'top' in g else 1080 - g.get('bottom', 60) - h
    return x, y, w, h


def _png1():
    raw = b'\0\0\0\0\0'
    chunk = lambda t, b: struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xFFFFFFFF)  # noqa: E731
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')


CAMEL = {k.lower(): k for k in ('viewBox', 'pathLength', 'preserveAspectRatio', 'gradientUnits', 'gradientTransform', 'patternUnits',
                                 'patternTransform', 'patternContentUnits', 'clipPathUnits', 'maskUnits', 'linearGradient',
                                 'radialGradient', 'clipPath', 'textPath', 'markerWidth', 'markerHeight', 'refX', 'refY', 'stdDeviation')}


def _svg(ctx, n, root=False):
    """DOM subtree -> SVG markup with CSS classes inlined (the HTML parser lowercased names: SVG needs camelCase back)."""
    if isinstance(n, str):
        return escape(n)
    a = {CAMEL.get(k, k): v for k, v in n.attrs.items() if k not in ('class', 'style', 'aria-hidden') and v is not None}
    tag = CAMEL.get(n.tag, n.tag)
    d = decl(ctx, n)
    m = re.match(r'\s*(\d{3})?\s*(\d+(?:\.\d+)?)px\s+(.+)', d.get('font', ''))
    if m:
        d.setdefault('font-weight', m.group(1) or '400')
        d.setdefault('font-size', m.group(2) + 'px')
        d.setdefault('font-family', m.group(3))
    for p in SVG_PROPS:
        v = d.get(p)
        if not v or (p == 'stroke-dasharray' and 'pathlength' in n.attrs):   # .draw dashes rely on pathLength
            continue
        if p == 'font-family':
            v = ctx.t['font_mono' if 'mono' in v else 'font_display' if 'display' in v else 'font_body']
        elif p in ('fill', 'stroke') and v != 'none':
            c = _col(ctx, v)
            v, alpha = ('#' + c[0], c[1]) if c else ('none', 1)
            if alpha < 1:
                a[p + '-opacity'] = f'{alpha:.3f}'
        else:
            v = resolve(v, [getattr(ctx, 'tok', {})])
        a[p] = v
    if root:
        a['xmlns'] = 'http://www.w3.org/2000/svg'
    attrs = ''.join(f' {k}={quoteattr(str(v))}' for k, v in a.items())
    return f'<{tag}{attrs}>' + ''.join(_svg(ctx, k) for k in n.kids) + f'</{tag}>'


def svg_pic(ctx, node, images):
    """Inline <svg> placed by left/top -> SVG picture item with a draw / rise entrance like the HTML."""
    st = node.attrs.get('style', '')
    g = {k: float(v) for k, v in re.findall(r'(left|top):\s*(-?\d+(?:\.\d+)?)px', st)}
    w, h = px(node.attrs.get('width', '0')), px(node.attrs.get('height', '0'))
    if not (w and h and 'left' in g):
        return
    k = len(images) + 1
    images[f'rIdS{k}'] = (f'free{id(node)}_{k}.svg', _svg(ctx, node, True).encode('utf-8'))
    images[f'rIdP{k}'] = ('blank1x1.png', _png1())
    classes = {c for n in [node] + list(_walk(node)) for c in n.cls}
    d = re.search(r'--d:\s*([\d.]+)', ' '.join(n.attrs.get('style', '') for n in _walk(node)))
    kind = 'wipe' if 'draw' in classes else 'rise' if classes & {'fx', 'fx-up', 'fx-pop'} else 'fade'
    ctx.items.append({'name': 'Drawing', 'image': True, 'rid': f'rIdP{k}', 'svg_rid': f'rIdS{k}', 'x': g['left'], 'y': g.get('top', 0),
                      'w': w, 'h': h, 'fx': [(None, {'kind': kind, 'step': 0, 'delay': float(d.group(1)) * 1000 if d else 0, 'anchor': id(node)})]})


def svg_items(items, images):
    """Items carrying 'svg' markup (patterned actors, stage paper) -> SVG pictures stored once per distinct drawing."""
    for it in items:
        svg = it.pop('svg', None)
        if svg is None:
            continue
        key = __import__('hashlib').md5(svg.encode('utf-8')).hexdigest()[:12]
        images[f'rIdV{key}'] = (f'pat{key}.svg', svg.encode('utf-8'))
        images['rIdBlank'] = ('blank1x1.png', _png1())
        it.update(image=True, rid='rIdBlank', svg_rid=f'rIdV{key}')


def _walk(n):
    for k in n.kids:
        if not isinstance(k, str):
            yield k
            yield from _walk(k)
